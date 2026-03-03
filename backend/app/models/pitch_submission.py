from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PitchSubmission(Base):
    __tablename__ = "pitch_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    song_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("songs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_type: Mapped[str] = mapped_column(String(20), nullable=False)
    # "playlist" | "radio"
    playlist_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("playlists.id", ondelete="SET NULL"), nullable=True
    )
    radio_station_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("radio_stations.id", ondelete="SET NULL"), nullable=True
    )
    pitched_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    pitch_method: Mapped[str] = mapped_column(String(50), nullable=False)
    # "email" | "spotify" | "instagram_dm" | "submithub"
    status: Mapped[str] = mapped_column(String(50), default="sent", nullable=False)
    # "sent" | "responded" | "added" | "rejected" | "no_response"
    response_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    response_notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    song = relationship("Song", backref="pitches")
    playlist = relationship("Playlist", backref="pitches")
    radio_station = relationship("RadioStation", backref="pitches")
