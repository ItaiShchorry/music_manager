"""
US-004: GET /songs/{song_id}/matches — playlist + radio station match scores.

TDD: tests written first.
"""
import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _song_with_profile(db, sample_user, genre, language, mood_tags):
    """Create a song with profile fields set."""
    from datetime import date
    from app.models.song import Song

    song = Song(
        user_id=sample_user.id,
        spotify_track_id=f"profile_song_{genre}_{language}",
        title="Profile Song",
        artist_name="Test Artist",
        release_date=date(2024, 6, 1),
        genre=genre,
        language=language,
        mood_tags=mood_tags,
    )
    db.add(song)
    db.flush()
    return song


# ---------------------------------------------------------------------------
# Cases
# ---------------------------------------------------------------------------

def test_match_happy_path(client, db, sample_user, auth_headers, sample_playlist, sample_radio_station):
    """Song with genre + language + mood_tags returns 200 with sorted playlists."""
    song = _song_with_profile(db, sample_user, "indie pop", "hebrew", ["melancholic"])

    r = client.get(f"/api/v1/songs/{song.id}/matches", headers=auth_headers)
    assert r.status_code == 200, r.text
    data = r.json()

    assert "playlists" in data
    assert "radio_stations" in data

    # Playlists should be sorted by score descending
    scores = [p["score"] for p in data["playlists"]]
    assert scores == sorted(scores, reverse=True)

    # sample_playlist (genres=["indie", "alternative"], languages=["hebrew"]) should score > 0
    matching = [p for p in data["playlists"] if p["playlist"]["id"] == sample_playlist.id]
    assert len(matching) == 1
    assert matching[0]["score"] > 0
    assert "reasons" in matching[0]


def test_match_bare_song_returns_all_playlists(client, db, sample_user, auth_headers, sample_playlist, sample_radio_station):
    """Song with no profile fields still returns all playlists with score 0."""
    from datetime import date
    from app.models.song import Song

    song = Song(
        user_id=sample_user.id,
        spotify_track_id="bare_song_no_profile",
        title="Bare Song",
        artist_name="Bare Artist",
        release_date=date(2024, 1, 1),
    )
    db.add(song)
    db.flush()

    r = client.get(f"/api/v1/songs/{song.id}/matches", headers=auth_headers)
    assert r.status_code == 200, r.text
    data = r.json()

    # All playlists are returned (even if score 0)
    assert len(data["playlists"]) >= 1
    # All scores are 0 since song has no profile
    for p in data["playlists"]:
        assert p["score"] == 0


def test_match_requires_auth(client, sample_song):
    r = client.get(f"/api/v1/songs/{sample_song.id}/matches")
    assert r.status_code == 401


def test_match_song_not_found(client, auth_headers):
    r = client.get("/api/v1/songs/99999/matches", headers=auth_headers)
    assert r.status_code == 404


def test_match_response_structure(client, db, sample_user, auth_headers, sample_playlist, sample_radio_station):
    """Verify the full response structure matches the spec."""
    song = _song_with_profile(db, sample_user, "indie", "hebrew", ["upbeat"])

    r = client.get(f"/api/v1/songs/{song.id}/matches", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()

    # Playlist entries have expected keys
    for entry in data["playlists"]:
        assert "playlist" in entry
        assert "score" in entry
        assert "reasons" in entry
        assert isinstance(entry["reasons"], list)

    # Radio station entries have expected keys
    for entry in data["radio_stations"]:
        assert "station" in entry
        assert "recommended" in entry
        assert isinstance(entry["recommended"], bool)
