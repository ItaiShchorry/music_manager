"""US-011: View music health at a glance (dashboard health endpoint)."""
import pytest

# ---------------------------------------------------------------------------
# US-011 cases
# ---------------------------------------------------------------------------
# 1. GET /dashboard/health-score — happy path, returns score + metrics
# 2. No snapshot yet → 404
# 3. Returns the most recent snapshot when multiple exist
# 4. Health score 85-100 → label "Excellent"
# 5. Health score 70-84 → label "Healthy"
# 6. Health score 50-69 → label "Needs Work"
# 7. Health score <50 → label "Critical"
# 8. Auth required
# ---------------------------------------------------------------------------


def _make_snapshot(client, auth_headers, streams_trend=25.0, save_rate_pct=10.0,
                   conversion_pct=8.0, playlist_adds=4, cost_per_stream=None):
    """Helper — posts a snapshot with precalculated save_rate baked in via raw streams/saves."""
    # We control save_rate via total_saves / total_streams
    total_streams = 1000
    total_saves = int(total_streams * save_rate_pct / 100)
    total_listeners = 500
    total_followers = int(total_listeners * conversion_pct / 100)
    payload = {
        "total_streams": total_streams,
        "total_monthly_listeners": total_listeners,
        "total_followers": total_followers,
        "total_saves": total_saves,
        "total_playlist_adds": playlist_adds,
        "streams_vs_last_week_pct": streams_trend,
        "listeners_vs_last_week_pct": 10.0,
        "followers_vs_last_week_pct": 5.0,
    }
    if cost_per_stream is not None:
        payload["cost_per_stream"] = cost_per_stream
    return client.post("/api/v1/dashboard/snapshots", json=payload, headers=auth_headers)


def test_get_health_score_happy_path(client, auth_headers):
    _make_snapshot(client, auth_headers)
    r = client.get("/api/v1/dashboard/health-score", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert "health_score" in data
    assert "label" in data
    assert "metrics" in data
    metrics = data["metrics"]
    assert "total_streams" in metrics
    assert "total_monthly_listeners" in metrics
    assert "total_followers" in metrics
    assert "save_rate" in metrics
    assert "follower_conversion_rate" in metrics
    assert "streams_vs_last_week_pct" in metrics


def test_get_health_score_no_snapshot(client, auth_headers):
    r = client.get("/api/v1/dashboard/health-score", headers=auth_headers)
    assert r.status_code == 404


def test_get_health_score_returns_latest(client, auth_headers, db):
    """When multiple snapshots exist, the latest date wins."""
    from datetime import date, timedelta
    from app.models.dashboard import DashboardSnapshot

    # Create today's snapshot via API
    _make_snapshot(client, auth_headers, streams_trend=5.0)

    # Manually insert an older snapshot using the test session
    old = DashboardSnapshot(
        user_id=1,
        snapshot_date=date.today() - timedelta(days=7),
        total_streams=100,
        total_monthly_listeners=50,
        total_followers=2,
        total_saves=2,
        total_playlist_adds=0,
        save_rate=2.0,
        follower_conversion_rate=4.0,
        health_score=30,
        streams_vs_last_week_pct=-20.0,
        listeners_vs_last_week_pct=-10.0,
        followers_vs_last_week_pct=-5.0,
    )
    db.add(old)
    db.flush()

    r = client.get("/api/v1/dashboard/health-score", headers=auth_headers)
    assert r.status_code == 200
    # Should reflect today's (better) snapshot, not the old one
    assert r.json()["metrics"]["total_streams"] == 1000


def test_health_score_label_excellent(client, auth_headers):
    # streams_trend=25% (+100 pts), save_rate=15% (100 pts), conversion=10% (100 pts),
    # playlist_adds=5 (100 pts) → high score
    _make_snapshot(client, auth_headers, streams_trend=25.0, save_rate_pct=15.0,
                   conversion_pct=10.0, playlist_adds=5)
    r = client.get("/api/v1/dashboard/health-score", headers=auth_headers)
    data = r.json()
    assert data["health_score"] >= 85
    assert data["label"] == "Excellent"


def test_health_score_label_healthy(client, auth_headers):
    # streams_trend=15%, save_rate=8%, conversion=6%, playlist_adds=3 → mid-high
    _make_snapshot(client, auth_headers, streams_trend=15.0, save_rate_pct=8.0,
                   conversion_pct=6.0, playlist_adds=3)
    r = client.get("/api/v1/dashboard/health-score", headers=auth_headers)
    data = r.json()
    assert 70 <= data["health_score"] <= 84
    assert data["label"] == "Healthy"


def test_health_score_label_needs_work(client, auth_headers):
    # streams_trend=5% → 60pts, save_rate=4.5% → 50pts, conversion=4% → 50pts,
    # playlist_adds=1 → 60pts, no roi → 60pts
    # weighted: 18 + 12.5 + 10 + 9 + 6 = 55.5 → rounds to 56 → "Needs Work"
    _make_snapshot(client, auth_headers, streams_trend=5.0, save_rate_pct=4.5,
                   conversion_pct=4.0, playlist_adds=1)
    r = client.get("/api/v1/dashboard/health-score", headers=auth_headers)
    data = r.json()
    assert 50 <= data["health_score"] <= 69
    assert data["label"] == "Needs Work"


def test_get_health_score_requires_auth(client):
    r = client.get("/api/v1/dashboard/health-score")
    assert r.status_code == 401
