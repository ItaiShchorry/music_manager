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
