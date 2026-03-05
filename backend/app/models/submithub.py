from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SubmitHubCampaign(Base):
    __tablename__ = "submithub_campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id", ondelete="CASCADE"), nullable=False)
    campaign_id: Mapped[int | None] = mapped_column(ForeignKey("campaigns.id", ondelete="SET NULL"))

    campaign_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    budget_allocated: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    curator_count: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50), default="active")  # active | completed

    notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    submissions: Mapped[list["SubmitHubSubmission"]] = relationship(
        "SubmitHubSubmission", back_populates="sh_campaign", cascade="all, delete-orphan"
    )


class SubmitHubSubmission(Base):
    __tablename__ = "submithub_submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    submithub_campaign_id: Mapped[int] = mapped_column(
        ForeignKey("submithub_campaigns.id", ondelete="CASCADE"), nullable=False
    )

    curator_name: Mapped[str] = mapped_column(String(255), nullable=False)
    curator_genre_focus: Mapped[list[str] | None] = mapped_column(JSON)
    curator_approval_rate: Mapped[float | None]

    submission_date: Mapped[date | None] = mapped_column(Date)
    cost: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("3.00"))

    response_status: Mapped[str] = mapped_column(String(50), default="pending")  # pending | approved | declined
    response_date: Mapped[date | None] = mapped_column(Date)
    curator_feedback: Mapped[str | None] = mapped_column(Text)

    playlist_added: Mapped[bool] = mapped_column(Boolean, default=False)
    playlist_url: Mapped[str | None] = mapped_column(String(500))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    sh_campaign: Mapped["SubmitHubCampaign"] = relationship(
        "SubmitHubCampaign", back_populates="submissions"
    )
