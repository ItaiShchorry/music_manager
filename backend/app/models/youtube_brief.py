from datetime import datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class YouTubeBrief(Base):
    __tablename__ = "youtube_briefs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    song_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("songs.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Brief request parameters
    concept_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # making_of | acoustic_session | production_breakdown | song_explained | live_performance
    key_message: Mapped[str | None] = mapped_column(Text)
    context: Mapped[str | None] = mapped_column(Text)

    # Generated content
    seo_title: Mapped[str | None] = mapped_column(String(100))
    hook_paragraph: Mapped[str | None] = mapped_column(Text)
    chapters: Mapped[list | None] = mapped_column(JSON)  # [{timestamp, title, what_to_cover}]
    video_description: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list | None] = mapped_column(JSON)  # [str]

    # Lifecycle status
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    # draft | planned | filmed | published
    filmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    youtube_url: Mapped[str | None] = mapped_column(String(500))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User", backref="youtube_briefs")
    song = relationship("Song", backref="youtube_briefs")
    stats = relationship("YouTubeBriefStat", back_populates="brief", cascade="all, delete-orphan")


class YouTubeBriefStat(Base):
    __tablename__ = "youtube_brief_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    brief_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("youtube_briefs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    snapshot_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    views: Mapped[int | None] = mapped_column(Integer)
    likes: Mapped[int | None] = mapped_column(Integer)
    comments: Mapped[int | None] = mapped_column(Integer)
    subscribers_gained: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (UniqueConstraint("brief_id", "snapshot_date", name="uq_brief_stat_date"),)

    brief = relationship("YouTubeBrief", back_populates="stats")
