"""
US-011: SubmitHub campaign planning + submission tracking.
  POST /submithub-campaigns           — create a SubmitHub campaign for a song
  GET  /songs/{id}/submithub          — list SubmitHub campaigns for a song
  POST /submithub-campaigns/{id}/submissions — add a submission entry
  PATCH /submithub-submissions/{id}   — update submission result

TDD: tests written FIRST.
"""
from datetime import date

import pytest

from app.models.song import Song


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _song(db, sample_user, track_id="sh_test_song"):
    song = Song(
        user_id=sample_user.id,
        spotify_track_id=track_id,
        title="SH Test Song",
        artist_name="Test Artist",
        release_date=date(2024, 6, 1),
        genre="indie pop",
        language="hebrew",
    )
    db.add(song)
    db.flush()
    return song


# ---------------------------------------------------------------------------
# SubmitHub Campaign
# ---------------------------------------------------------------------------

def test_create_submithub_campaign_happy_path(client, db, sample_user, auth_headers):
    """Create a SubmitHub campaign for a song → 201."""
    song = _song(db, sample_user)

    r = client.post(
        "/api/v1/submithub-campaigns",
        json={
            "song_id": song.id,
            "budget_allocated": 36.0,
            "curator_count": 12,
        },
        headers=auth_headers,
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["song_id"] == song.id
    assert data["budget_allocated"] == 36.0
    assert data["curator_count"] == 12
    assert data["status"] == "active"
    assert data["campaign_code"].startswith("SH-")
    assert "id" in data


def test_create_submithub_campaign_linked_to_campaign(client, db, sample_user, auth_headers):
    """SubmitHub campaign can optionally be linked to a main campaign."""
    song = _song(db, sample_user)

    # Create a main campaign first
    camp = client.post(
        "/api/v1/campaigns",
        json={"name": "EP Push", "release_type": "ep",
              "start_date": "2026-03-01", "end_date": "2026-04-01",
              "budget_total": 500.0},
        headers=auth_headers,
    ).json()

    r = client.post(
        "/api/v1/submithub-campaigns",
        json={"song_id": song.id, "budget_allocated": 36.0,
              "campaign_id": camp["id"]},
        headers=auth_headers,
    )
    assert r.status_code == 201, r.text
    assert r.json()["campaign_id"] == camp["id"]


def test_create_submithub_campaign_song_not_found(client, auth_headers):
    """Song not owned by user → 404."""
    r = client.post(
        "/api/v1/submithub-campaigns",
        json={"song_id": 99999},
        headers=auth_headers,
    )
    assert r.status_code == 404


def test_list_submithub_campaigns_for_song(client, db, sample_user, auth_headers):
    """GET /songs/{id}/submithub → 200, list of SubmitHub campaigns."""
    song = _song(db, sample_user)

    # Create two campaigns for this song
    for budget in (36.0, 45.0):
        client.post(
            "/api/v1/submithub-campaigns",
            json={"song_id": song.id, "budget_allocated": budget},
            headers=auth_headers,
        )

    r = client.get(f"/api/v1/songs/{song.id}/submithub", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2


def test_list_submithub_campaigns_empty(client, db, sample_user, auth_headers):
    """Song with no SubmitHub campaigns → empty list."""
    song = _song(db, sample_user)
    r = client.get(f"/api/v1/songs/{song.id}/submithub", headers=auth_headers)
    assert r.status_code == 200
    assert r.json() == []


def test_create_submithub_campaign_requires_auth(client):
    r = client.post("/api/v1/submithub-campaigns", json={"song_id": 1})
    assert r.status_code == 401


# ---------------------------------------------------------------------------
# SubmitHub Submissions
# ---------------------------------------------------------------------------

def test_add_submission_happy_path(client, db, sample_user, auth_headers):
    """Add a submission to a SubmitHub campaign → 201."""
    song = _song(db, sample_user)
    sh_camp = client.post(
        "/api/v1/submithub-campaigns",
        json={"song_id": song.id, "budget_allocated": 36.0},
        headers=auth_headers,
    ).json()

    r = client.post(
        f"/api/v1/submithub-campaigns/{sh_camp['id']}/submissions",
        json={
            "curator_name": "IndieRockPlaylist",
            "curator_genre_focus": ["indie rock", "alternative"],
            "curator_approval_rate": 20.0,
            "submission_date": "2026-03-10",
            "cost": 3.0,
        },
        headers=auth_headers,
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["curator_name"] == "IndieRockPlaylist"
    assert data["response_status"] == "pending"
    assert data["cost"] == 3.0


def test_list_submissions_for_campaign(client, db, sample_user, auth_headers):
    """GET /submithub-campaigns/{id}/submissions → list."""
    song = _song(db, sample_user)
    sh_camp = client.post(
        "/api/v1/submithub-campaigns",
        json={"song_id": song.id},
        headers=auth_headers,
    ).json()

    for name in ("Curator A", "Curator B", "Curator C"):
        client.post(
            f"/api/v1/submithub-campaigns/{sh_camp['id']}/submissions",
            json={"curator_name": name, "cost": 3.0},
            headers=auth_headers,
        )

    r = client.get(f"/api/v1/submithub-campaigns/{sh_camp['id']}/submissions",
                   headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 3


def test_update_submission_status_approved(client, db, sample_user, auth_headers):
    """PATCH submission → update status to approved, add playlist URL."""
    song = _song(db, sample_user)
    sh_camp = client.post(
        "/api/v1/submithub-campaigns",
        json={"song_id": song.id},
        headers=auth_headers,
    ).json()

    sub = client.post(
        f"/api/v1/submithub-campaigns/{sh_camp['id']}/submissions",
        json={"curator_name": "AcousticVibes", "cost": 3.0},
        headers=auth_headers,
    ).json()

    r = client.patch(
        f"/api/v1/submithub-submissions/{sub['id']}",
        json={
            "response_status": "approved",
            "response_date": "2026-03-12",
            "playlist_added": True,
            "playlist_url": "https://open.spotify.com/playlist/abc",
        },
        headers=auth_headers,
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["response_status"] == "approved"
    assert data["playlist_added"] is True


def test_update_submission_with_feedback(client, db, sample_user, auth_headers):
    """PATCH submission → declined with curator feedback."""
    song = _song(db, sample_user)
    sh_camp = client.post(
        "/api/v1/submithub-campaigns",
        json={"song_id": song.id},
        headers=auth_headers,
    ).json()

    sub = client.post(
        f"/api/v1/submithub-campaigns/{sh_camp['id']}/submissions",
        json={"curator_name": "IndieRock", "cost": 3.0},
        headers=auth_headers,
    ).json()

    r = client.patch(
        f"/api/v1/submithub-submissions/{sub['id']}",
        json={
            "response_status": "declined",
            "curator_feedback": "Great song but doesn't fit our current direction.",
        },
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["curator_feedback"] == "Great song but doesn't fit our current direction."


def test_update_submission_invalid_status(client, db, sample_user, auth_headers):
    """Invalid response_status → 422."""
    song = _song(db, sample_user)
    sh_camp = client.post(
        "/api/v1/submithub-campaigns",
        json={"song_id": song.id},
        headers=auth_headers,
    ).json()

    sub = client.post(
        f"/api/v1/submithub-campaigns/{sh_camp['id']}/submissions",
        json={"curator_name": "Test", "cost": 3.0},
        headers=auth_headers,
    ).json()

    r = client.patch(
        f"/api/v1/submithub-submissions/{sub['id']}",
        json={"response_status": "maybe"},
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_submithub_submission_requires_auth(client):
    r = client.post("/api/v1/submithub-campaigns/1/submissions",
                    json={"curator_name": "X"})
    assert r.status_code == 401
