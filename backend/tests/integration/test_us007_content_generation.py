"""
US-007: POST /songs/{id}/content — Hebrew social media content generation.
        GET  /songs/{id}/content — list previously generated content.

TDD: tests written FIRST. All Anthropic API calls are mocked — no real calls.
"""
import json
from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from app.models.song import Song

# ---------------------------------------------------------------------------
# Shared mock helpers
# ---------------------------------------------------------------------------

FAKE_CLAUDE_RESPONSE = {
    "caption_hebrew": "שיר חדש בחוץ עכשיו! 🎵 אחלה של יום לשתף אתכם.",
    "caption_english": "New song out now! 🎵 So excited to share this with you.",
    "hashtags_hebrew": ["#מוזיקה_ישראלית", "#שיר_חדש", "#אינדי"],
    "hashtags_english": ["#IsraeliMusic", "#NewSong", "#IndieMusic"],
}


def _make_mock_anthropic():
    """Build a mock anthropic.Anthropic() that returns FAKE_CLAUDE_RESPONSE."""
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(text=json.dumps(FAKE_CLAUDE_RESPONSE))]
    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_msg
    mock_anthropic_class = MagicMock(return_value=mock_client)
    return mock_anthropic_class, mock_client


def _song_with_profile(db, sample_user):
    """Helper: create a song with full profile fields."""
    song = Song(
        user_id=sample_user.id,
        spotify_track_id="content_test_song_abc123",
        title="לב קפוא",
        artist_name="Test Artist",
        release_date=date(2024, 3, 1),
        genre="indie pop",
        language="hebrew",
        mood_tags=["melancholic", "emotional"],
        story="כתבתי את השיר הזה בתקופה קשה.",
    )
    db.add(song)
    db.flush()
    return song


# ---------------------------------------------------------------------------
# POST /songs/{id}/content — generate content
# ---------------------------------------------------------------------------

def test_generate_content_happy_path(client, db, sample_user, auth_headers):
    """Generate content with 3 tones × 3 platforms → 9 items returned, saved."""
    song = _song_with_profile(db, sample_user)
    mock_cls, mock_client = _make_mock_anthropic()

    with patch("app.services.content_generator.anthropic", mock_cls) as patched:
        # anthropic is imported as module; Anthropic() is called on it
        patched.Anthropic.return_value = mock_client

        r = client.post(
            f"/api/v1/songs/{song.id}/content",
            json={
                "post_type": "release",
                "key_message": "Out now on Spotify",
                "tones": ["emotional", "excited", "casual"],
                "platforms": ["instagram", "facebook", "tiktok"],
            },
            headers=auth_headers,
        )

    assert r.status_code == 201, r.text
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 9  # 3 tones × 3 platforms


def test_generate_content_response_structure(client, db, sample_user, auth_headers):
    """Each item in the response has the required fields."""
    song = _song_with_profile(db, sample_user)
    mock_cls, mock_client = _make_mock_anthropic()

    with patch("app.services.content_generator.anthropic", mock_cls) as patched:
        patched.Anthropic.return_value = mock_client

        r = client.post(
            f"/api/v1/songs/{song.id}/content",
            json={
                "post_type": "release",
                "tones": ["emotional"],
                "platforms": ["instagram"],
            },
            headers=auth_headers,
        )

    assert r.status_code == 201, r.text
    item = r.json()[0]
    assert "id" in item
    assert item["song_id"] == song.id
    assert item["post_type"] == "release"
    assert item["platform"] == "instagram"
    assert item["tone"] == "emotional"
    assert "caption_hebrew" in item
    assert "caption_english" in item
    assert "hashtags" in item
    assert isinstance(item["hashtags"], list)
    assert "character_count" in item
    assert "created_at" in item


def test_generate_content_requires_auth(client, sample_song):
    """Unauthenticated request → 401."""
    r = client.post(
        f"/api/v1/songs/{sample_song.id}/content",
        json={"post_type": "release"},
    )
    assert r.status_code == 401


def test_generate_content_song_not_found(client, auth_headers):
    """Song ID that doesn't exist → 404."""
    mock_cls, mock_client = _make_mock_anthropic()

    with patch("app.services.content_generator.anthropic", mock_cls) as patched:
        patched.Anthropic.return_value = mock_client

        r = client.post(
            "/api/v1/songs/99999/content",
            json={"post_type": "release"},
            headers=auth_headers,
        )

    assert r.status_code == 404


def test_generate_content_wrong_user(client, db, sample_user, auth_headers):
    """Song belonging to another user → 404 (ownership check)."""
    from app.models.user import User
    from app.utils.auth import hash_password

    other_user = User(
        email="other@example.com",
        hashed_password=hash_password("pass"),
        name="Other",
    )
    db.add(other_user)
    db.flush()

    other_song = Song(
        user_id=other_user.id,
        spotify_track_id="other_user_song_xyz",
        title="Other Song",
        artist_name="Other Artist",
        release_date=date(2024, 1, 1),
    )
    db.add(other_song)
    db.flush()

    mock_cls, mock_client = _make_mock_anthropic()

    with patch("app.services.content_generator.anthropic", mock_cls) as patched:
        patched.Anthropic.return_value = mock_client

        r = client.post(
            f"/api/v1/songs/{other_song.id}/content",
            json={"post_type": "release"},
            headers=auth_headers,
        )

    assert r.status_code == 404


def test_generate_content_invalid_post_type(client, auth_headers, sample_song):
    """Invalid post_type → 422 validation error."""
    r = client.post(
        f"/api/v1/songs/{sample_song.id}/content",
        json={"post_type": "invalid_type"},
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_generate_content_single_variant(client, db, sample_user, auth_headers):
    """Single tone + single platform → exactly 1 item returned."""
    song = _song_with_profile(db, sample_user)
    mock_cls, mock_client = _make_mock_anthropic()

    with patch("app.services.content_generator.anthropic", mock_cls) as patched:
        patched.Anthropic.return_value = mock_client

        r = client.post(
            f"/api/v1/songs/{song.id}/content",
            json={
                "post_type": "bts",
                "tones": ["casual"],
                "platforms": ["facebook"],
            },
            headers=auth_headers,
        )

    assert r.status_code == 201, r.text
    assert len(r.json()) == 1
    item = r.json()[0]
    assert item["tone"] == "casual"
    assert item["platform"] == "facebook"


def test_generate_content_defaults(client, db, sample_user, auth_headers):
    """Omitting tones and platforms uses all 3 tones × all 3 platforms → 9 items."""
    song = _song_with_profile(db, sample_user)
    mock_cls, mock_client = _make_mock_anthropic()

    with patch("app.services.content_generator.anthropic", mock_cls) as patched:
        patched.Anthropic.return_value = mock_client

        r = client.post(
            f"/api/v1/songs/{song.id}/content",
            json={"post_type": "release"},
            headers=auth_headers,
        )

    assert r.status_code == 201, r.text
    assert len(r.json()) == 9


def test_generate_content_character_count_stored(client, db, sample_user, auth_headers):
    """character_count is populated and equals len(caption_hebrew)."""
    song = _song_with_profile(db, sample_user)
    mock_cls, mock_client = _make_mock_anthropic()

    with patch("app.services.content_generator.anthropic", mock_cls) as patched:
        patched.Anthropic.return_value = mock_client

        r = client.post(
            f"/api/v1/songs/{song.id}/content",
            json={"post_type": "release", "tones": ["emotional"], "platforms": ["instagram"]},
            headers=auth_headers,
        )

    assert r.status_code == 201, r.text
    item = r.json()[0]
    # character_count should equal len(caption_hebrew) — confirms it's populated
    assert item["character_count"] == len(item["caption_hebrew"])


# ---------------------------------------------------------------------------
# GET /songs/{id}/content — list previously generated content
# ---------------------------------------------------------------------------

def test_list_content_empty(client, db, sample_user, auth_headers):
    """Song with no generated content returns empty list."""
    song = _song_with_profile(db, sample_user)

    r = client.get(f"/api/v1/songs/{song.id}/content", headers=auth_headers)
    assert r.status_code == 200, r.text
    assert r.json() == []


def test_list_content_after_generation(client, db, sample_user, auth_headers):
    """After generating content, GET returns those items (most recent first)."""
    song = _song_with_profile(db, sample_user)
    mock_cls, mock_client = _make_mock_anthropic()

    with patch("app.services.content_generator.anthropic", mock_cls) as patched:
        patched.Anthropic.return_value = mock_client

        client.post(
            f"/api/v1/songs/{song.id}/content",
            json={"post_type": "release", "tones": ["emotional"], "platforms": ["instagram"]},
            headers=auth_headers,
        )

    r = client.get(f"/api/v1/songs/{song.id}/content", headers=auth_headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert len(data) == 1
    assert data[0]["post_type"] == "release"


def test_list_content_requires_auth(client, sample_song):
    r = client.get(f"/api/v1/songs/{sample_song.id}/content")
    assert r.status_code == 401


def test_list_content_song_not_found(client, auth_headers):
    r = client.get("/api/v1/songs/99999/content", headers=auth_headers)
    assert r.status_code == 404
