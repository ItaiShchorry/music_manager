from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import (
    Date, DateTime, ForeignKey, Integer, JSON, Numeric, String, Table, Text, Column
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# Many-to-many association table: campaigns ↔ songs
campaign_songs = Table(
    "campaign_songs",
    Base.metadata,
    Column("campaign_id", Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), primary_key=True),
    Column("song_id", Integer, ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True),
)


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    release_type: Mapped[str] = mapped_column(String(50), nullable=False)   # single | ep | album
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    budget_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    budget_spent: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))

    primary_goal: Mapped[str | None] = mapped_column(String(100))   # awareness | growth | monetization
    status: Mapped[str] = mapped_column(String(50), default="planning")  # planning | active | completed

    # AI-generated budget recommendation (stored as JSON)
    budget_recommendation: Mapped[dict | None] = mapped_column(JSON)

    notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    # Relationships
    songs = relationship("Song", secondary=campaign_songs, lazy="selectin")
    expenses = relationship("Expense", back_populates="campaign", cascade="all, delete-orphan")


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    expense_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # playlist_pitching | social_ads | content | radio_promotion | submithub | pr | other
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    subcategory: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="expenses")
