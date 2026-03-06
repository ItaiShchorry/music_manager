"""Post Opportunity Engine — generates timely post angle suggestions using Claude."""
import json
import logging
import re
from datetime import date, datetime, timedelta, timezone
from typing import Any

import anthropic

from app.config import settings
from app.models.dashboard import DashboardSnapshot
from app.models.pitch_submission import PitchSubmission
from app.models.post_opportunity import PostOpportunity
from app.models.song import Song
from app.models.youtube_brief import YouTubeBrief

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-20250514"

MILESTONES = [1_000, 5_000, 10_000, 25_000, 50_000, 100_000]

# Hardcoded Israeli holiday calendar (2026). Refresh annually.
ISRAELI_HOLIDAYS: list[dict] = [
    {"name": "Purim", "date": "2026-03-13"},
    {"name": "Passover (Pesach)", "date": "2026-04-02"},
    {"name": "Holocaust Remembrance Day (Yom HaShoah)", "date": "2026-04-23"},
    {"name": "Memorial Day (Yom HaZikaron)", "date": "2026-04-29"},
    {"name": "Independence Day (Yom HaAtzmaut)", "date": "2026-04-30"},
    {"name": "Lag BaOmer", "date": "2026-05-17"},
    {"name": "Shavuot", "date": "2026-05-22"},
    {"name": "Tisha B'Av", "date": "2026-07-23"},
    {"name": "Rosh Hashanah", "date": "2026-09-11"},
    {"name": "Yom Kippur", "date": "2026-09-20"},
    {"name": "Sukkot", "date": "2026-09-25"},
    {"name": "Simchat Torah", "date": "2026-10-03"},
    {"name": "Hanukkah", "date": "2026-12-14"},
]

_FALLBACK_OPPORTUNITIES = [
    {
        "hook": "Share the story behind your latest song — your fans want to know what inspired it",
        "why_now": "Building a personal connection with your audience increases saves and follows",
        "signal_type": "inactivity",
        "category": "promotion",
        "suggested_platform": "instagram",
        "hashtag_suggestions": ["#מוזיקה_ישראלית", "#behind_the_music", "#songwriter", "#IsraeliPop"],
        "timing_note": "Post early in the week for higher engagement",
    }
]


def get_upcoming_israeli_holidays(days_ahead: int = 30) -> list[dict]:
    today = date.today()
    end = today + timedelta(days=days_ahead)
    upcoming = []
    for h in ISRAELI_HOLIDAYS:
        try:
            hdate = date.fromisoformat(h["date"])
            if today <= hdate <= end:
                upcoming.append({
                    "name": h["name"],
                    "date": h["date"],
                    "days_until": (hdate - today).days,
                })
        except ValueError:
            pass
    return upcoming


def _milestone_already_surfaced(user_id: int, milestone: int, db) -> bool:
    """Return True if this milestone has been surfaced as a PostOpportunity before."""
    existing = (
        db.query(PostOpportunity)
        .filter(
            PostOpportunity.user_id == user_id,
            PostOpportunity.signal_type == "milestone",
        )
        .all()
    )
    for opp in existing:
        if str(milestone) in (opp.hook or ""):
            return True
    return False


def _song_has_brief(song_id: int, db) -> bool:
    """Check if a song has any YouTube brief."""
    return db.query(YouTubeBrief).filter(YouTubeBrief.song_id == song_id).first() is not None


def collect_signals(user_id: int, db, songs: list | None = None, song_id: int | None = None) -> list[dict]:
    """Gather all signals that could trigger post opportunities.

    Args:
        user_id: Current user's ID
        db: DB session
        songs: Pre-fetched list of Song objects (optional; loaded if None)
        song_id: Optional filter to limit to a single song (legacy API)
    """
    signals = []

    # Load songs if not provided
    if songs is None:
        songs_q = db.query(Song).filter(Song.user_id == user_id)
        if song_id:
            songs_q = songs_q.filter(Song.id == song_id)
        songs = songs_q.all()

    # 1. Stream milestones (from total across all snapshots)
    latest_snap = (
        db.query(DashboardSnapshot)
        .filter(DashboardSnapshot.user_id == user_id)
        .order_by(DashboardSnapshot.snapshot_date.desc())
        .first()
    )
    if latest_snap and latest_snap.total_streams:
        for milestone in MILESTONES:
            if latest_snap.total_streams >= milestone:
                if not _milestone_already_surfaced(user_id, milestone, db):
                    signals.append({
                        "type": "milestone",
                        "category": "promotion",
                        "milestone": milestone,
                        "current_streams": latest_snap.total_streams,
                    })
                    break

    # 2. Recent playlist adds
    all_adds_q = (
        db.query(PitchSubmission)
        .join(Song, Song.id == PitchSubmission.song_id)
        .filter(
            Song.user_id == user_id,
            PitchSubmission.status == "added",
            PitchSubmission.response_date.isnot(None),
        )
    )
    if song_id:
        all_adds_q = all_adds_q.filter(PitchSubmission.song_id == song_id)
    all_adds = all_adds_q.all()

    week_ago = datetime.now() - timedelta(days=7)
    for pitch in all_adds:
        rd = pitch.response_date
        if rd is not None:
            rd_naive = rd.replace(tzinfo=None) if rd.tzinfo else rd
            if rd_naive >= week_ago:
                playlist_name = (
                    pitch.playlist.name
                    if pitch.playlist
                    else pitch.response_notes or "a playlist"
                )
                signals.append({
                    "type": "playlist_add",
                    "category": "promotion",
                    "song_title": pitch.song.title,
                    "playlist_name": playlist_name,
                })

    # 3. Inactivity
    last_used = (
        db.query(PostOpportunity)
        .filter(
            PostOpportunity.user_id == user_id,
            PostOpportunity.status == "used",
            PostOpportunity.used_at.isnot(None),
        )
        .order_by(PostOpportunity.used_at.desc())
        .first()
    )
    if last_used and last_used.used_at:
        used_at_naive = last_used.used_at.replace(tzinfo=None) if last_used.used_at.tzinfo else last_used.used_at
        days_since = (datetime.now() - used_at_naive).days
    else:
        days_since = 30

    if days_since >= 7:
        signals.append({
            "type": "inactivity",
            "category": "promotion",
            "days_since_last_post_idea_used": days_since,
        })

    # 4. Recent releases
    today = date.today()
    for song in songs:
        if song.release_date and (today - song.release_date).days <= 30:
            signals.append({
                "type": "recent_release",
                "category": "promotion",
                "song_title": song.title,
                "days_since_release": (today - song.release_date).days,
            })

    # 5. Upcoming Israeli holidays
    for holiday in get_upcoming_israeli_holidays(days_ahead=14):
        signals.append({
            "type": "calendar",
            "category": "promotion",
            "holiday_name": holiday["name"],
            "days_until": holiday["days_until"],
        })

    # -----------------------------------------------------------------------
    # 6. Creative signals (catalog analysis)
    # -----------------------------------------------------------------------
    all_moods = []
    all_themes = []
    songs_with_story = []

    for song in songs:
        if song.mood_tags:
            all_moods.extend(song.mood_tags)
        if song.themes:
            all_themes.extend(song.themes)

    # lyric_prompt — song has mood_tags or themes to draw from
    songs_with_profile = [s for s in songs if s.mood_tags or s.themes]
    if songs_with_profile:
        sample = songs_with_profile[0]
        moods = sample.mood_tags or []
        themes = sample.themes or []
        signals.append({
            "type": "lyric_prompt",
            "category": "creative",
            "song_title": sample.title,
            "moods": moods[:3],
            "themes": themes[:3],
        })

    # catalog_gap — detect emotional/thematic imbalance
    unique_moods = set(all_moods)
    heavy_sad = sum(1 for m in all_moods if m.lower() in ("sad", "melancholic", "longing", "dark"))
    if len(songs) >= 2 and heavy_sad > len(songs) * 0.5:
        signals.append({
            "type": "catalog_gap",
            "category": "creative",
            "observation": "Catalog is mostly melancholic — no upbeat or celebratory songs",
            "suggestion": "major-key or celebratory song",
        })

    # style_exploration — if comparable_artists mentioned
    artists_with_comparables = [s for s in songs if s.comparable_artists]
    if artists_with_comparables:
        ca = artists_with_comparables[0].comparable_artists[0]
        signals.append({
            "type": "style_exploration",
            "category": "creative",
            "comparable_artist": ca,
            "song_title": artists_with_comparables[0].title,
        })

    # instrumental_challenge — always a valid creative prompt
    if songs:
        signals.append({
            "type": "instrumental_challenge",
            "category": "creative",
            "description": "Write a 45-second intro that builds from silence to full arrangement",
        })

    # -----------------------------------------------------------------------
    # 7. YouTube signals
    # -----------------------------------------------------------------------
    for song in songs:
        # story_ready — has story > 100 chars AND no brief
        if song.story and len(song.story) > 100 and not _song_has_brief(song.id, db):
            signals.append({
                "type": "story_ready",
                "category": "youtube",
                "song_title": song.title,
                "song_id": song.id,
            })

        # no_video — song > 60 days old and no brief
        if song.release_date and (today - song.release_date).days > 60 and not _song_has_brief(song.id, db):
            signals.append({
                "type": "no_video",
                "category": "youtube",
                "song_title": song.title,
                "song_id": song.id,
                "days_old": (today - song.release_date).days,
            })

    return signals


def _build_catalog_summary(songs: list) -> str:
    if not songs:
        return "No songs in catalog yet."
    lines = []
    for song in songs[:10]:  # cap at 10
        parts = [f"'{song.title}'"]
        if song.genre:
            parts.append(f"genre:{song.genre}")
        if song.mood_tags:
            parts.append(f"mood:{','.join(song.mood_tags[:3])}")
        if song.themes:
            parts.append(f"themes:{','.join(song.themes[:3])}")
        if song.comparable_artists:
            parts.append(f"similar:{','.join(song.comparable_artists[:2])}")
        if song.story:
            parts.append(f"story:{song.story[:100]}...")
        lines.append(" | ".join(parts))
    return "\n".join(lines)


def _build_prompt(signals: list[dict], songs: list | None = None) -> str:
    holidays = get_upcoming_israeli_holidays(days_ahead=14)
    holiday_text = (
        ", ".join(f"{h['name']} in {h['days_until']} days" for h in holidays)
        if holidays
        else "none in the next 14 days"
    )

    catalog_summary = _build_catalog_summary(songs or [])

    return f"""You are this artist's personal creative manager and music coach.

ARTIST CATALOG:
{catalog_summary}

CURRENT SIGNALS:
{json.dumps(signals, indent=2, ensure_ascii=False)}

ISRAELI CALENDAR CONTEXT:
- Today: {date.today().isoformat()}
- Upcoming holidays: {holiday_text}
- Shabbat: Friday evening through Saturday evening (lower engagement window)

YOUR TASK:
Generate 3-5 post opportunity cards — a mix of creative challenges (~60%) and promotional ideas (~40%).

CREATIVE CHALLENGES must be:
- Catalog-specific (reference actual songs, themes, moods from this artist)
- Specific, surprising, and fun — never generic advice
- Varied across: genre cross-pollination, tempo experiments, perspective flips, language play, constraints
- Ideas: write from villain's POV, 7-minute challenge, catalog inversion (if catalog is all minor key → try major), bilingual verse, cover idea from comparable artists

PROMOTIONAL IDEAS:
- Milestone announcements, playlist celebration posts, holiday tie-ins, behind-the-scenes

DIVERSITY AXES — vary challenges across:
- Genre cross-pollination
- Tempo & energy (upbeat vs ambient)
- Goofiness & play (parody, wordplay, absurd constraints)
- Perspective flip (villain's POV, object's POV)
- Language play (Hebrew↔English, bilingual verse)
- Constraints (10-unique-words chorus, silence-to-full-build instrumental)

OUTPUT FORMAT — JSON array, each item:
{{
  "hook": "1-2 sentence description of the challenge or post idea",
  "why_now": "why this is timely or relevant",
  "signal_type": "lyric_prompt|catalog_gap|song_experiment|style_exploration|instrumental_challenge|cover_idea|milestone|playlist_add|inactivity|calendar|recent_release|story_ready|no_video",
  "category": "creative|youtube|promotion",
  "suggested_platform": "instagram|facebook|tiktok|all",
  "hashtag_suggestions": ["#...", "..."],
  "timing_note": "optional timing advice"
}}

Respond ONLY with a valid JSON array (no markdown fences)."""


def _parse_opportunities(text: str) -> list[dict[str, Any]]:
    """Extract JSON array from Claude response, tolerating markdown fences."""
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        logger.warning("No JSON array found in Claude opportunity response")
        return _FALLBACK_OPPORTUNITIES
    try:
        items = json.loads(match.group())
    except json.JSONDecodeError as exc:
        logger.warning(f"JSON parse error in opportunity response: {exc}")
        return _FALLBACK_OPPORTUNITIES
    required = {"hook", "why_now", "signal_type"}
    valid = [i for i in items if isinstance(i, dict) and required.issubset(i.keys())]
    return valid if valid else _FALLBACK_OPPORTUNITIES


class OpportunityGenerator:
    def __init__(self, client=None):
        self.client = client or anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def generate(self, user_id: int, db, song_id: int | None = None) -> list[dict]:
        """Collect signals and ask Claude to generate post opportunity cards."""
        songs_q = db.query(Song).filter(Song.user_id == user_id)
        if song_id:
            songs_q = songs_q.filter(Song.id == song_id)
        songs = songs_q.all()

        signals = collect_signals(user_id, db, songs=songs, song_id=song_id)
        if not signals:
            return []

        prompt = _build_prompt(signals, songs=songs)
        try:
            message = self.client.messages.create(
                model=MODEL,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = message.content[0].text
            return _parse_opportunities(raw)
        except Exception as exc:
            logger.warning(f"Claude opportunity generation failed: {exc}")
            return _FALLBACK_OPPORTUNITIES
