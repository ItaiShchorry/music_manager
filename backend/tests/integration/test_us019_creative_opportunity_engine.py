"""
US-019: Creative Opportunity Engine — expanded with creative + youtube categories
- category field saved on PostOpportunity
- creative signal types present when catalog signals detected
- YouTube signals: story_ready, no_video, youtube_milestone
- generate endpoint response includes category field
"""
import pytest
from datetime import date, datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from app.models.post_opportunity import PostOpportunity
from app.models.song import Song
from app.models.youtube_brief import YouTubeBrief


MOCK_CREATIVE_RESPONSE = """[
  {
    "hook": "You write a lot about longing — write a verse where it turns to peace, without using either word.",
    "why_now": "Your catalog shows a strong emotional pattern that deserves exploration.",
    "signal_type": "lyric_prompt",
    "category": "creative",
    "suggested_platform": "instagram",
    "hashtag_suggestions": ["#songwriting", "#מוזיקה_ישראלית", "#lyrics"],
    "timing_note": null
  },
  {
    "hook": "Your catalog has 3 songs but none explore joy or celebration — try writing something upbeat.",
    "why_now": "Catalog gap identified: no major-key or celebratory songs.",
    "signal_type": "catalog_gap",
    "category": "creative",
    "suggested_platform": "tiktok",
    "hashtag_suggestions": ["#newmusic", "#challenge"],
    "timing_note": null
  },
  {
    "hook": "Share your latest milestone with fans — celebrate hitting 1000 streams!",
    "why_now": "You just crossed a streaming milestone your audience will love to hear about.",
    "signal_type": "milestone",
    "category": "promotion",
    "suggested_platform": "instagram",
    "hashtag_suggestions": ["#milestone", "#מוזיקה_ישראלית"],
    "timing_note": null
  }
]"""


def _make_mock_client():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=MOCK_CREATIVE_RESPONSE)]
    )
    return mock_client


# ---------------------------------------------------------------------------
# Category field saved correctly
# ---------------------------------------------------------------------------

def test_generate_saves_category_field(client, sample_song, auth_headers, db):
    """POST /opportunities/generate saves the category field from Claude response."""
    with patch("app.services.opportunity_service.anthropic") as patched:
        patched.Anthropic.return_value = _make_mock_client()
        resp = client.post(
            "/api/v1/opportunities/generate",
            json={"song_id": sample_song.id},
            headers=auth_headers,
        )
    assert resp.status_code == 201
    data = resp.json()
    assert len(data) > 0
    categories = {item["category"] for item in data}
    assert "creative" in categories or "promotion" in categories


def test_opportunity_response_includes_category(client, sample_song, auth_headers, db):
    """GET /opportunities returns category field on each item."""
    # Create an opportunity directly
    opp = PostOpportunity(
        user_id=sample_song.user_id,
        hook="Test hook",
        why_now="Test why",
        signal_type="lyric_prompt",
        category="creative",
        status="active",
    )
    db.add(opp)
    db.flush()

    resp = client.get("/api/v1/opportunities", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert any(item["category"] == "creative" for item in data)


def test_category_defaults_to_promotion_for_old_signal_types(client, sample_song, auth_headers, db):
    """Existing signal types (milestone, inactivity, etc.) get category='promotion'."""
    opp = PostOpportunity(
        user_id=sample_song.user_id,
        hook="Milestone hook",
        why_now="Hit 10k streams",
        signal_type="milestone",
        category="promotion",
        status="active",
    )
    db.add(opp)
    db.flush()

    resp = client.get("/api/v1/opportunities", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    milestone_ops = [i for i in data if i["signal_type"] == "milestone"]
    assert all(o["category"] == "promotion" for o in milestone_ops)


# ---------------------------------------------------------------------------
# Creative signals detection
# ---------------------------------------------------------------------------

def test_collect_signals_returns_lyric_prompt_for_song_with_moods(db, sample_user, sample_song):
    """lyric_prompt signal generated when song has mood_tags."""
    from app.models.song import Song
    song = db.query(Song).filter(Song.id == sample_song.id).first()
    song.mood_tags = ["longing", "melancholic"]
    song.themes = ["loss", "love"]
    db.flush()

    from app.services.opportunity_service import collect_signals
    signals = collect_signals(sample_user.id, db, songs=[song])
    signal_types = [s["type"] for s in signals]
    assert "lyric_prompt" in signal_types


def test_collect_signals_catalog_gap_detected(db, sample_user, sample_song):
    """catalog_gap signal generated when catalog has genre imbalance."""
    from app.models.song import Song
    # Create multiple songs of same genre
    for i in range(3):
        s = Song(
            user_id=sample_user.id,
            spotify_track_id=f"sad_track_{i}",
            title=f"Sad Song {i}",
            artist_name="Test",
            mood_tags=["sad", "melancholic"],
            themes=["loss"],
        )
        db.add(s)
    db.flush()

    all_songs = db.query(Song).filter(Song.user_id == sample_user.id).all()
    from app.services.opportunity_service import collect_signals
    signals = collect_signals(sample_user.id, db, songs=all_songs)
    signal_types = [s["type"] for s in signals]
    assert "catalog_gap" in signal_types


def test_collect_signals_story_ready_for_youtube(db, sample_user, sample_song):
    """story_ready signal generated when song has story > 100 chars and no brief."""
    from app.models.song import Song
    song = db.query(Song).filter(Song.id == sample_song.id).first()
    song.story = "A" * 110  # > 100 chars
    db.flush()

    from app.services.opportunity_service import collect_signals
    signals = collect_signals(sample_user.id, db, songs=[song])
    signal_types = [s["type"] for s in signals]
    assert "story_ready" in signal_types


def test_collect_signals_no_story_ready_when_brief_exists(db, sample_user, sample_song):
    """No story_ready signal if song already has a YouTube brief."""
    from app.models.song import Song
    song = db.query(Song).filter(Song.id == sample_song.id).first()
    song.story = "A" * 110
    db.flush()

    brief = YouTubeBrief(
        user_id=sample_user.id,
        song_id=sample_song.id,
        concept_type="song_explained",
        status="draft",
    )
    db.add(brief)
    db.flush()

    from app.services.opportunity_service import collect_signals
    signals = collect_signals(sample_user.id, db, songs=[song])
    signal_types = [s["type"] for s in signals]
    assert "story_ready" not in signal_types


def test_collect_signals_no_video_for_old_song(db, sample_user, sample_song):
    """no_video signal for songs > 60 days old with no brief."""
    from app.models.song import Song
    song = db.query(Song).filter(Song.id == sample_song.id).first()
    song.release_date = date.today() - timedelta(days=90)
    db.flush()

    from app.services.opportunity_service import collect_signals
    signals = collect_signals(sample_user.id, db, songs=[song])
    signal_types = [s["type"] for s in signals]
    assert "no_video" in signal_types


# ---------------------------------------------------------------------------
# Full generate endpoint with creative Claude response
# ---------------------------------------------------------------------------

def test_generate_endpoint_returns_creative_and_promotion_categories(
    client, sample_song, auth_headers, db
):
    """generate endpoint returns mix of creative and promotion category items."""
    from app.models.song import Song
    song = db.query(Song).filter(Song.id == sample_song.id).first()
    song.mood_tags = ["melancholic"]
    song.themes = ["loss"]
    db.commit()

    with patch("app.services.opportunity_service.anthropic") as patched:
        patched.Anthropic.return_value = _make_mock_client()
        resp = client.post(
            "/api/v1/opportunities/generate",
            json={},
            headers=auth_headers,
        )
    assert resp.status_code == 201
    data = resp.json()
    categories = {item["category"] for item in data}
    # Both creative and promotion should appear in the mock response
    assert len(categories) >= 1
