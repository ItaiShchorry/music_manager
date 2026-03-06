"""
US-016: YouTube Video Brief Generator
- POST /songs/{id}/youtube-briefs generates and saves a brief
- Claude returns seo_title, hook_paragraph, chapters, video_description, tags
- Falls back to structured placeholder on Claude failure
- 422 on invalid concept_type
- 404 if song not found
- 401 if unauthenticated
- search_keywords included in Claude prompt
"""
import pytest
from unittest.mock import MagicMock, patch

VALID_CONCEPT_TYPES = [
    "making_of",
    "acoustic_session",
    "production_breakdown",
    "song_explained",
    "live_performance",
]

MOCK_CLAUDE_RESPONSE = """{
  "seo_title": "How I Made 'Test Song' — Production Breakdown",
  "hook_paragraph": "Ever wondered what goes into making an Israeli indie track? In this video I walk you through every layer of 'Test Song', from the initial voice memo to the final master. You'll see how I built the beat, why I chose that specific chord progression, and the moment I knew the chorus was perfect.",
  "chapters": [
    {"timestamp": "0:00", "title": "Intro", "what_to_cover": "Quick teaser of the final track"},
    {"timestamp": "1:30", "title": "The Seed Idea", "what_to_cover": "The original voice memo and where inspiration struck"},
    {"timestamp": "4:00", "title": "Building the Beat", "what_to_cover": "Drum programming and rhythm choices"},
    {"timestamp": "8:00", "title": "Chord Progression & Melody", "what_to_cover": "How the harmony was developed"},
    {"timestamp": "12:00", "title": "Final Mix", "what_to_cover": "Key mixing decisions and what to listen for"}
  ],
  "video_description": "A behind-the-scenes look at creating 'Test Song'. Perfect for fans curious about Israeli indie production and songwriting.",
  "tags": ["production breakdown", "Israeli indie", "music production", "songwriting", "מוזיקה_ישראלית", "behind the scenes", "how i make music", "indie pop"]
}"""


def _make_mock_client():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=MOCK_CLAUDE_RESPONSE)]
    )
    return mock_client


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_generate_brief_happy_path(client, sample_song, auth_headers):
    """POST /songs/{id}/youtube-briefs returns 201 with brief content."""
    with patch("app.services.youtube_brief_generator.anthropic") as patched:
        patched.Anthropic.return_value = _make_mock_client()
        resp = client.post(
            f"/api/v1/songs/{sample_song.id}/youtube-briefs",
            json={"concept_type": "production_breakdown"},
            headers=auth_headers,
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["concept_type"] == "production_breakdown"
    assert data["seo_title"] == "How I Made 'Test Song' — Production Breakdown"
    assert "hook_paragraph" in data
    assert isinstance(data["chapters"], list)
    assert len(data["chapters"]) >= 3
    assert isinstance(data["tags"], list)
    assert data["status"] == "draft"
    assert data["song_id"] == sample_song.id


def test_generate_brief_with_key_message(client, sample_song, auth_headers):
    """key_message and context are saved and passed to Claude."""
    with patch("app.services.youtube_brief_generator.anthropic") as patched:
        patched.Anthropic.return_value = _make_mock_client()
        resp = client.post(
            f"/api/v1/songs/{sample_song.id}/youtube-briefs",
            json={
                "concept_type": "song_explained",
                "key_message": "This song is about letting go",
                "context": "Written after a difficult breakup",
            },
            headers=auth_headers,
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["key_message"] == "This song is about letting go"
    assert data["context"] == "Written after a difficult breakup"


def test_generate_brief_fallback_on_claude_error(client, sample_song, auth_headers):
    """Falls back to structured placeholder when Claude raises an exception."""
    with patch("app.services.youtube_brief_generator.anthropic") as patched:
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = Exception("API timeout")
        patched.Anthropic.return_value = mock_client
        resp = client.post(
            f"/api/v1/songs/{sample_song.id}/youtube-briefs",
            json={"concept_type": "acoustic_session"},
            headers=auth_headers,
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["seo_title"] is not None  # fallback content present
    assert data["status"] == "draft"


def test_generate_brief_invalid_concept_type(client, sample_song, auth_headers):
    """422 when concept_type is not one of the valid values."""
    resp = client.post(
        f"/api/v1/songs/{sample_song.id}/youtube-briefs",
        json={"concept_type": "invalid_type"},
        headers=auth_headers,
    )
    assert resp.status_code == 422


def test_generate_brief_404_song_not_found(client, auth_headers):
    """404 when song_id does not exist."""
    with patch("app.services.youtube_brief_generator.anthropic") as patched:
        patched.Anthropic.return_value = _make_mock_client()
        resp = client.post(
            "/api/v1/songs/99999/youtube-briefs",
            json={"concept_type": "making_of"},
            headers=auth_headers,
        )
    assert resp.status_code == 404


def test_generate_brief_401_unauthenticated(client, sample_song):
    """401 when no auth token provided."""
    resp = client.post(
        f"/api/v1/songs/{sample_song.id}/youtube-briefs",
        json={"concept_type": "making_of"},
    )
    assert resp.status_code == 401


def test_list_briefs_for_song(client, sample_song, auth_headers, db):
    """GET /songs/{id}/youtube-briefs returns list of briefs."""
    from app.models.youtube_brief import YouTubeBrief
    brief = YouTubeBrief(
        user_id=sample_song.user_id,
        song_id=sample_song.id,
        concept_type="making_of",
        seo_title="Test Brief",
        status="draft",
    )
    db.add(brief)
    db.flush()

    resp = client.get(f"/api/v1/songs/{sample_song.id}/youtube-briefs", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert any(b["seo_title"] == "Test Brief" for b in data)


def test_generate_brief_search_keywords_in_prompt(client, sample_song, auth_headers, db):
    """search_keywords from song are passed to the Claude prompt."""
    from app.models.song import Song
    song = db.query(Song).filter(Song.id == sample_song.id).first()
    song.search_keywords = ["melancholic Israeli indie", "songs about loss"]
    db.commit()

    captured_prompts = []
    mock_msg = MagicMock(content=[MagicMock(text=MOCK_CLAUDE_RESPONSE)])

    def capture_and_return(**kwargs):
        content = kwargs.get("messages", [{}])[0].get("content", "")
        captured_prompts.append(content)
        return mock_msg

    with patch("app.services.youtube_brief_generator.anthropic") as patched:
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = capture_and_return
        patched.Anthropic.return_value = mock_client
        resp = client.post(
            f"/api/v1/songs/{sample_song.id}/youtube-briefs",
            json={"concept_type": "song_explained"},
            headers=auth_headers,
        )
    assert resp.status_code == 201
    assert len(captured_prompts) == 1
    assert "melancholic Israeli indie" in captured_prompts[0]
