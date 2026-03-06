"""
Generates campaign learnings by comparing planned budget allocation
vs actual channel spend, then calls Claude for actionable insights.
"""
import json
import logging
import re
from collections import defaultdict

import anthropic

from app.config import settings

from app.models.campaign import Campaign, Expense

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-20250514"

CHANNEL_LABELS = {
    "playlist_pitching": "Playlist Pitching",
    "submithub": "SubmitHub",
    "social_ads": "Social Ads",
    "content_creation": "Content Creation",
    "content": "Content Creation",
    "radio_promotion": "Radio Promotion",
    "pr": "PR / Press",
    "other": "Other",
}

# Maps expense category to budget_recommendation key
CATEGORY_TO_CHANNEL = {
    "playlist_pitching": "playlist_pitching",
    "submithub": "submithub",
    "social_ads": "social_ads",
    "content": "content_creation",
    "content_creation": "content_creation",
    "radio_promotion": "radio_promotion",
    "pr": "other",
    "other": "other",
}


def _build_prompt(campaign: Campaign, actual_by_channel: dict[str, float]) -> str:
    planned = campaign.budget_recommendation or {}
    total_spent = sum(actual_by_channel.values())

    planned_lines = []
    if planned:
        for ch, data in planned.items():
            if ch == "top_tip":
                continue
            label = CHANNEL_LABELS.get(ch, ch)
            planned_lines.append(f"  {label}: planned ${data.get('amount', 0):.2f}")
    else:
        planned_lines.append("  (no planned allocation available)")

    actual_lines = []
    if actual_by_channel:
        for ch, amt in actual_by_channel.items():
            label = CHANNEL_LABELS.get(ch, ch)
            actual_lines.append(f"  {label}: ${amt:.2f}")
    else:
        actual_lines.append("  (no expenses recorded)")

    return f"""You are a music marketing analyst reviewing an Israeli indie artist's campaign results.

Campaign: "{campaign.name}"
Type: {campaign.release_type}
Budget: ${float(campaign.budget_total):.2f} total, ${total_spent:.2f} spent
Status: {campaign.status}

Planned allocation:
{chr(10).join(planned_lines)}

Actual spend by channel:
{chr(10).join(actual_lines)}

Analyze the campaign and provide:
1. A 2-3 sentence summary of what happened and the main takeaway.
2. Per-channel insights for each channel that has planned or actual spend.
3. 3 specific suggestions for the NEXT campaign based on these results.

Return ONLY valid JSON in this exact format:
{{
  "summary": "<2-3 sentence summary>",
  "channel_insights": [
    {{
      "channel": "<channel_key>",
      "planned": <number or null>,
      "actual": <number>,
      "verdict": "<on_track|over_budget|under_budget|not_used|unplanned>",
      "recommendation": "<1 sentence recommendation>"
    }}
  ],
  "next_campaign_suggestions": ["<suggestion1>", "<suggestion2>", "<suggestion3>"]
}}

Use these channel keys: playlist_pitching, submithub, social_ads, content_creation, radio_promotion, other."""


def _fallback_learnings(campaign: Campaign, actual_by_channel: dict[str, float]) -> dict:
    """Rule-based fallback when Claude is unavailable."""
    planned = campaign.budget_recommendation or {}
    total_spent = sum(actual_by_channel.values())
    total_budget = float(campaign.budget_total)

    if total_spent == 0:
        summary = (
            f"Campaign \"{campaign.name}\" had no recorded expenses. "
            "Log your spending to unlock channel performance insights."
        )
    elif total_spent > total_budget * 0.9:
        summary = (
            f"Campaign \"{campaign.name}\" used {round(total_spent / total_budget * 100)}% of the budget. "
            "Review channel performance and adjust allocation for the next run."
        )
    else:
        summary = (
            f"Campaign \"{campaign.name}\" spent ${total_spent:.2f} of ${total_budget:.2f} budget. "
            "Consider what worked best and double down on that channel next time."
        )

    # Build per-channel insights
    all_channels = set(actual_by_channel.keys())
    if planned:
        for ch in planned:
            if ch != "top_tip":
                all_channels.add(ch)

    channel_insights = []
    for ch in sorted(all_channels):
        actual = actual_by_channel.get(ch, 0.0)
        plan_data = planned.get(ch, {}) if planned else {}
        plan_amt = plan_data.get("amount") if plan_data else None

        if plan_amt is not None and actual == 0:
            verdict = "not_used"
            rec = f"Consider allocating budget to {CHANNEL_LABELS.get(ch, ch)} as planned."
        elif plan_amt is None and actual > 0:
            verdict = "unplanned"
            rec = f"Add {CHANNEL_LABELS.get(ch, ch)} to your planned allocation next time."
        elif plan_amt and actual > plan_amt * 1.1:
            verdict = "over_budget"
            rec = f"Cap {CHANNEL_LABELS.get(ch, ch)} closer to ${plan_amt:.0f} next campaign."
        elif plan_amt and actual < plan_amt * 0.9:
            verdict = "under_budget"
            rec = f"You have room to invest more in {CHANNEL_LABELS.get(ch, ch)} next time."
        else:
            verdict = "on_track"
            rec = f"Continue this allocation for {CHANNEL_LABELS.get(ch, ch)}."

        channel_insights.append({
            "channel": ch,
            "planned": plan_amt,
            "actual": actual,
            "verdict": verdict,
            "recommendation": rec,
        })

    suggestions = [
        "Review which channels drove the most engagement and increase allocation there.",
        "Set a pre-launch reminder to pitch to Israeli playlists at least 4 weeks out.",
        "Compare SubmitHub approval rate vs direct playlist pitch to optimize spend next round.",
    ]

    return {
        "summary": summary,
        "channel_insights": channel_insights,
        "next_campaign_suggestions": suggestions,
    }


class LearningsGenerator:
    def __init__(self, client=None):
        self.client = client or anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def generate(self, campaign: Campaign, expenses: list[Expense]) -> dict:
        # Aggregate actual spend per channel
        actual_by_channel: dict[str, float] = defaultdict(float)
        for e in expenses:
            ch = CATEGORY_TO_CHANNEL.get(e.category, "other")
            actual_by_channel[ch] += float(e.amount)
        actual_by_channel = dict(actual_by_channel)

        prompt = _build_prompt(campaign, actual_by_channel)
        logger.info(f"Generating learnings for campaign_id={campaign.id}")

        try:
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text.strip()
            return self._parse(text, campaign, actual_by_channel)
        except Exception as exc:
            logger.warning(f"LearningsGenerator Claude call failed: {exc}")
            return _fallback_learnings(campaign, actual_by_channel)

    def _parse(self, text: str, campaign: Campaign, actual_by_channel: dict) -> dict:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        raw = match.group(0) if match else text
        try:
            data = json.loads(raw)
            required = {"summary", "channel_insights", "next_campaign_suggestions"}
            if not required.issubset(data.keys()):
                raise ValueError("Missing required keys")
            return data
        except (json.JSONDecodeError, ValueError) as exc:
            logger.warning(f"Failed to parse learnings JSON: {exc}")
            return _fallback_learnings(campaign, actual_by_channel)
