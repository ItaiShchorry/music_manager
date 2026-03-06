"""User Progress API — GET /me/progress."""
import logging
from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.user_progress import UserProgress
from app.utils.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(tags=["progress"])


class BadgeSchema(BaseModel):
    badge_type: str
    earned_at: str

    model_config = {"from_attributes": True}


class UserProgressResponse(BaseModel):
    id: int
    user_id: int
    streak_current: int
    streak_best: int
    last_challenge_date: Optional[date]
    total_completed: int
    level: str
    badges: list
    updated_at: datetime

    model_config = {"from_attributes": True}


@router.get("/me/progress", response_model=UserProgressResponse)
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return the current user's gamification progress."""
    progress = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == current_user.id)
        .first()
    )
    if not progress:
        raise HTTPException(status_code=404, detail="No progress record found — complete a challenge to start!")
    return progress
