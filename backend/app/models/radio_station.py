from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RadioStation(Base):
    __tablename__ = "radio_stations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_hebrew: Mapped[str | None] = mapped_column(String(255))
    station_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # "national" | "regional" | "online" | "university"
    contact_email: Mapped[str | None] = mapped_column(String(255))
    contact_phone: Mapped[str | None] = mapped_column(String(50))
    website: Mapped[str | None] = mapped_column(String(255))
    genres_focus: Mapped[list | None] = mapped_column(JSON)    # ["mainstream pop", "rock"]
    best_for: Mapped[list | None] = mapped_column(JSON)        # ["new artists", "indie"]
    submission_guidelines: Mapped[str | None] = mapped_column(Text)
    response_time: Mapped[str | None] = mapped_column(String(100))
    reach_description: Mapped[str | None] = mapped_column(String(255))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
