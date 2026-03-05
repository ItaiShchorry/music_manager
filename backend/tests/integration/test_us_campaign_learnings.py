"""
Campaign Apply Learnings

POST /campaigns/{id}/apply-learnings
Analyzes actual channel spend vs planned allocation and returns
Claude-generated insights and recommendations for the next campaign.
"""
from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from app.models.campaign import Campaign, Expense


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MOCK_BUDGET_REC = {
    "playlist_pitching": {"amount": 60.0, "pct": 60, "rationale": "Best ROI"},
    "submithub": {"amount": 30.0, "pct": 30, "rationale": "Curator responses"},
    "social_ads": {"amount": 10.0, "pct": 10, "rationale": "Ads"},
    "content_creation": {"amount": 0.0, "pct": 0, "rationale": ""},
    "radio_promotion": {"amount": 0.0, "pct": 0, "rationale": ""},
    "other": {"amount": 0.0, "pct": 0, "rationale": ""},
    "top_tip": "Focus on playlisting.",
}

MOCK_LEARNINGS_JSON = """{
  "summary": "The campaign delivered solid ROI on SubmitHub but overspent on social ads.",
  "channel_insights": [
    {
      "channel": "playlist_pitching",
      "planned": 60.0,
      "actual": 55.0,
      "verdict": "on_track",
      "recommendation": "Continue allocating 60% to playlist pitching."
    },
    {
      "channel": "submithub",
      "planned": 30.0,
      "actual": 45.0,
      "verdict": "over_budget",
      "recommendation": "Cap SubmitHub at planned allocation next time."
    }
  ],
  "next_campaign_suggestions": [
    "Allocate more to playlist pitching based on strong conversion.",
    "Reduce SubmitHub budget to planned amount.",
    "Try Kan 88 radio outreach — not yet tested."
  ]
}"""


def _mock_claude(json_text: str = MOCK_LEARNINGS_JSON):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=json_text)]
    )
    return mock_client


def _create_campaign(db, sample_user, with_rec: bool = True) -> Campaign:
    c = Campaign(
        user_id=sample_user.id,
        name="Test Campaign",
        release_type="single",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 2, 28),
        budget_total=Decimal("100.00"),
        status="completed",
        budget_recommendation=MOCK_BUDGET_REC if with_rec else None,
    )
    db.add(c)
    db.flush()
    return c


def _add_expense(db, campaign_id: int, user_id: int, category: str, amount: float) -> Expense:
    e = Expense(
        campaign_id=campaign_id,
        user_id=user_id,
        expense_date=date(2026, 1, 15),
        amount=Decimal(str(amount)),
        category=category,
    )
    db.add(e)
    db.flush()
    return e


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestApplyLearnings:
    def test_happy_path(self, client, auth_headers, db, sample_user):
        """POST /apply-learnings → 200 with summary, channel_insights, suggestions."""
        c = _create_campaign(db, sample_user)
        _add_expense(db, c.id, sample_user.id, "playlist_pitching", 55.0)
        _add_expense(db, c.id, sample_user.id, "submithub", 45.0)

        with patch("app.services.learnings_generator.anthropic") as patched:
            patched.Anthropic.return_value = _mock_claude()
            resp = client.post(
                f"/api/v1/campaigns/{c.id}/apply-learnings",
                headers=auth_headers,
            )

        assert resp.status_code == 200
        data = resp.json()
        assert "summary" in data
        assert len(data["summary"]) > 10
        assert "channel_insights" in data
        assert isinstance(data["channel_insights"], list)
        assert "next_campaign_suggestions" in data
        assert isinstance(data["next_campaign_suggestions"], list)
        assert len(data["next_campaign_suggestions"]) > 0

    def test_no_budget_recommendation(self, client, auth_headers, db, sample_user):
        """Works even when no budget_recommendation was generated."""
        c = _create_campaign(db, sample_user, with_rec=False)
        _add_expense(db, c.id, sample_user.id, "social_ads", 30.0)

        with patch("app.services.learnings_generator.anthropic") as patched:
            patched.Anthropic.return_value = _mock_claude()
            resp = client.post(
                f"/api/v1/campaigns/{c.id}/apply-learnings",
                headers=auth_headers,
            )

        assert resp.status_code == 200
        data = resp.json()
        assert "summary" in data

    def test_claude_error_returns_fallback(self, client, auth_headers, db, sample_user):
        """When Claude fails, a rule-based fallback is returned."""
        c = _create_campaign(db, sample_user)
        _add_expense(db, c.id, sample_user.id, "submithub", 80.0)

        with patch("app.services.learnings_generator.anthropic") as patched:
            mock_client = MagicMock()
            mock_client.messages.create.side_effect = Exception("Claude down")
            patched.Anthropic.return_value = mock_client
            resp = client.post(
                f"/api/v1/campaigns/{c.id}/apply-learnings",
                headers=auth_headers,
            )

        assert resp.status_code == 200
        data = resp.json()
        assert "summary" in data
        assert len(data["summary"]) > 5

    def test_campaign_not_found(self, client, auth_headers):
        """Unknown campaign ID → 404."""
        resp = client.post(
            "/api/v1/campaigns/99999/apply-learnings",
            headers=auth_headers,
        )
        assert resp.status_code == 404

    def test_auth_required(self, client, db, sample_user):
        """No token → 401."""
        c = _create_campaign(db, sample_user)
        resp = client.post(f"/api/v1/campaigns/{c.id}/apply-learnings")
        assert resp.status_code == 401
