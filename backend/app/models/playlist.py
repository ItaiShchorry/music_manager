from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Playlist(Base):
    __tablename__ = "playlists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    spotify_id: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    curator_name: Mapped[str | None] = mapped_column(String(255))
    curator_contact: Mapped[str | None] = mapped_column(String(255))  # email or IG handle
    follower_count: Mapped[int | None] = mapped_column(Integer)
    genres: Mapped[list | None] = mapped_column(JSON)          # ["pop", "hebrew pop"]
    languages: Mapped[list | None] = mapped_column(JSON)       # ["hebrew", "english"]
    mood_tags: Mapped[list | None] = mapped_column(JSON)       # ["melancholic", "upbeat"]
    submission_method: Mapped[str | None] = mapped_column(String(50))
    # "spotify_for_artists" | "email" | "instagram_dm" | "submithub"
    submission_guidelines: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
