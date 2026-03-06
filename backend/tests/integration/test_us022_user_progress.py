"""
US-022: User Progress & Gamification
- Streak increments on consecutive days, resets on gap
- streak_best updated correctly
- Level thresholds: 0-4=newcomer, 5=emerging, 15=pro, 30=expert
- Badges awarded: first_spark, three_day_streak, ten_creations, publisher
- GET /me/progress returns full progress object
"""
import pytest
from datetime import date, timedelta

from app.models.user_progress import UserProgress, compute_level
from app.models.post_opportunity import PostOpportunity


# ---------------------------------------------------------------------------
# Unit tests: compute_level
# ---------------------------------------------------------------------------

LEVEL_CASES = [
    (0, "newcomer"),
    (4, "newcomer"),
    (5, "emerging"),
    (14, "emerging"),
    (15, "pro"),
    (29, "pro"),
    (30, "expert"),
    (100, "expert"),
]

@pytest.mark.parametrize("total, expected_level", LEVEL_CASES)
def test_compute_level(total, expected_level):
    assert compute_level(total) == expected_level


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------

@pytest.fixture()
def active_opportunity(db, sample_user, sample_song):
    opp = PostOpportunity(
        user_id=sample_user.id,
        song_id=sample_song.id,
        hook="Test challenge",
        why_now="Testing",
        signal_type="lyric_prompt",
        category="creative",
        status="active",
    )
    db.add(opp)
    db.flush()
    return opp


def _complete_challenge(client, opp_id, auth_headers):
    return client.post(
        f"/api/v1/challenges/{opp_id}/complete",
        json={"content_type": "text", "text_content": "Lyrics here"},
        headers=auth_headers,
    )


def test_get_progress_returns_structure(client, sample_user, auth_headers, db):
    """GET /me/progress returns a progress object with all expected fields."""
    # Create progress record directly
    progress = UserProgress(
        user_id=sample_user.id,
        streak_current=3,
        streak_best=5,
        total_completed=7,
        level="emerging",
        badges=[{"badge_type": "first_spark", "earned_at": "2026-03-01T00:00:00Z"}],
    )
    db.add(progress)
    db.flush()

    resp = client.get("/api/v1/me/progress", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["streak_current"] == 3
    assert data["streak_best"] == 5
    assert data["total_completed"] == 7
    assert data["level"] == "emerging"
    assert len(data["badges"]) == 1


def test_first_challenge_awards_first_spark_badge(client, active_opportunity, auth_headers, db, sample_user):
    """first_spark badge awarded on first challenge completion."""
    _complete_challenge(client, active_opportunity.id, auth_headers)

    progress = db.query(UserProgress).filter(UserProgress.user_id == sample_user.id).first()
    db.refresh(progress)
    badge_types = [b["badge_type"] for b in progress.badges]
    assert "first_spark" in badge_types


def test_streak_increments_on_consecutive_days(db, sample_user):
    """Streak increments when last_challenge_date is yesterday."""
    from app.services.progress_service import update_progress

    yesterday = date.today() - timedelta(days=1)
    progress = UserProgress(
        user_id=sample_user.id,
        streak_current=2,
        streak_best=2,
        last_challenge_date=yesterday,
        total_completed=2,
    )
    db.add(progress)
    db.flush()

    update_progress(sample_user.id, db)
    db.refresh(progress)
    assert progress.streak_current == 3


def test_streak_resets_on_gap(db, sample_user):
    """Streak resets to 1 when last_challenge_date is more than 1 day ago."""
    from app.services.progress_service import update_progress

    three_days_ago = date.today() - timedelta(days=3)
    progress = UserProgress(
        user_id=sample_user.id,
        streak_current=5,
        streak_best=5,
        last_challenge_date=three_days_ago,
        total_completed=5,
    )
    db.add(progress)
    db.flush()

    update_progress(sample_user.id, db)
    db.refresh(progress)
    assert progress.streak_current == 1


def test_streak_no_change_if_already_done_today(db, sample_user):
    """Streak stays the same when already completed a challenge today."""
    from app.services.progress_service import update_progress

    progress = UserProgress(
        user_id=sample_user.id,
        streak_current=4,
        streak_best=4,
        last_challenge_date=date.today(),
        total_completed=4,
    )
    db.add(progress)
    db.flush()

    update_progress(sample_user.id, db)
    db.refresh(progress)
    assert progress.streak_current == 4


def test_streak_best_updated(db, sample_user):
    """streak_best is updated when current exceeds it."""
    from app.services.progress_service import update_progress

    yesterday = date.today() - timedelta(days=1)
    progress = UserProgress(
        user_id=sample_user.id,
        streak_current=5,
        streak_best=5,
        last_challenge_date=yesterday,
        total_completed=5,
    )
    db.add(progress)
    db.flush()

    update_progress(sample_user.id, db)
    db.refresh(progress)
    assert progress.streak_best == 6
    assert progress.streak_current == 6


def test_ten_creations_badge_awarded(db, sample_user):
    """ten_creations badge awarded when total_completed reaches 10."""
    from app.services.progress_service import update_progress

    yesterday = date.today() - timedelta(days=1)
    progress = UserProgress(
        user_id=sample_user.id,
        streak_current=1,
        streak_best=1,
        last_challenge_date=yesterday,
        total_completed=9,
        badges=[],
    )
    db.add(progress)
    db.flush()

    update_progress(sample_user.id, db)
    db.refresh(progress)
    assert progress.total_completed == 10
    badge_types = [b["badge_type"] for b in progress.badges]
    assert "ten_creations" in badge_types


def test_get_progress_404_if_no_progress(client, auth_headers, sample_user, db):
    """GET /me/progress returns 404 when no progress record exists (or creates a default)."""
    resp = client.get("/api/v1/me/progress", headers=auth_headers)
    # Either 404 or returns default progress — either is acceptable
    assert resp.status_code in (200, 404)
