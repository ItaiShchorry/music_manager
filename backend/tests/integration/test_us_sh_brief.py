"""
SubmitHub Pitch Brief Generator

POST /submithub-campaigns/{id}/brief
Generates a ready-to-copy pitch text from the song's profile using Claude.
"""
import json
from unittest.mock import MagicMock, patch

import pytest

from app.models.submithub import SubmitHubCampaign


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _create_sh_campaign(db, sample_song, sample_user) -> SubmitHubCampaign:
    sh = SubmitHubCampaign(
        user_id=sample_user.id,
        song_id=sample_song.id,
        campaign_code="SH-TEST-001",
        status="active",
    )
    db.add(sh)
    db.flush()
    return sh


MOCK_BRIEF_TEXT = (
    "Melancholic indie pop song with heartfelt Hebrew lyrics about moving on. "
    "Acoustic-driven production with vulnerable vocals — for fans of John Mayer and Asaf Avidan. "
    "Fresh release with genuine emotional depth."
)


def _mock_claude(text: str = MOCK_BRIEF_TEXT):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=text)]
    )
    return mock_client


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

class TestGeneratePitchBrief:
    def test_happy_path(self, client, auth_headers, db, sample_user, sample_song):
        """POST /submithub-campaigns/{id}/brief → 200 with pitch_text."""
        sh = _create_sh_campaign(db, sample_song, sample_user)

        with patch("app.services.pitch_brief_generator.anthropic") as patched:
            patched.Anthropic.return_value = _mock_claude()
            resp = client.post(
                f"/api/v1/submithub-campaigns/{sh.id}/brief",
                headers=auth_headers,
            )

        assert resp.status_code == 200
        data = resp.json()
        assert "pitch_text" in data
        assert len(data["pitch_text"]) > 10
        assert "campaign_code" in data
        assert data["campaign_code"] == "SH-TEST-001"
        assert "spotify_url" in data

    def test_pitch_text_reflects_song_profile(self, client, auth_headers, db, sample_user, sample_song):
        """The brief is generated from the song's actual profile fields."""
        # Add genre + mood to the sample song
        sample_song.genre = "indie pop"
        sample_song.language = "hebrew"
        sample_song.mood_tags = ["melancholic", "hopeful"]
        db.flush()

        sh = _create_sh_campaign(db, sample_song, sample_user)

        with patch("app.services.pitch_brief_generator.anthropic") as patched:
            mock_client = _mock_claude()
            patched.Anthropic.return_value = mock_client
            resp = client.post(
                f"/api/v1/submithub-campaigns/{sh.id}/brief",
                headers=auth_headers,
            )

        assert resp.status_code == 200
        # Verify Claude was called (prompt contains song details)
        call_args = mock_client.messages.create.call_args
        prompt_content = call_args[1]["messages"][0]["content"]
        assert "indie pop" in prompt_content.lower() or "Test Song" in prompt_content

    def test_claude_error_returns_fallback(self, client, auth_headers, db, sample_user, sample_song):
        """When Claude fails, a rule-based fallback brief is returned."""
        sh = _create_sh_campaign(db, sample_song, sample_user)

        with patch("app.services.pitch_brief_generator.anthropic") as patched:
            mock_client = MagicMock()
            mock_client.messages.create.side_effect = Exception("Claude unavailable")
            patched.Anthropic.return_value = mock_client
            resp = client.post(
                f"/api/v1/submithub-campaigns/{sh.id}/brief",
                headers=auth_headers,
            )

        assert resp.status_code == 200
        data = resp.json()
        assert "pitch_text" in data
        assert len(data["pitch_text"]) > 10

    def test_campaign_not_found_returns_404(self, client, auth_headers):
        """Unknown campaign ID → 404."""
        with patch("app.services.pitch_brief_generator.anthropic"):
            resp = client.post(
                "/api/v1/submithub-campaigns/99999/brief",
                headers=auth_headers,
            )
        assert resp.status_code == 404

    def test_auth_required(self, client, db, sample_user, sample_song):
        """No token → 401."""
        sh = _create_sh_campaign(db, sample_song, sample_user)
        resp = client.post(f"/api/v1/submithub-campaigns/{sh.id}/brief")
        assert resp.status_code == 401
