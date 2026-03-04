"""Dashboard API: snapshot sync, health score, insight cards."""
import logging
from datetime import date, datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database import get_db
from app.models.dashboard import DashboardSnapshot, Insight
from app.models.pitch_submission import PitchSubmission
from app.models.user import User
from app.services.health_score import calculate_health_score, health_label
from app.services.insight_generator import InsightGenerator

logger = logging.getLogger(__name__)
router = APIRouter(tags=["dashboard"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class SnapshotCreate(BaseModel):
    total_streams: int = 0
    total_monthly_listeners: int = 0
    total_followers: int = 0
    total_saves: int = 0
    total_playlist_adds: int = 0
    streams_vs_last_week_pct: Optional[float] = None
    listeners_vs_last_week_pct: Optional[float] = None
    followers_vs_last_week_pct: Optional[float] = None
    cost_per_stream: Optional[float] = None


class SnapshotResponse(BaseModel):
    id: int
    snapshot_date: date
    total_streams: int
    total_monthly_listeners: int
    total_followers: int
    total_saves: int
    total_playlist_adds: int
    save_rate: Optional[float]
    follower_conversion_rate: Optional[float]
    cost_per_stream: Optional[float]
    streams_vs_last_week_pct: Optional[float]
    listeners_vs_last_week_pct: Optional[float]
    followers_vs_last_week_pct: Optional[float]
    health_score: Optional[int]

    class Config:
        from_attributes = True


class HealthScoreResponse(BaseModel):
    health_score: int
    label: str
    metrics: dict[str, Any]


class InsightResponse(BaseModel):
    id: int
    insight_type: str
    priority: str
    title: str
    description: str
    action_text: Optional[str]
    action_link: Optional[str]
    related_song_id: Optional[int]
    related_campaign_id: Optional[int]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class InsightUpdate(BaseModel):
    status: str  # dismissed | actioned


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _compute_snapshot(body: SnapshotCreate) -> dict:
    """Derive calculated fields from raw input."""
    save_rate = (
        round((body.total_saves / body.total_streams) * 100, 2)
        if body.total_streams > 0
        else None
    )
    follower_conversion_rate = (
        round((body.total_followers / body.total_monthly_listeners) * 100, 2)
        if body.total_monthly_listeners > 0
        else None
    )
    score = calculate_health_score(
        streams_vs_last_week_pct=body.streams_vs_last_week_pct,
        save_rate=save_rate,
        follower_conversion_rate=follower_conversion_rate,
        total_playlist_adds=body.total_playlist_adds,
        cost_per_stream=body.cost_per_stream,
    )
    return {
        "save_rate": save_rate,
        "follower_conversion_rate": follower_conversion_rate,
        "health_score": score,
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/dashboard/snapshots", response_model=SnapshotResponse, status_code=201)
def create_snapshot(
    body: SnapshotCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Manual Spotify data sync — upserts a snapshot for today."""
    today = date.today()
    computed = _compute_snapshot(body)

    existing = (
        db.query(DashboardSnapshot)
        .filter(
            DashboardSnapshot.user_id == current_user.id,
            DashboardSnapshot.snapshot_date == today,
        )
        .first()
    )

    if existing:
        # Update existing row and return 200 via a trick: raise then return
        # We need to signal 200 instead of 201 when updating.
        # FastAPI's status_code is fixed per route — we'll handle it via a separate path.
        for field, value in {**body.model_dump(), **computed}.items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        # Re-raise as 200 by returning the object (caller checks status via response)
        from fastapi.responses import JSONResponse
        return JSONResponse(
            content=_snapshot_to_dict(existing),
            status_code=200,
        )

    snap = DashboardSnapshot(
        user_id=current_user.id,
        snapshot_date=today,
        **body.model_dump(),
        **computed,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    logger.info(f"Created dashboard snapshot for user {current_user.id}, health_score={snap.health_score}")
    return snap


def _snapshot_to_dict(snap: DashboardSnapshot) -> dict:
    return {
        "id": snap.id,
        "snapshot_date": snap.snapshot_date.isoformat(),
        "total_streams": snap.total_streams,
        "total_monthly_listeners": snap.total_monthly_listeners,
        "total_followers": snap.total_followers,
        "total_saves": snap.total_saves,
        "total_playlist_adds": snap.total_playlist_adds,
        "save_rate": snap.save_rate,
        "follower_conversion_rate": snap.follower_conversion_rate,
        "cost_per_stream": snap.cost_per_stream,
        "streams_vs_last_week_pct": snap.streams_vs_last_week_pct,
        "listeners_vs_last_week_pct": snap.listeners_vs_last_week_pct,
        "followers_vs_last_week_pct": snap.followers_vs_last_week_pct,
        "health_score": snap.health_score,
    }


@router.get("/dashboard/health-score", response_model=HealthScoreResponse)
def get_health_score(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return the latest health score and key metrics for the current user."""
    snap = (
        db.query(DashboardSnapshot)
        .filter(DashboardSnapshot.user_id == current_user.id)
        .order_by(DashboardSnapshot.snapshot_date.desc())
        .first()
    )
    if not snap:
        raise HTTPException(status_code=404, detail="No dashboard data found. Sync Spotify data first.")

    score = snap.health_score or 0
    return HealthScoreResponse(
        health_score=score,
        label=health_label(score),
        metrics={
            "total_streams": snap.total_streams,
            "total_monthly_listeners": snap.total_monthly_listeners,
            "total_followers": snap.total_followers,
            "total_saves": snap.total_saves,
            "total_playlist_adds": snap.total_playlist_adds,
            "save_rate": snap.save_rate,
            "follower_conversion_rate": snap.follower_conversion_rate,
            "cost_per_stream": snap.cost_per_stream,
            "streams_vs_last_week_pct": snap.streams_vs_last_week_pct,
            "listeners_vs_last_week_pct": snap.listeners_vs_last_week_pct,
            "followers_vs_last_week_pct": snap.followers_vs_last_week_pct,
        },
    )


@router.post("/dashboard/insights/generate", response_model=list[InsightResponse], status_code=201)
def generate_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate AI insight cards from the latest snapshot."""
    snap = (
        db.query(DashboardSnapshot)
        .filter(DashboardSnapshot.user_id == current_user.id)
        .order_by(DashboardSnapshot.snapshot_date.desc())
        .first()
    )
    if not snap:
        raise HTTPException(status_code=404, detail="No dashboard data. Sync Spotify data first.")

    # Check for any accepted pitch belonging to the current user
    from app.models.song import Song as SongModel
    recent_added = (
        db.query(PitchSubmission)
        .join(SongModel, SongModel.id == PitchSubmission.song_id)
        .filter(
            SongModel.user_id == current_user.id,
            PitchSubmission.status == "added",
        )
        .first()
    )

    generator = InsightGenerator()
    raw_insights = generator.generate(snap, recent_pitch_added=bool(recent_added))

    created = []
    for item in raw_insights:
        insight = Insight(
            user_id=current_user.id,
            insight_type=item.get("insight_type", "tip"),
            priority=item.get("priority", "medium"),
            title=item.get("title", ""),
            description=item.get("description", ""),
            action_text=item.get("action_text"),
            action_link=item.get("action_link"),
        )
        db.add(insight)
        created.append(insight)

    db.commit()
    for i in created:
        db.refresh(i)

    logger.info(f"Generated {len(created)} insights for user {current_user.id}")
    return created


@router.get("/dashboard/insights", response_model=list[InsightResponse])
def list_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List active insights for the current user, high priority first."""
    from sqlalchemy import case
    priority_order = case(
        {"high": 0, "medium": 1, "low": 2},
        value=Insight.priority,
        else_=1,
    )
    insights = (
        db.query(Insight)
        .filter(
            Insight.user_id == current_user.id,
            Insight.status == "active",
        )
        .order_by(priority_order, Insight.created_at.desc())
        .all()
    )
    return insights


@router.patch("/dashboard/insights/{insight_id}", response_model=InsightResponse)
def update_insight(
    insight_id: int,
    body: InsightUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Dismiss or mark an insight as actioned."""
    insight = (
        db.query(Insight)
        .filter(Insight.id == insight_id, Insight.user_id == current_user.id)
        .first()
    )
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    if body.status not in ("dismissed", "actioned"):
        raise HTTPException(status_code=422, detail="status must be 'dismissed' or 'actioned'")
    insight.status = body.status
    db.commit()
    db.refresh(insight)
    return insight
