"""
Budget recommendation service — calls Claude to generate a justified channel
split for a campaign based on budget, release type, and song profiles.
"""
import json
import logging
import re

import anthropic

from app.config import settings

from app.models.campaign import Campaign
from app.models.song import Song

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-20250514"

FALLBACK_RECOMMENDATION = {
    "playlist_pitching": {"amount": 0, "pct": 60, "rationale": "Best ROI at emerging tier for Israeli artists"},
    "submithub": {"amount": 0, "pct": 10, "rationale": "Guaranteed curator responses"},
    "social_ads": {"amount": 0, "pct": 20, "rationale": "Instagram > Facebook for Hebrew pop discovery"},
    "content_creation": {"amount": 0, "pct": 7, "rationale": "Acoustic / BTS content drives engagement"},
    "radio_promotion": {"amount": 0, "pct": 2, "rationale": "Kan 88 or Galei Tzahal email outreach"},
    "other": {"amount": 0, "pct": 1, "rationale": "Miscellaneous"},
    "top_tip": "Focus on playlist pitching — it delivers the best streams-per-dollar for emerging Israeli artists.",
}


class BudgetRecommender:
    def __init__(self, client=None):
        self.client = client or anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def generate(self, campaign: Campaign, songs: list[Song]) -> dict:
        prompt = self._build_prompt(campaign, songs)
        logger.info(f"Generating budget recommendation for campaign_id={campaign.id}")

        try:
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            if not response.content:
                raise ValueError("Claude returned an empty response")
            text = response.content[0].text
            return self._parse(text, campaign.budget_total)
        except Exception as e:
            logger.error(f"Budget recommendation failed: {e}", exc_info=True)
            return self._scaled_fallback(float(campaign.budget_total))

    def _build_prompt(self, campaign: Campaign, songs: list[Song]) -> str:
        total = float(campaign.budget_total)
        tier = {
            "awareness": "emerging (0–10K monthly listeners)",
            "growth": "developing (10K–100K monthly listeners)",
            "monetization": "established (100K+ monthly listeners)",
        }.get(campaign.primary_goal or "awareness", "emerging")

        song_lines = []
        for s in songs:
            parts = [s.title]
            if s.genre:
                parts.append(f"genre={s.genre}")
            if s.language:
                parts.append(f"language={s.language}")
            if s.mood_tags:
                parts.append(f"moods={','.join(s.mood_tags)}")
            song_lines.append(" | ".join(parts))

        songs_block = "\n".join(f"  - {l}" for l in song_lines) if song_lines else "  - (no songs attached)"

        return f"""You are a music marketing expert for independent Israeli artists.

Campaign: "{campaign.name}"
Release type: {campaign.release_type}
Artist tier: {tier}
Total budget: ${total:.2f}
Songs:
{songs_block}

Generate a specific, justified budget allocation across these 6 channels:
- playlist_pitching (direct curator outreach)
- submithub (paid curator platform, $3/submission)
- social_ads (Instagram/Facebook/TikTok ads)
- content_creation (video/photo production)
- radio_promotion (Israeli radio outreach — Galei Tzahal, Kan 88, etc.)
- other

Rules:
1. All amounts must sum exactly to ${total:.2f}
2. Amounts must be realistic (e.g. SubmitHub: multiples of $3; social_ads >= $20 if allocated)
3. Each channel gets a plain-English rationale (1 sentence)
4. Include one strategic tip in "top_tip"

Return ONLY valid JSON in this exact format:
{{
  "playlist_pitching": {{"amount": <number>, "pct": <integer>, "rationale": "<string>"}},
  "submithub": {{"amount": <number>, "pct": <integer>, "rationale": "<string>"}},
  "social_ads": {{"amount": <number>, "pct": <integer>, "rationale": "<string>"}},
  "content_creation": {{"amount": <number>, "pct": <integer>, "rationale": "<string>"}},
  "radio_promotion": {{"amount": <number>, "pct": <integer>, "rationale": "<string>"}},
  "other": {{"amount": <number>, "pct": <integer>, "rationale": "<string>"}},
  "top_tip": "<string>"
}}"""

    def _parse(self, text: str, budget_total) -> dict:
        # Strip markdown fences if present
        match = re.search(r"\{.*\}", text, re.DOTALL)
        raw_text = match.group(0) if match else text
        try:
            data = json.loads(raw_text)
            # Validate required keys
            required = {"playlist_pitching", "submithub", "social_ads",
                        "content_creation", "radio_promotion", "other", "top_tip"}
            if not required.issubset(data.keys()):
                raise ValueError("Missing required keys in recommendation")
            return data
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Could not parse budget recommendation JSON: {text[:200]!r} — {e}")
            return self._scaled_fallback(float(budget_total))

    def _scaled_fallback(self, total: float) -> dict:
        rec = {}
        percentages = {
            "playlist_pitching": 60,
            "submithub": 10,
            "social_ads": 20,
            "content_creation": 7,
            "radio_promotion": 2,
            "other": 1,
        }
        for channel, pct in percentages.items():
            amount = round(total * pct / 100, 2)
            rec[channel] = {
                "amount": amount,
                "pct": pct,
                "rationale": FALLBACK_RECOMMENDATION[channel]["rationale"],
            }
        rec["top_tip"] = FALLBACK_RECOMMENDATION["top_tip"]
        return rec
