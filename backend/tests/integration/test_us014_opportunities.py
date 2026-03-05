"""
US-014: Post Opportunity Suggestions

Tests for generating and listing post opportunity cards.
Claude API calls are always mocked — no real API calls.
"""
import json
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

MOCK_OPPORTUNITIES = [
    {
        "hook": "Your song just crossed 5,000 streams — share what that milestone means to you",
        "why_now": "Milestone detected: 5,000 total streams reached",
        "signal_type": "milestone",
        "suggested_platform": "instagram",
        "hashtag_suggestions": ["#מוזיקה_ישראלית", "#5000_השמעות", "#IsraeliPop"],
        "timing_note": "Post today while the milestone is fresh",
    },
    {
        "hook": "It's been a while since you posted — remind your audience you're still active",
        "why_now": "No post idea used in the past 30 days",
        "signal_type": "inactivity",
        "suggested_platform": "facebook",
        "hashtag_suggestions": ["#IsraeliMusic", "#עכשיו_מנגנים"],
        "timing_note": "Post Sunday morning for best reach",
    },
]


def _mock_claude_response(items: list = None):
    """Return a mocked Anthropic client that yields the given opportunity list."""
    if items is None:
        items = MOCK_OPPORTUNITIES
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=json.dumps(items))]
    )
    return mock_client


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

class TestListOpportunities:
    def test_list_when_empty(self, client, auth_headers):
        """GET /opportunities returns 200 and empty list when nothing generated."""
        resp = client.get("/api/v1/opportunities", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_auth_required(self, client):
        """GET /opportunities without token returns 401."""
        resp = client.get("/api/v1/opportunities")
        assert resp.status_code == 401


class TestGenerateOpportunities:
    def test_generate_happy_path(self, client, auth_headers):
        """POST /opportunities/generate returns 201 and opportunity cards."""
        mock_client = _mock_claude_response()
        with patch("app.services.opportunity_service.anthropic") as patched:
            patched.Anthropic.return_value = mock_client
            resp = client.post("/api/v1/opportunities/generate", headers=auth_headers, json={})

        assert resp.status_code == 201
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == len(MOCK_OPPORTUNITIES)
        first = data[0]
        assert "hook" in first
        assert "why_now" in first
        assert "signal_type" in first
        assert first["status"] == "active"

    def test_generated_appear_in_list(self, client, auth_headers):
        """After generating, items appear in GET /opportunities."""
        mock_client = _mock_claude_response()
        with patch("app.services.opportunity_service.anthropic") as patched:
            patched.Anthropic.return_value = mock_client
            client.post("/api/v1/opportunities/generate", headers=auth_headers, json={})

        resp = client.get("/api/v1/opportunities", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) == len(MOCK_OPPORTUNITIES)

    def test_generate_auth_required(self, client):
        """POST /opportunities/generate without token returns 401."""
        resp = client.post("/api/v1/opportunities/generate", json={})
        assert resp.status_code == 401

    def test_generate_with_song_id(self, client, auth_headers, sample_song):
        """Generating for a specific song_id stores the song_id on the opportunities."""
        mock_client = _mock_claude_response([MOCK_OPPORTUNITIES[0]])
        with patch("app.services.opportunity_service.anthropic") as patched:
            patched.Anthropic.return_value = mock_client
            resp = client.post(
                "/api/v1/opportunities/generate",
                headers=auth_headers,
                json={"song_id": sample_song.id},
            )

        assert resp.status_code == 201
        data = resp.json()
        assert data[0]["song_id"] == sample_song.id

    def test_generate_claude_error_returns_fallback(self, client, auth_headers):
        """When Claude raises, fallback opportunities are returned."""
        with patch("app.services.opportunity_service.anthropic") as patched:
            mock_client = MagicMock()
            mock_client.messages.create.side_effect = Exception("Claude unavailable")
            patched.Anthropic.return_value = mock_client
            resp = client.post("/api/v1/opportunities/generate", headers=auth_headers, json={})

        assert resp.status_code == 201
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # fallback always returns at least 1
