from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

LEVEL_THRESHOLDS = [
    (30, "expert"),
    (15, "pro"),
    (5, "emerging"),
    (0, "newcomer"),
]


def compute_level(total_completed: int) -> str:
    for threshold, level in LEVEL_THRESHOLDS:
        if total_completed >= threshold:
            return level
    return "newcomer"


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )

    streak_current: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    streak_best: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_challenge_date: Mapped[date | None] = mapped_column(Date)
    total_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    level: Mapped[str] = mapped_column(String(20), default="newcomer", nullable=False)
    # newcomer | emerging | pro | expert
    badges: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    # [{badge_type: str, earned_at: str (ISO)}]

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User", backref="progress")
