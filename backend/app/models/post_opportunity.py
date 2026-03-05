from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PostOpportunity(Base):
    __tablename__ = "post_opportunities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    song_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("songs.id", ondelete="SET NULL"), nullable=True
    )

    # The suggestion content
    hook: Mapped[str] = mapped_column(Text, nullable=False)
    why_now: Mapped[str] = mapped_column(Text, nullable=False)
    signal_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # "milestone" | "playlist_add" | "inactivity" | "calendar" | "recent_release" | "trend"

    suggested_platform: Mapped[str | None] = mapped_column(String(50))
    # "instagram" | "facebook" | "tiktok" | "all"
    hashtag_suggestions: Mapped[list | None] = mapped_column(JSON)
    timing_note: Mapped[str | None] = mapped_column(Text)

    # Status lifecycle
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    # "active" | "used" | "dismissed" | "remind_later"
    remind_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User", backref="post_opportunities")
    song = relationship("Song", backref="post_opportunities")
