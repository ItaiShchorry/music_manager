"""YouTube Video Brief Generator — creates SEO-optimized video briefs using Claude."""
import json
import logging
import re
from typing import Any

import anthropic

from app.config import settings

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-20250514"

VALID_CONCEPT_TYPES = {
    "making_of",
    "acoustic_session",
    "production_breakdown",
    "song_explained",
    "live_performance",
}

CONCEPT_DESCRIPTIONS = {
    "making_of": "behind-the-scenes look at how the song was made — creative process, inspiration, production journey",
    "acoustic_session": "stripped-down acoustic performance — raw and intimate, showcasing vocals and songwriting",
    "production_breakdown": "technical deep-dive into the production — beats, instruments, mixing decisions",
    "song_explained": "songwriter explains the story, meaning, and emotions behind the song",
    "live_performance": "live performance video — energy, audience connection, full arrangement",
}


def _build_prompt(song, concept_type: str, key_message: str | None, context: str | None) -> str:
    keywords_text = ""
    if song.search_keywords:
        keywords_text = f"\nSEO Search Keywords: {', '.join(song.search_keywords)}"

    story_text = ""
    if song.story:
        story_text = f"\nSong Story: {song.story[:300]}"

    mood_text = ""
    if song.mood_tags:
        mood_text = f"\nMood: {', '.join(song.mood_tags)}"

    themes_text = ""
    if song.themes:
        themes_text = f"\nThemes: {', '.join(song.themes)}"

    comparable_text = ""
    if song.comparable_artists:
        comparable_text = f"\nComparable Artists: {', '.join(song.comparable_artists)}"

    key_msg_text = f"\nKey Message from Artist: {key_message}" if key_message else ""
    context_text = f"\nAdditional Context: {context}" if context else ""

    concept_desc = CONCEPT_DESCRIPTIONS.get(concept_type, concept_type)

    return f"""You are a YouTube content strategist for an Israeli indie musician.

Generate a detailed YouTube video brief for the following song and concept.

SONG INFO:
- Title: {song.title}
- Artist: {song.artist_name}
- Genre: {song.genre or "indie"}{mood_text}{themes_text}{comparable_text}{story_text}{keywords_text}

VIDEO CONCEPT: {concept_type} — {concept_desc}{key_msg_text}{context_text}

Generate a complete video brief with:
- seo_title: Eye-catching title optimized for search (max 70 characters)
- hook_paragraph: Opening description that grabs viewers (100-150 words)
- chapters: 3-5 chapters with timestamp, title, and what_to_cover
- video_description: YouTube description (300-500 chars) — incorporate the search keywords naturally
- tags: 8-12 tags mixing Hebrew and English

Respond ONLY with valid JSON (no markdown fences):
{{
  "seo_title": "...",
  "hook_paragraph": "...",
  "chapters": [
    {{"timestamp": "0:00", "title": "...", "what_to_cover": "..."}},
    ...
  ],
  "video_description": "...",
  "tags": ["...", "..."]
}}"""


def _fallback_brief(song, concept_type: str) -> dict[str, Any]:
    """Return a structured placeholder when Claude is unavailable."""
    return {
        "seo_title": f"{song.title} — {concept_type.replace('_', ' ').title()} | {song.artist_name}",
        "hook_paragraph": (
            f"Join me as I share the story behind '{song.title}'. "
            f"This video gives you an inside look at the creative process, "
            f"the emotions that inspired the song, and what it means to me as an artist."
        ),
        "chapters": [
            {"timestamp": "0:00", "title": "Introduction", "what_to_cover": "Welcome and brief overview"},
            {"timestamp": "2:00", "title": "The Story", "what_to_cover": "Background and inspiration"},
            {"timestamp": "6:00", "title": "The Creation", "what_to_cover": "How the song came together"},
            {"timestamp": "10:00", "title": "Final Thoughts", "what_to_cover": "What this song means to you"},
        ],
        "video_description": (
            f"'{song.title}' by {song.artist_name}. "
            f"An honest look at the story behind this song. "
            f"Subscribe for more music and behind-the-scenes content."
        ),
        "tags": [
            "Israeli indie", "מוזיקה_ישראלית", "behind the scenes",
            song.title, song.artist_name, concept_type.replace("_", " "),
            "Israeli music", "songwriter",
        ],
    }


def _parse_brief(text: str) -> dict[str, Any] | None:
    """Extract JSON object from Claude response, tolerating markdown fences."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


class YouTubeBriefGenerator:
    def __init__(self, client=None):
        self.client = client or anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def generate(self, song, concept_type: str, key_message: str | None = None, context: str | None = None) -> dict[str, Any]:
        """Generate a YouTube video brief for the given song and concept."""
        prompt = _build_prompt(song, concept_type, key_message, context)
        try:
            message = self.client.messages.create(
                model=MODEL,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = message.content[0].text
            result = _parse_brief(raw)
            if result:
                return result
            logger.warning("Could not parse Claude brief response — using fallback")
        except Exception as exc:
            logger.warning(f"Claude YouTube brief generation failed: {exc}")

        return _fallback_brief(song, concept_type)
