"""
US-006: Pitch submission tracking.

  POST   /api/v1/pitches
  GET    /api/v1/songs/{song_id}/pitches
  PATCH  /api/v1/pitches/{pitch_id}
"""
import pytest


# ---------------------------------------------------------------------------
# Cases
# ---------------------------------------------------------------------------

def test_log_playlist_pitch(client, auth_headers, sample_song, sample_playlist):
    """POST a pitch against a playlist → 201 created."""
    payload = {
        "song_id": sample_song.id,
        "target_type": "playlist",
        "playlist_id": sample_playlist.id,
        "pitch_method": "email",
    }
    r = client.post("/api/v1/pitches", json=payload, headers=auth_headers)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["song_id"] == sample_song.id
    assert data["playlist_id"] == sample_playlist.id
    assert data["status"] == "sent"
    assert data["target_type"] == "playlist"


def test_log_radio_pitch(client, auth_headers, sample_song, sample_radio_station):
    """POST a pitch against a radio station → 201 created."""
    payload = {
        "song_id": sample_song.id,
        "target_type": "radio",
        "radio_station_id": sample_radio_station.id,
        "pitch_method": "email",
    }
    r = client.post("/api/v1/pitches", json=payload, headers=auth_headers)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["radio_station_id"] == sample_radio_station.id
    assert data["target_type"] == "radio"


def test_get_pitches_for_song(client, auth_headers, sample_song, sample_playlist):
    """GET /songs/{id}/pitches returns list of pitches."""
    # Create a pitch first
    client.post(
        "/api/v1/pitches",
        json={
            "song_id": sample_song.id,
            "target_type": "playlist",
            "playlist_id": sample_playlist.id,
            "pitch_method": "email",
        },
        headers=auth_headers,
    )

    r = client.get(f"/api/v1/songs/{sample_song.id}/pitches", headers=auth_headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["song_id"] == sample_song.id


def test_update_pitch_status(client, auth_headers, sample_song, sample_playlist):
    """PATCH /pitches/{id} can update status."""
    create_r = client.post(
        "/api/v1/pitches",
        json={
            "song_id": sample_song.id,
            "target_type": "playlist",
            "playlist_id": sample_playlist.id,
            "pitch_method": "email",
        },
        headers=auth_headers,
    )
    pitch_id = create_r.json()["id"]

    r = client.patch(
        f"/api/v1/pitches/{pitch_id}",
        json={"status": "added"},
        headers=auth_headers,
    )
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "added"


def test_pitch_requires_auth(client, sample_song, sample_playlist):
    r = client.post(
        "/api/v1/pitches",
        json={
            "song_id": sample_song.id,
            "target_type": "playlist",
            "playlist_id": sample_playlist.id,
            "pitch_method": "email",
        },
    )
    assert r.status_code == 401


def test_get_pitches_song_not_found(client, auth_headers):
    r = client.get("/api/v1/songs/99999/pitches", headers=auth_headers)
    assert r.status_code == 404


def test_pitch_with_invalid_song(client, auth_headers, sample_playlist):
    """Pitching against a non-existent song returns 404."""
    r = client.post(
        "/api/v1/pitches",
        json={
            "song_id": 99999,
            "target_type": "playlist",
            "playlist_id": sample_playlist.id,
            "pitch_method": "email",
        },
        headers=auth_headers,
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

def test_invalid_target_type_rejected(client, auth_headers, sample_song, sample_playlist):
    """target_type must be 'playlist' or 'radio' — anything else is 422."""
    r = client.post(
        "/api/v1/pitches",
        json={
            "song_id": sample_song.id,
            "target_type": "banana",
            "playlist_id": sample_playlist.id,
            "pitch_method": "email",
        },
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_invalid_pitch_method_rejected(client, auth_headers, sample_song, sample_playlist):
    """pitch_method must be one of the allowed values."""
    r = client.post(
        "/api/v1/pitches",
        json={
            "song_id": sample_song.id,
            "target_type": "playlist",
            "playlist_id": sample_playlist.id,
            "pitch_method": "telegram",
        },
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_invalid_status_in_patch_rejected(client, auth_headers, sample_song, sample_playlist):
    """PATCH status must be one of the allowed values."""
    create_r = client.post(
        "/api/v1/pitches",
        json={
            "song_id": sample_song.id,
            "target_type": "playlist",
            "playlist_id": sample_playlist.id,
            "pitch_method": "email",
        },
        headers=auth_headers,
    )
    pitch_id = create_r.json()["id"]
    r = client.patch(
        f"/api/v1/pitches/{pitch_id}",
        json={"status": "garbage"},
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_playlist_pitch_without_playlist_id_rejected(client, auth_headers, sample_song):
    """target_type='playlist' with no playlist_id must return 422."""
    r = client.post(
        "/api/v1/pitches",
        json={
            "song_id": sample_song.id,
            "target_type": "playlist",
            "pitch_method": "email",
        },
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_pitch_nonexistent_playlist_returns_404(client, auth_headers, sample_song):
    """Pitching to a playlist ID that doesn't exist returns 404."""
    r = client.post(
        "/api/v1/pitches",
        json={
            "song_id": sample_song.id,
            "target_type": "playlist",
            "playlist_id": 99999,
            "pitch_method": "email",
        },
        headers=auth_headers,
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Ownership / cross-user isolation
# ---------------------------------------------------------------------------

def test_cannot_read_another_users_pitches(db, client, sample_song, sample_playlist, auth_headers):
    """A second user cannot read pitches for a song they don't own."""
    from app.models.user import User
    from app.utils.auth import create_access_token, hash_password

    other_user = User(
        email="other@example.com",
        hashed_password=hash_password("otherpass"),
        name="Other User",
    )
    db.add(other_user)
    db.flush()
    other_headers = {"Authorization": f"Bearer {create_access_token(other_user.id)}"}

    # First create a pitch as the real user
    client.post(
        "/api/v1/pitches",
        json={
            "song_id": sample_song.id,
            "target_type": "playlist",
            "playlist_id": sample_playlist.id,
            "pitch_method": "email",
        },
        headers=auth_headers,
    )

    # Other user tries to read the pitches for the song — song doesn't belong to them
    r = client.get(f"/api/v1/songs/{sample_song.id}/pitches", headers=other_headers)
    assert r.status_code == 404


def test_cannot_update_another_users_pitch(db, client, sample_song, sample_playlist, auth_headers):
    """A second user cannot PATCH a pitch they don't own."""
    from app.models.user import User
    from app.utils.auth import create_access_token, hash_password

    other_user = User(
        email="other2@example.com",
        hashed_password=hash_password("otherpass"),
        name="Other User 2",
    )
    db.add(other_user)
    db.flush()
    other_headers = {"Authorization": f"Bearer {create_access_token(other_user.id)}"}

    create_r = client.post(
        "/api/v1/pitches",
        json={
            "song_id": sample_song.id,
            "target_type": "playlist",
            "playlist_id": sample_playlist.id,
            "pitch_method": "email",
        },
        headers=auth_headers,
    )
    pitch_id = create_r.json()["id"]

    r = client.patch(
        f"/api/v1/pitches/{pitch_id}",
        json={"status": "added"},
        headers=other_headers,
    )
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Response shape
# ---------------------------------------------------------------------------

def test_pitch_response_includes_target_name(client, auth_headers, sample_song, sample_playlist):
    """PitchResponse must include target_name populated from the playlist."""
    r = client.post(
        "/api/v1/pitches",
        json={
            "song_id": sample_song.id,
            "target_type": "playlist",
            "playlist_id": sample_playlist.id,
            "pitch_method": "email",
        },
        headers=auth_headers,
    )
    assert r.status_code == 201
    data = r.json()
    assert "target_name" in data
    assert data["target_name"] == sample_playlist.name
