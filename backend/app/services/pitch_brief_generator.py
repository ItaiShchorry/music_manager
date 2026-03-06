"""Generates a ready-to-copy SubmitHub pitch text from a song's profile."""
import logging

import anthropic

from app.config import settings
from app.models.song import Song

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-20250514"


def _build_prompt(song: Song) -> str:
    parts = [
        "You are a music promotion expert helping an Israeli indie artist craft a SubmitHub pitch.",
        "",
        "Write a SHORT pitch text (2-3 sentences maximum) that the artist can paste directly into SubmitHub.",
        "The pitch should describe the song's sound, mood, language, and reference comparable artists.",
        "It must be engaging, honest, and targeted at playlist curators.",
        "Do NOT include any introduction or explanation — just the pitch text itself.",
        "",
        "SONG DETAILS:",
        f"- Title: {song.title}",
        f"- Artist: {song.artist_name}",
    ]

    if song.genre:
        parts.append(f"- Genre: {song.genre}")
    if song.language:
        parts.append(f"- Language: {song.language}")
    if song.mood_tags:
        parts.append(f"- Mood: {', '.join(song.mood_tags)}")
    if song.comparable_artists:
        parts.append(f"- Comparable artists: {', '.join(song.comparable_artists)}")
    if song.themes:
        parts.append(f"- Themes: {', '.join(song.themes)}")
    if song.story:
        # Use first 300 chars of story as context
        parts.append(f"- Song story: {song.story[:300]}")
    if song.release_date:
        parts.append(f"- Release date: {song.release_date}")

    parts += [
        "",
        "Write the 2-3 sentence pitch now:",
    ]
    return "\n".join(parts)


def _fallback_brief(song: Song) -> str:
    """Rule-based fallback when Claude is unavailable."""
    parts = [f'"{song.title}" by {song.artist_name}']
    if song.genre:
        parts.append(f"— {song.genre}")
    if song.language:
        lang = song.language.capitalize()
        parts.append(f"with {lang} lyrics")
    if song.mood_tags:
        mood = song.mood_tags[0] if song.mood_tags else None
        if mood:
            parts.append(f"with a {mood} feel")
    if song.comparable_artists:
        parts.append(f"for fans of {song.comparable_artists[0]}")
    return " ".join(parts) + "."


class PitchBriefGenerator:
    def __init__(self, client=None):
        self.client = client or anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def generate(self, song: Song) -> str:
        """Return a 2-3 sentence SubmitHub pitch text."""
        prompt = _build_prompt(song)
        try:
            message = self.client.messages.create(
                model=MODEL,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
            )
            text = message.content[0].text.strip()
            # Strip any accidental prefixes like "Here's the pitch:" etc.
            if text.lower().startswith(("here's", "here is", "pitch:")):
                lines = text.split("\n")
                text = "\n".join(l for l in lines if l.strip() and not l.lower().startswith("here")).strip()
            return text or _fallback_brief(song)
        except Exception as exc:
            logger.warning(f"Claude pitch brief generation failed: {exc}")
            return _fallback_brief(song)
