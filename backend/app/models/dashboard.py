"""Dashboard snapshot and AI insight models."""
from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class DashboardSnapshot(Base):
    __tablename__ = "dashboard_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    snapshot_date = Column(Date, nullable=False)

    # Raw metrics from Spotify for Artists (manual input)
    total_streams = Column(Integer, default=0)
    total_monthly_listeners = Column(Integer, default=0)
    total_followers = Column(Integer, default=0)
    total_saves = Column(Integer, default=0)
    total_playlist_adds = Column(Integer, default=0)

    # Calculated metrics
    save_rate = Column(Float, nullable=True)                # (saves / streams) * 100
    follower_conversion_rate = Column(Float, nullable=True)  # (followers / monthly_listeners) * 100
    cost_per_stream = Column(Float, nullable=True)           # from campaign data

    # Week-over-week trends (user inputs these from Spotify for Artists)
    streams_vs_last_week_pct = Column(Float, nullable=True)
    listeners_vs_last_week_pct = Column(Float, nullable=True)
    followers_vs_last_week_pct = Column(Float, nullable=True)

    # Computed health score
    health_score = Column(Integer, nullable=True)           # 0-100

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="snapshots")


class Insight(Base):
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    insight_type = Column(String(50), nullable=False)  # momentum|warning|opportunity|tip|milestone
    priority = Column(String(20), default="medium")    # low|medium|high
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    action_text = Column(String(255), nullable=True)
    action_link = Column(String(500), nullable=True)

    related_song_id = Column(Integer, ForeignKey("songs.id", ondelete="SET NULL"), nullable=True)
    related_campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="SET NULL"), nullable=True)

    status = Column(String(50), default="active")  # active|dismissed|actioned

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="insights")
