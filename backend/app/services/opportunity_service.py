"""Post Opportunity Engine — generates timely post angle suggestions using Claude."""
import json
import logging
import re
from datetime import date, datetime, timedelta, timezone
from typing import Any

import anthropic

from app.models.dashboard import DashboardSnapshot
from app.models.pitch_submission import PitchSubmission
from app.models.post_opportunity import PostOpportunity
from app.models.song import Song

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


def collect_signals(user_id: int, db, song_id: int | None) -> list[dict]:
    """Gather all signals that could trigger post opportunities."""
    signals = []

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
                        "milestone": milestone,
                        "current_streams": latest_snap.total_streams,
                    })
                    break  # surface one milestone at a time (lowest unsurfaced)

    # 2. Recent playlist adds (pitches with status='added' and a response_date)
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
        # Strip timezone for comparison (SQLite returns naive datetimes)
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
                    "song_title": pitch.song.title,
                    "playlist_name": playlist_name,
                })

    # 3. Inactivity (no opportunity used in last 7 days)
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
            "days_since_last_post_idea_used": days_since,
        })

    # 4. Recent releases (songs released in last 30 days)
    songs_q = db.query(Song).filter(Song.user_id == user_id)
    if song_id:
        songs_q = songs_q.filter(Song.id == song_id)
    songs = songs_q.all()
    today = date.today()
    for song in songs:
        if song.release_date and (today - song.release_date).days <= 30:
            signals.append({
                "type": "recent_release",
                "song_title": song.title,
                "days_since_release": (today - song.release_date).days,
            })

    # 5. Upcoming Israeli holidays
    upcoming_holidays = get_upcoming_israeli_holidays(days_ahead=14)
    for holiday in upcoming_holidays:
        signals.append({
            "type": "calendar",
            "holiday_name": holiday["name"],
            "days_until": holiday["days_until"],
        })

    return signals


def _build_prompt(signals: list[dict]) -> str:
    holidays = get_upcoming_israeli_holidays(days_ahead=14)
    holiday_text = (
        ", ".join(f"{h['name']} in {h['days_until']} days" for h in holidays)
        if holidays
        else "none in the next 14 days"
    )
    return f"""You are a social media strategist for an Israeli mainstream pop musician.

Based on the signals below, generate 3-5 post opportunity cards. Each is a *suggestion of what to post about* — NOT the actual post text.

ARTIST CONTEXT:
- Genre: mainstream Hebrew pop
- Primary platforms: Instagram, Facebook
- Audience: Israeli fans aged 18-40
- Language: Hebrew (primary), English (secondary)

CURRENT SIGNALS:
{json.dumps(signals, indent=2, ensure_ascii=False)}

ISRAELI CALENDAR CONTEXT:
- Today: {date.today().isoformat()}
- Upcoming holidays: {holiday_text}
- Shabbat: Friday evening through Saturday evening (lower engagement window)

RULES FOR EACH OPPORTUNITY:
- hook: 1-2 sentences describing what to write about (NOT the post itself)
- why_now: explain the signal that makes this timely
- signal_type: one of: milestone, playlist_add, inactivity, calendar, trend, recent_release
- suggested_platform: instagram | facebook | tiktok | all
- hashtag_suggestions: 4-8 tags (mix Hebrew + English), relevant to this specific hook
- timing_note: specific timing advice if relevant (e.g., "post before Shabbat starts Friday 6pm")

Only generate opportunities that are genuinely timely and relevant. Better to return 2 great ones than 5 mediocre ones.

Respond ONLY with a valid JSON array (no markdown fences):
[
  {{
    "hook": "...",
    "why_now": "...",
    "signal_type": "...",
    "suggested_platform": "...",
    "hashtag_suggestions": ["#...", "..."],
    "timing_note": "..."
  }}
]"""


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
        self.client = client or anthropic.Anthropic()

    def generate(self, user_id: int, db, song_id: int | None = None) -> list[dict]:
        """Collect signals and ask Claude to generate post opportunity cards."""
        signals = collect_signals(user_id, db, song_id)
        if not signals:
            return []

        prompt = _build_prompt(signals)
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
