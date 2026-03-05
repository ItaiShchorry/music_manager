"""
US-015: Opportunity History

Tests for updating opportunity status (used, dismissed, remind_later)
and verifying the active feed reflects those changes.
"""
import json
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from app.models.post_opportunity import PostOpportunity


# ---------------------------------------------------------------------------
# Helper: seed a direct PostOpportunity row (bypasses Claude)
# ---------------------------------------------------------------------------

def _create_opportunity(db, user_id: int, hook: str = "Test hook") -> PostOpportunity:
    opp = PostOpportunity(
        user_id=user_id,
        hook=hook,
        why_now="Test signal",
        signal_type="inactivity",
        suggested_platform="instagram",
        hashtag_suggestions=["#test"],
        timing_note="Post anytime",
        status="active",
    )
    db.add(opp)
    db.flush()
    return opp


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

class TestUpdateOpportunityStatus:
    def test_mark_as_used(self, client, auth_headers, db, sample_user):
        """PATCH status=used sets used_at and returns the updated record."""
        opp = _create_opportunity(db, sample_user.id)

        resp = client.patch(
            f"/api/v1/opportunities/{opp.id}",
            headers=auth_headers,
            json={"status": "used"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "used"
        assert data["used_at"] is not None

    def test_dismiss_opportunity(self, client, auth_headers, db, sample_user):
        """PATCH status=dismissed → 200, status updated."""
        opp = _create_opportunity(db, sample_user.id)

        resp = client.patch(
            f"/api/v1/opportunities/{opp.id}",
            headers=auth_headers,
            json={"status": "dismissed"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "dismissed"

    def test_remind_later(self, client, auth_headers, db, sample_user):
        """PATCH status=remind_later → 200."""
        opp = _create_opportunity(db, sample_user.id)

        resp = client.patch(
            f"/api/v1/opportunities/{opp.id}",
            headers=auth_headers,
            json={"status": "remind_later"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "remind_later"

    def test_invalid_status_rejected(self, client, auth_headers, db, sample_user):
        """PATCH with unknown status → 422."""
        opp = _create_opportunity(db, sample_user.id)

        resp = client.patch(
            f"/api/v1/opportunities/{opp.id}",
            headers=auth_headers,
            json={"status": "invalid_status"},
        )
        assert resp.status_code == 422

    def test_update_nonexistent_opportunity(self, client, auth_headers):
        """PATCH on unknown id → 404."""
        resp = client.patch(
            "/api/v1/opportunities/99999",
            headers=auth_headers,
            json={"status": "dismissed"},
        )
        assert resp.status_code == 404

    def test_auth_required_on_patch(self, client, db, sample_user):
        """PATCH without token → 401."""
        opp = _create_opportunity(db, sample_user.id)
        resp = client.patch(f"/api/v1/opportunities/{opp.id}", json={"status": "used"})
        assert resp.status_code == 401


class TestDismissedRemovedFromActiveFeed:
    def test_dismissed_not_in_active_list(self, client, auth_headers, db, sample_user):
        """Dismissed opportunities do not appear in GET /opportunities."""
        opp = _create_opportunity(db, sample_user.id, hook="I should be hidden after dismiss")

        # Dismiss it
        client.patch(
            f"/api/v1/opportunities/{opp.id}",
            headers=auth_headers,
            json={"status": "dismissed"},
        )

        # Should not appear in active list
        resp = client.get("/api/v1/opportunities", headers=auth_headers)
        assert resp.status_code == 200
        ids = [item["id"] for item in resp.json()]
        assert opp.id not in ids

    def test_used_not_in_active_list(self, client, auth_headers, db, sample_user):
        """Used opportunities do not appear in GET /opportunities."""
        opp = _create_opportunity(db, sample_user.id, hook="I should be hidden after use")

        client.patch(
            f"/api/v1/opportunities/{opp.id}",
            headers=auth_headers,
            json={"status": "used"},
        )

        resp = client.get("/api/v1/opportunities", headers=auth_headers)
        ids = [item["id"] for item in resp.json()]
        assert opp.id not in ids

    def test_other_active_opportunities_unaffected(self, client, auth_headers, db, sample_user):
        """Dismissing one opportunity doesn't affect others."""
        opp1 = _create_opportunity(db, sample_user.id, hook="Opportunity 1")
        opp2 = _create_opportunity(db, sample_user.id, hook="Opportunity 2")

        client.patch(
            f"/api/v1/opportunities/{opp1.id}",
            headers=auth_headers,
            json={"status": "dismissed"},
        )

        resp = client.get("/api/v1/opportunities", headers=auth_headers)
        ids = [item["id"] for item in resp.json()]
        assert opp1.id not in ids
        assert opp2.id in ids
