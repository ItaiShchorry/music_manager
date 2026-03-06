"""User Progress & Gamification — streak tracking, level computation, badge awards."""
import logging
from datetime import date, datetime, timezone

from app.models.user_progress import UserProgress, compute_level

logger = logging.getLogger(__name__)

BADGE_CHECKS = [
    ("first_spark", lambda p: p.total_completed >= 1),
    ("three_day_streak", lambda p: p.streak_current >= 3),
    ("week_on_fire", lambda p: p.streak_current >= 7),
    ("ten_creations", lambda p: p.total_completed >= 10),
]


def _award_badges(progress: UserProgress) -> None:
    """Check all badge conditions and append newly earned badges."""
    existing_types = {b["badge_type"] for b in (progress.badges or [])}
    now_iso = datetime.now(timezone.utc).isoformat()
    new_badges = list(progress.badges or [])
    changed = False
    for badge_type, condition in BADGE_CHECKS:
        if badge_type not in existing_types and condition(progress):
            new_badges.append({"badge_type": badge_type, "earned_at": now_iso})
            changed = True
    if changed:
        progress.badges = new_badges


def update_progress(user_id: int, db) -> UserProgress:
    """
    Upsert UserProgress for user_id:
    - Increment total_completed
    - Update streak (consecutive days logic)
    - Recompute level
    - Award any newly earned badges
    """
    today = date.today()
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()

    if progress is None:
        progress = UserProgress(
            user_id=user_id,
            streak_current=1,
            streak_best=1,
            last_challenge_date=today,
            total_completed=1,
            level="newcomer",
            badges=[],
        )
        db.add(progress)
        db.flush()
    else:
        # Update total
        progress.total_completed += 1

        # Streak logic
        last = progress.last_challenge_date
        if last is None:
            progress.streak_current = 1
        elif last == today:
            pass  # already completed today, no change
        elif (today - last).days == 1:
            progress.streak_current += 1
        else:
            progress.streak_current = 1

        if progress.streak_current > progress.streak_best:
            progress.streak_best = progress.streak_current

        progress.last_challenge_date = today

    # Recompute level
    progress.level = compute_level(progress.total_completed)

    # Award badges
    _award_badges(progress)

    progress.updated_at = datetime.now(timezone.utc)
    db.flush()
    return progress
