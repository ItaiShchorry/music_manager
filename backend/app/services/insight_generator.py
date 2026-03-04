"""AI-powered insight generator for the dashboard."""
import json
import logging
import re
from typing import Any

import anthropic

from app.models.dashboard import DashboardSnapshot

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-20250514"

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

_FALLBACK_TIP = {
    "insight_type": "tip",
    "priority": "medium",
    "title": "Keep building momentum",
    "description": "Consistent promotion and playlist pitching leads to sustainable growth.",
    "action_text": "Submit to 3 new playlists this week",
}


class InsightGenerator:
    def __init__(self, client=None):
        self.client = client or anthropic.Anthropic()

    def generate(
        self,
        snapshot: DashboardSnapshot,
        recent_pitch_added: bool = False,
    ) -> list[dict[str, Any]]:
        """Generate insight cards from the latest snapshot."""
        prompt = self._build_prompt(snapshot, recent_pitch_added)
        try:
            message = self.client.messages.create(
                model=MODEL,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = message.content[0].text
            insights = self._parse(raw)
        except Exception as exc:
            logger.warning(f"Claude insight generation failed: {exc}")
            insights = self._rule_based_fallback(snapshot, recent_pitch_added)

        return sorted(insights, key=lambda x: PRIORITY_ORDER.get(x.get("priority", "medium"), 1))

    # ------------------------------------------------------------------
    def _build_prompt(self, snap: DashboardSnapshot, recent_pitch_added: bool) -> str:
        lines = [
            "You are a music promotion analyst. Generate actionable insight cards for an Israeli indie artist.",
            "",
            "## Current metrics snapshot",
            f"- Streams vs last week: {snap.streams_vs_last_week_pct:+.1f}%" if snap.streams_vs_last_week_pct is not None else "- Streams trend: unknown",
            f"- Save rate: {snap.save_rate:.1f}%" if snap.save_rate is not None else "- Save rate: unknown",
            f"- Follower conversion: {snap.follower_conversion_rate:.1f}%" if snap.follower_conversion_rate is not None else "- Follower conversion: unknown",
            f"- Playlist adds this week: {snap.total_playlist_adds or 0}",
            f"- Recent pitch accepted: {'yes' if recent_pitch_added else 'no'}",
            f"- Health score: {snap.health_score}",
            "",
            "## Instructions",
            "Return a JSON object with an 'insights' array. Each insight must have:",
            "- insight_type: one of 'momentum' | 'warning' | 'opportunity' | 'tip' | 'milestone'",
            "- priority: one of 'high' | 'medium' | 'low'",
            "- title: short title (max 60 chars)",
            "- description: 1-2 sentence explanation (max 150 chars)",
            "- action_text: specific recommended action (max 100 chars)",
            "",
            "Generate 1-3 relevant insights. Focus on the most important issues.",
            "If a pitch was recently accepted, include a momentum insight.",
            "If save rate < 5%, include a tip insight.",
            "If streams dropped, include a warning insight.",
            "Return JSON only, no markdown fences.",
        ]
        return "\n".join(lines)

    def _parse(self, text: str) -> list[dict[str, Any]]:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            logger.warning("No JSON found in Claude insight response")
            return [_FALLBACK_TIP]
        data = json.loads(match.group())
        insights = data.get("insights", [])
        if not insights:
            return [_FALLBACK_TIP]
        required = {"insight_type", "priority", "title", "description"}
        return [i for i in insights if required.issubset(i.keys())]

    def _rule_based_fallback(
        self, snap: DashboardSnapshot, recent_pitch_added: bool
    ) -> list[dict[str, Any]]:
        """Return deterministic insights when Claude is unavailable."""
        results = []
        if recent_pitch_added:
            results.append({
                "insight_type": "momentum",
                "priority": "high",
                "title": "Pitch accepted!",
                "description": "A curator accepted your recent submission.",
                "action_text": "Share the playlist on social media and thank the curator",
            })
        if snap.save_rate is not None and snap.save_rate < 5:
            results.append({
                "insight_type": "tip",
                "priority": "medium",
                "title": f"Low save rate: {snap.save_rate:.1f}%",
                "description": "Target 5%+. Listeners aren't saving your song to their libraries.",
                "action_text": "Add a call-to-action in your next post asking fans to save the song",
            })
        if snap.streams_vs_last_week_pct is not None and snap.streams_vs_last_week_pct < -10:
            results.append({
                "insight_type": "warning",
                "priority": "high",
                "title": f"Streams dropped {abs(snap.streams_vs_last_week_pct):.0f}% this week",
                "description": "This may indicate a playlist removal or end of campaign burst.",
                "action_text": "Submit to 3-5 new playlists to recover momentum",
            })
        return results or [_FALLBACK_TIP]
