"""
US-008: Campaign CRUD — create / list / get / update / delete.
US-009: AI budget recommendation — POST /campaigns/{id}/budget-recommendation.
US-010: Expense tracking — POST/GET /campaigns/{id}/expenses, PATCH /expenses/{id}.

TDD: tests written FIRST. Budget recommendation calls are mocked — no real API calls.
"""
import json
from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from app.models.song import Song


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _song(db, sample_user):
    song = Song(
        user_id=sample_user.id,
        spotify_track_id="camp_test_song_abc",
        title="Test Song",
        artist_name="Test Artist",
        release_date=date(2024, 1, 1),
        genre="indie pop",
        language="hebrew",
    )
    db.add(song)
    db.flush()
    return song


FAKE_BUDGET_RESPONSE = {
    "playlist_pitching": {"amount": 180, "pct": 60, "rationale": "Best ROI at emerging tier"},
    "submithub": {"amount": 30, "pct": 10, "rationale": "Guaranteed responses, good targeting"},
    "social_ads": {"amount": 60, "pct": 20, "rationale": "Instagram > Facebook for your genre"},
    "content_creation": {"amount": 20, "pct": 7, "rationale": "Acoustic session video"},
    "radio_promotion": {"amount": 5, "pct": 2, "rationale": "Kan 88 email submission"},
    "other": {"amount": 5, "pct": 1, "rationale": "Miscellaneous"},
    "top_tip": "Focus on playlist pitching — it gives the best streams-per-dollar at your stage.",
}


def _make_mock_anthropic():
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(text=json.dumps(FAKE_BUDGET_RESPONSE))]
    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_msg
    mock_cls = MagicMock(return_value=mock_client)
    return mock_cls, mock_client


# ---------------------------------------------------------------------------
# Campaign CRUD
# ---------------------------------------------------------------------------

def test_create_campaign_happy_path(client, db, sample_user, auth_headers):
    """Create a basic campaign → 201 with id."""
    r = client.post(
        "/api/v1/campaigns",
        json={
            "name": "Spring Single Push",
            "release_type": "single",
            "start_date": "2026-03-01",
            "end_date": "2026-04-15",
            "budget_total": 300.0,
            "primary_goal": "awareness",
        },
        headers=auth_headers,
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["name"] == "Spring Single Push"
    assert data["release_type"] == "single"
    assert data["budget_total"] == 300.0
    assert data["budget_spent"] == 0.0
    assert data["status"] == "planning"
    assert "id" in data
    assert "created_at" in data


def test_create_campaign_with_songs(client, db, sample_user, auth_headers):
    """Create a campaign and attach songs → 201, songs listed."""
    song = _song(db, sample_user)

    r = client.post(
        "/api/v1/campaigns",
        json={
            "name": "EP Campaign",
            "release_type": "ep",
            "start_date": "2026-03-01",
            "end_date": "2026-04-30",
            "budget_total": 500.0,
            "primary_goal": "growth",
            "song_ids": [song.id],
        },
        headers=auth_headers,
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert len(data["songs"]) == 1
    assert data["songs"][0]["id"] == song.id


def test_create_campaign_invalid_release_type(client, auth_headers):
    """Invalid release_type → 422."""
    r = client.post(
        "/api/v1/campaigns",
        json={
            "name": "Bad Type",
            "release_type": "mixtape",
            "start_date": "2026-03-01",
            "end_date": "2026-04-01",
            "budget_total": 100.0,
        },
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_create_campaign_requires_auth(client):
    """Unauthenticated → 401."""
    r = client.post(
        "/api/v1/campaigns",
        json={"name": "X", "release_type": "single", "start_date": "2026-03-01",
              "end_date": "2026-04-01", "budget_total": 100.0},
    )
    assert r.status_code == 401


def test_list_campaigns_empty(client, auth_headers):
    """No campaigns → empty list."""
    r = client.get("/api/v1/campaigns", headers=auth_headers)
    assert r.status_code == 200
    assert r.json() == []


def test_list_campaigns_after_create(client, auth_headers):
    """Creates two campaigns → list returns both."""
    for name in ("Campaign A", "Campaign B"):
        client.post(
            "/api/v1/campaigns",
            json={"name": name, "release_type": "single",
                  "start_date": "2026-03-01", "end_date": "2026-04-01",
                  "budget_total": 100.0},
            headers=auth_headers,
        )
    r = client.get("/api/v1/campaigns", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_get_campaign(client, auth_headers):
    """Get specific campaign → 200, full detail."""
    create = client.post(
        "/api/v1/campaigns",
        json={"name": "Single Push", "release_type": "single",
              "start_date": "2026-03-01", "end_date": "2026-04-01",
              "budget_total": 200.0},
        headers=auth_headers,
    )
    cid = create.json()["id"]
    r = client.get(f"/api/v1/campaigns/{cid}", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["id"] == cid


def test_get_campaign_not_found(client, auth_headers):
    """Unknown id → 404."""
    r = client.get("/api/v1/campaigns/99999", headers=auth_headers)
    assert r.status_code == 404


def test_update_campaign_status(client, auth_headers):
    """PATCH status from planning → active → 200."""
    create = client.post(
        "/api/v1/campaigns",
        json={"name": "Single Push", "release_type": "single",
              "start_date": "2026-03-01", "end_date": "2026-04-01",
              "budget_total": 200.0},
        headers=auth_headers,
    )
    cid = create.json()["id"]
    r = client.patch(
        f"/api/v1/campaigns/{cid}",
        json={"status": "active"},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["status"] == "active"


def test_delete_campaign(client, auth_headers):
    """DELETE campaign → 204, then 404 on GET."""
    create = client.post(
        "/api/v1/campaigns",
        json={"name": "Delete Me", "release_type": "single",
              "start_date": "2026-03-01", "end_date": "2026-04-01",
              "budget_total": 100.0},
        headers=auth_headers,
    )
    cid = create.json()["id"]
    r = client.delete(f"/api/v1/campaigns/{cid}", headers=auth_headers)
    assert r.status_code == 204
    assert client.get(f"/api/v1/campaigns/{cid}", headers=auth_headers).status_code == 404


# ---------------------------------------------------------------------------
# Budget Recommendation (US-009)
# ---------------------------------------------------------------------------

def test_budget_recommendation_happy_path(client, db, sample_user, auth_headers):
    """POST /campaigns/{id}/budget-recommendation → 200, structured allocation."""
    song = _song(db, sample_user)
    create = client.post(
        "/api/v1/campaigns",
        json={"name": "Test", "release_type": "single",
              "start_date": "2026-03-01", "end_date": "2026-04-01",
              "budget_total": 300.0, "song_ids": [song.id]},
        headers=auth_headers,
    )
    cid = create.json()["id"]
    mock_cls, mock_client = _make_mock_anthropic()

    with patch("app.services.budget_recommender.anthropic", mock_cls) as patched:
        patched.Anthropic.return_value = mock_client
        r = client.post(f"/api/v1/campaigns/{cid}/budget-recommendation",
                        headers=auth_headers)

    assert r.status_code == 200, r.text
    data = r.json()
    assert "playlist_pitching" in data
    assert "submithub" in data
    assert "social_ads" in data
    assert "top_tip" in data
    assert data["playlist_pitching"]["amount"] == 180


def test_budget_recommendation_stored_on_campaign(client, db, sample_user, auth_headers):
    """After generating recommendation, GET campaign shows budget_recommendation populated."""
    song = _song(db, sample_user)
    create = client.post(
        "/api/v1/campaigns",
        json={"name": "Test", "release_type": "single",
              "start_date": "2026-03-01", "end_date": "2026-04-01",
              "budget_total": 300.0, "song_ids": [song.id]},
        headers=auth_headers,
    )
    cid = create.json()["id"]
    mock_cls, mock_client = _make_mock_anthropic()

    with patch("app.services.budget_recommender.anthropic", mock_cls) as patched:
        patched.Anthropic.return_value = mock_client
        client.post(f"/api/v1/campaigns/{cid}/budget-recommendation",
                    headers=auth_headers)

    campaign = client.get(f"/api/v1/campaigns/{cid}", headers=auth_headers).json()
    assert campaign["budget_recommendation"] is not None
    assert campaign["budget_recommendation"]["playlist_pitching"]["amount"] == 180


def test_budget_recommendation_not_found(client, auth_headers):
    """Unknown campaign → 404."""
    mock_cls, mock_client = _make_mock_anthropic()
    with patch("app.services.budget_recommender.anthropic", mock_cls) as patched:
        patched.Anthropic.return_value = mock_client
        r = client.post("/api/v1/campaigns/99999/budget-recommendation",
                        headers=auth_headers)
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Expense Tracking (US-010)
# ---------------------------------------------------------------------------

def test_add_expense_happy_path(client, auth_headers):
    """POST /campaigns/{id}/expenses → 201, expense returned."""
    create = client.post(
        "/api/v1/campaigns",
        json={"name": "EP Push", "release_type": "ep",
              "start_date": "2026-03-01", "end_date": "2026-04-01",
              "budget_total": 500.0},
        headers=auth_headers,
    )
    cid = create.json()["id"]

    r = client.post(
        f"/api/v1/campaigns/{cid}/expenses",
        json={
            "expense_date": "2026-03-05",
            "amount": 36.0,
            "category": "playlist_pitching",
            "subcategory": "submithub",
            "description": "SubmitHub 12 credits",
        },
        headers=auth_headers,
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["amount"] == 36.0
    assert data["category"] == "playlist_pitching"
    assert data["campaign_id"] == cid


def test_expense_updates_budget_spent(client, auth_headers):
    """Adding expenses accumulates budget_spent on the campaign."""
    create = client.post(
        "/api/v1/campaigns",
        json={"name": "EP Push", "release_type": "ep",
              "start_date": "2026-03-01", "end_date": "2026-04-01",
              "budget_total": 500.0},
        headers=auth_headers,
    )
    cid = create.json()["id"]

    for amount in (36.0, 25.0, 50.0):
        client.post(
            f"/api/v1/campaigns/{cid}/expenses",
            json={"expense_date": "2026-03-05", "amount": amount,
                  "category": "social_ads"},
            headers=auth_headers,
        )

    campaign = client.get(f"/api/v1/campaigns/{cid}", headers=auth_headers).json()
    assert campaign["budget_spent"] == 111.0


def test_list_expenses(client, auth_headers):
    """GET /campaigns/{id}/expenses → 200, list of expenses."""
    create = client.post(
        "/api/v1/campaigns",
        json={"name": "Test", "release_type": "single",
              "start_date": "2026-03-01", "end_date": "2026-04-01",
              "budget_total": 200.0},
        headers=auth_headers,
    )
    cid = create.json()["id"]

    for i in range(3):
        client.post(
            f"/api/v1/campaigns/{cid}/expenses",
            json={"expense_date": "2026-03-05", "amount": 10.0,
                  "category": "content"},
            headers=auth_headers,
        )

    r = client.get(f"/api/v1/campaigns/{cid}/expenses", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 3


def test_expense_invalid_category(client, auth_headers):
    """Invalid category → 422."""
    create = client.post(
        "/api/v1/campaigns",
        json={"name": "Test", "release_type": "single",
              "start_date": "2026-03-01", "end_date": "2026-04-01",
              "budget_total": 200.0},
        headers=auth_headers,
    )
    cid = create.json()["id"]
    r = client.post(
        f"/api/v1/campaigns/{cid}/expenses",
        json={"expense_date": "2026-03-05", "amount": 10.0,
              "category": "bad_category"},
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_expense_requires_auth(client):
    """No token → 401."""
    r = client.post("/api/v1/campaigns/1/expenses",
                    json={"expense_date": "2026-03-05", "amount": 10.0,
                          "category": "content"})
    assert r.status_code == 401
