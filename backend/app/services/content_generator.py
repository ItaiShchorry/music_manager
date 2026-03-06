"""
HebrewContentGenerator — uses Claude claude-sonnet-4-20250514 to generate
platform-optimised Hebrew social media captions for song promotion.
"""
import json
import logging
import re

import anthropic

from app.config import settings

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-20250514"

# (min_chars, max_chars) per platform
PLATFORM_LIMITS: dict[str, tuple[int, int]] = {
    "instagram": (125, 150),
    "facebook": (40, 80),
    "tiktok": (50, 100),
}

TONE_DESCRIPTIONS: dict[str, str] = {
    "emotional": "emotional and vulnerable — share personal feelings with raw authenticity",
    "excited": "excited and energetic — enthusiastic, upbeat, and celebratory",
    "casual": "conversational and casual — like talking to a friend, use slang like אחלה יאללה",
}


class HebrewContentGenerator:
    """Generates Hebrew + English social media content variants via Claude."""

    def __init__(self, client=None):
        self.client = client or anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def generate_for_song(
        self,
        song,
        post_type: str,
        platforms: list[str],
        tones: list[str],
        key_message: str = "",
        context: str = "",
    ) -> list[dict]:
        """
        Generate one Claude call per tone, then cross each platform.
        Returns a flat list of dicts: one per (tone, platform) combination.
        """
        results = []

        for tone in tones:
            logger.info(f"Generating content for song_id={song.id} tone={tone}")
            raw = self._call_claude(song, post_type, tone, key_message, context)

            for platform in platforms:
                caption_he = self._trim(raw.get("caption_hebrew", ""), platform)
                caption_en = self._trim(raw.get("caption_english", ""), platform)
                hashtags = (
                    (raw.get("hashtags_hebrew") or []) + (raw.get("hashtags_english") or [])
                )[:10]

                results.append(
                    {
                        "tone": tone,
                        "platform": platform,
                        "caption_hebrew": caption_he,
                        "caption_english": caption_en,
                        "hashtags": hashtags,
                        "character_count": len(caption_he),
                    }
                )

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _call_claude(
        self, song, post_type: str, tone: str, key_message: str, context: str
    ) -> dict:
        """Call Claude and return a parsed dict with caption + hashtag fields."""
        prompt = self._build_prompt(song, post_type, tone, key_message, context)
        response = self.client.messages.create(
            model=MODEL,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        if not response.content:
            raise ValueError("Claude returned an empty response")
        text = response.content[0].text
        return self._parse_json(text)

    def _build_prompt(
        self, song, post_type: str, tone: str, key_message: str, context: str
    ) -> str:
        tone_desc = TONE_DESCRIPTIONS.get(tone, tone)
        story_snippet = (song.story or "")[:200]
        mood_str = ", ".join(song.mood_tags or [])
        themes_str = ", ".join(song.themes or [])

        return f"""You are a social media expert for Israeli indie musicians.

SONG DETAILS:
- Title: {song.title}
- Artist: {song.artist_name}
- Genre: {song.genre or "indie"}
- Language: {song.language or "hebrew"}
- Mood: {mood_str}
- Themes: {themes_str}
- Story: {story_snippet}

POST TYPE: {post_type}
KEY MESSAGE: {key_message or "New song out now"}
ADDITIONAL CONTEXT: {context}
TONE: {tone_desc}

REQUIREMENTS:
- Write informal, authentic Hebrew (like talking to friends)
- Use natural Hebrew slang where appropriate (אחלה, יאללה, בטח)
- Include 3-5 Hebrew hashtags and 3-5 English hashtags
- Include emojis naturally
- End Hebrew caption with call-to-action (🎧 לינק בביו)
- End English caption with call-to-action (🎧 Link in bio)

Return ONLY a JSON object — no markdown, no explanation, no code fences:
{{
  "caption_hebrew": "<Hebrew caption, approximately 130-160 chars>",
  "caption_english": "<English caption, approximately 100-130 chars>",
  "hashtags_hebrew": ["#tag1", "#tag2", "#tag3"],
  "hashtags_english": ["#Tag1", "#Tag2", "#Tag3"]
}}"""

    def _parse_json(self, text: str) -> dict:
        """Parse Claude's JSON response, falling back to regex extraction."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
            logger.error(f"Could not parse Claude JSON response: {text[:200]!r}")
            return {
                "caption_hebrew": "",
                "caption_english": "",
                "hashtags_hebrew": [],
                "hashtags_english": [],
            }

    def _trim(self, text: str, platform: str) -> str:
        """Trim caption to the platform's max character limit."""
        max_len = PLATFORM_LIMITS.get(platform, (50, 200))[1]
        if len(text) <= max_len:
            return text
        return text[:max_len].rstrip()
