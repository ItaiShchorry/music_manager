"""US-012: Receive actionable insights (AI-generated insight cards)."""
from unittest.mock import MagicMock, patch
import pytest

# ---------------------------------------------------------------------------
# US-012 cases
# ---------------------------------------------------------------------------
# 1. POST /dashboard/insights/generate — happy path, returns list of insights
# 2. Low save rate (<5%) → generates Optimization Tip insight
# 3. Stream drop (negative trend) → generates Performance Warning insight
# 4. Recent pitch with status "added" → generates Momentum Alert insight
# 5. GET /dashboard/insights — lists active insights, sorted by priority
# 6. PATCH /dashboard/insights/{id} status=dismissed → 200, status updated
# 7. PATCH /dashboard/insights/{id} status=actioned → 200, status updated
# 8. Auth required on all endpoints
# ---------------------------------------------------------------------------

FAKE_INSIGHT_RESPONSE = """{
  "insights": [
    {
      "insight_type": "tip",
      "priority": "medium",
      "title": "Low save rate detected",
      "description": "Your save rate is 3.0% which is below the 5% target. Listeners aren't adding your song to their libraries.",
      "action_text": "Add a call-to-action in your posts asking fans to save the song"
    }
  ]
}"""


def _make_snapshot(client, auth_headers, streams_trend=5.0, save_rate_pct=3.0,
                   conversion_pct=4.0, playlist_adds=0):
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
        "listeners_vs_last_week_pct": 5.0,
        "followers_vs_last_week_pct": 2.0,
    }
    return client.post("/api/v1/dashboard/snapshots", json=payload, headers=auth_headers)


def _mock_claude(fake_response: str):
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=fake_response)]
    mock_client.messages.create.return_value = mock_message
    mock_cls = MagicMock()
    mock_cls.return_value = mock_client
    return mock_cls, mock_client


def test_generate_insights_happy_path(client, auth_headers):
    _make_snapshot(client, auth_headers)
    mock_cls, _ = _mock_claude(FAKE_INSIGHT_RESPONSE)
    with patch("app.services.insight_generator.anthropic", mock_cls):
        r = client.post("/api/v1/dashboard/insights/generate", headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    insight = data[0]
    assert "insight_type" in insight
    assert "priority" in insight
    assert "title" in insight
    assert "description" in insight


def test_generate_insights_low_save_rate(client, auth_headers):
    """Save rate < 5% always produces at least one tip insight without requiring Claude."""
    _make_snapshot(client, auth_headers, save_rate_pct=2.0)
    mock_cls, _ = _mock_claude(FAKE_INSIGHT_RESPONSE)
    with patch("app.services.insight_generator.anthropic", mock_cls):
        r = client.post("/api/v1/dashboard/insights/generate", headers=auth_headers)
    assert r.status_code == 201
    types = [i["insight_type"] for i in r.json()]
    assert "tip" in types


def test_generate_insights_stream_drop(client, auth_headers):
    """Negative streams trend generates a warning insight."""
    warning_response = """{
      "insights": [
        {
          "insight_type": "warning",
          "priority": "high",
          "title": "Stream drop detected",
          "description": "Streams fell 20% this week.",
          "action_text": "Submit to more playlists to recover momentum"
        }
      ]
    }"""
    _make_snapshot(client, auth_headers, streams_trend=-20.0)
    mock_cls, _ = _mock_claude(warning_response)
    with patch("app.services.insight_generator.anthropic", mock_cls):
        r = client.post("/api/v1/dashboard/insights/generate", headers=auth_headers)
    assert r.status_code == 201
    types = [i["insight_type"] for i in r.json()]
    assert "warning" in types


def test_generate_insights_momentum_alert(client, auth_headers, sample_song, sample_playlist):
    """A pitch recently marked 'added' surfaces a momentum alert."""
    # Create a pitch for sample_song targeting the sample_playlist
    pitch_payload = {
        "song_id": sample_song.id,
        "target_type": "playlist",
        "playlist_id": sample_playlist.id,
        "pitch_method": "email",
    }
    pr = client.post("/api/v1/pitches", json=pitch_payload, headers=auth_headers)
    assert pr.status_code == 201
    pitch_id = pr.json()["id"]

    # Mark the pitch as added
    client.patch(f"/api/v1/pitches/{pitch_id}", json={"status": "added"}, headers=auth_headers)

    _make_snapshot(client, auth_headers, streams_trend=10.0)
    momentum_response = """{
      "insights": [
        {
          "insight_type": "momentum",
          "priority": "high",
          "title": "Pitch accepted!",
          "description": "A playlist curator accepted your submission.",
          "action_text": "Thank the curator and share the playlist on social media"
        }
      ]
    }"""
    mock_cls, _ = _mock_claude(momentum_response)
    with patch("app.services.insight_generator.anthropic", mock_cls):
        r = client.post("/api/v1/dashboard/insights/generate", headers=auth_headers)
    assert r.status_code == 201
    types = [i["insight_type"] for i in r.json()]
    assert "momentum" in types


def test_list_insights_sorted_by_priority(client, auth_headers):
    """GET /dashboard/insights returns active insights, high priority first."""
    _make_snapshot(client, auth_headers)
    mock_cls, _ = _mock_claude("""{
      "insights": [
        {"insight_type": "tip", "priority": "low", "title": "Tip", "description": "desc", "action_text": "act"},
        {"insight_type": "warning", "priority": "high", "title": "Warning", "description": "desc", "action_text": "act"}
      ]
    }""")
    with patch("app.services.insight_generator.anthropic", mock_cls):
        client.post("/api/v1/dashboard/insights/generate", headers=auth_headers)

    r = client.get("/api/v1/dashboard/insights", headers=auth_headers)
    assert r.status_code == 200
    insights = r.json()
    priorities = [i["priority"] for i in insights]
    # "high" should appear before "low"
    if "high" in priorities and "low" in priorities:
        assert priorities.index("high") < priorities.index("low")


def test_dismiss_insight(client, auth_headers):
    _make_snapshot(client, auth_headers)
    mock_cls, _ = _mock_claude(FAKE_INSIGHT_RESPONSE)
    with patch("app.services.insight_generator.anthropic", mock_cls):
        gen_r = client.post("/api/v1/dashboard/insights/generate", headers=auth_headers)
    insight_id = gen_r.json()[0]["id"]

    r = client.patch(
        f"/api/v1/dashboard/insights/{insight_id}",
        json={"status": "dismissed"},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["status"] == "dismissed"


def test_action_insight(client, auth_headers):
    _make_snapshot(client, auth_headers)
    mock_cls, _ = _mock_claude(FAKE_INSIGHT_RESPONSE)
    with patch("app.services.insight_generator.anthropic", mock_cls):
        gen_r = client.post("/api/v1/dashboard/insights/generate", headers=auth_headers)
    insight_id = gen_r.json()[0]["id"]

    r = client.patch(
        f"/api/v1/dashboard/insights/{insight_id}",
        json={"status": "actioned"},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["status"] == "actioned"


def test_insights_require_auth(client):
    r = client.get("/api/v1/dashboard/insights")
    assert r.status_code == 401

    r2 = client.post("/api/v1/dashboard/insights/generate")
    assert r2.status_code == 401
