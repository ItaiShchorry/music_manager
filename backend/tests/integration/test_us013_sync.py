"""US-013: Sync Spotify data (manual dashboard snapshot creation)."""
import pytest

# ---------------------------------------------------------------------------
# US-013 cases
# ---------------------------------------------------------------------------
# 1. POST /dashboard/snapshots — happy path, all fields, returns 201 + snapshot
# 2. Health score auto-calculated on create
# 3. Save rate auto-calculated (saves / streams * 100)
# 4. Follower conversion auto-calculated (followers / monthly_listeners * 100)
# 5. Second snapshot same day — returns 200 and updates the existing row
# 6. Auth required — no token → 401
# ---------------------------------------------------------------------------


def test_create_snapshot_happy_path(client, auth_headers):
    payload = {
        "total_streams": 1000,
        "total_monthly_listeners": 500,
        "total_followers": 50,
        "total_saves": 80,
        "total_playlist_adds": 3,
        "streams_vs_last_week_pct": 25.0,
        "listeners_vs_last_week_pct": 15.0,
        "followers_vs_last_week_pct": 10.0,
    }
    r = client.post("/api/v1/dashboard/snapshots", json=payload, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["total_streams"] == 1000
    assert data["total_monthly_listeners"] == 500
    assert data["total_followers"] == 50
    assert data["total_saves"] == 80
    assert data["total_playlist_adds"] == 3
    assert "snapshot_date" in data
    assert "health_score" in data


def test_create_snapshot_calculates_save_rate(client, auth_headers):
    payload = {
        "total_streams": 1000,
        "total_monthly_listeners": 500,
        "total_followers": 50,
        "total_saves": 80,
        "streams_vs_last_week_pct": 10.0,
        "listeners_vs_last_week_pct": 5.0,
        "followers_vs_last_week_pct": 5.0,
    }
    r = client.post("/api/v1/dashboard/snapshots", json=payload, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    # save_rate = (80 / 1000) * 100 = 8.0
    assert abs(data["save_rate"] - 8.0) < 0.1


def test_create_snapshot_calculates_follower_conversion(client, auth_headers):
    payload = {
        "total_streams": 1000,
        "total_monthly_listeners": 500,
        "total_followers": 50,
        "total_saves": 50,
        "streams_vs_last_week_pct": 5.0,
        "listeners_vs_last_week_pct": 5.0,
        "followers_vs_last_week_pct": 5.0,
    }
    r = client.post("/api/v1/dashboard/snapshots", json=payload, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    # follower_conversion = (50 / 500) * 100 = 10.0
    assert abs(data["follower_conversion_rate"] - 10.0) < 0.1


def test_create_snapshot_health_score_calculated(client, auth_headers):
    """Health score must be an integer between 0 and 100."""
    payload = {
        "total_streams": 2000,
        "total_monthly_listeners": 800,
        "total_followers": 80,
        "total_saves": 200,
        "total_playlist_adds": 4,
        "streams_vs_last_week_pct": 30.0,
        "listeners_vs_last_week_pct": 20.0,
        "followers_vs_last_week_pct": 10.0,
    }
    r = client.post("/api/v1/dashboard/snapshots", json=payload, headers=auth_headers)
    assert r.status_code == 201
    score = r.json()["health_score"]
    assert 0 <= score <= 100


def test_upsert_snapshot_same_day(client, auth_headers):
    """POSTing a second snapshot on the same day updates the existing one."""
    base = {
        "total_streams": 1000,
        "total_monthly_listeners": 500,
        "total_followers": 50,
        "total_saves": 50,
        "streams_vs_last_week_pct": 5.0,
        "listeners_vs_last_week_pct": 5.0,
        "followers_vs_last_week_pct": 5.0,
    }
    r1 = client.post("/api/v1/dashboard/snapshots", json=base, headers=auth_headers)
    assert r1.status_code == 201
    first_id = r1.json()["id"]

    updated = {**base, "total_streams": 1500}
    r2 = client.post("/api/v1/dashboard/snapshots", json=updated, headers=auth_headers)
    assert r2.status_code == 200  # updated, not created
    data = r2.json()
    assert data["id"] == first_id
    assert data["total_streams"] == 1500


def test_create_snapshot_requires_auth(client):
    payload = {
        "total_streams": 1000,
        "total_monthly_listeners": 500,
        "total_followers": 50,
        "total_saves": 50,
        "streams_vs_last_week_pct": 5.0,
        "listeners_vs_last_week_pct": 5.0,
        "followers_vs_last_week_pct": 5.0,
    }
    r = client.post("/api/v1/dashboard/snapshots", json=payload)
    assert r.status_code == 401
