"""YouTube Brief API — generate, manage lifecycle, track stats."""
import logging
import re
from datetime import date, datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.song import Song
from app.models.user import User
from app.models.youtube_brief import YouTubeBrief, YouTubeBriefStat
from app.services.youtube_brief_generator import YouTubeBriefGenerator, VALID_CONCEPT_TYPES
from app.utils.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(tags=["youtube-briefs"])

YOUTUBE_URL_PATTERN = re.compile(
    r"^https?://(www\.)?(youtube\.com|youtu\.be)/", re.IGNORECASE
)

VALID_STATUSES = {"draft", "planned", "filmed", "published"}


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class YouTubeBriefCreate(BaseModel):
    concept_type: str
    key_message: Optional[str] = None
    context: Optional[str] = None

    @field_validator("concept_type")
    @classmethod
    def validate_concept_type(cls, v: str) -> str:
        if v not in VALID_CONCEPT_TYPES:
            raise ValueError(f"concept_type must be one of: {', '.join(sorted(VALID_CONCEPT_TYPES))}")
        return v


class YouTubeBriefUpdate(BaseModel):
    status: Optional[str] = None
    youtube_url: Optional[str] = None
    seo_title: Optional[str] = None
    key_message: Optional[str] = None


class YouTubeChapterSchema(BaseModel):
    timestamp: str
    title: str
    what_to_cover: str

    model_config = {"from_attributes": True}


class YouTubeBriefResponse(BaseModel):
    id: int
    user_id: int
    song_id: int
    concept_type: str
    key_message: Optional[str]
    context: Optional[str]
    seo_title: Optional[str]
    hook_paragraph: Optional[str]
    chapters: Optional[list]
    video_description: Optional[str]
    tags: Optional[list]
    status: str
    filmed_at: Optional[datetime]
    published_at: Optional[datetime]
    youtube_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class YouTubeBriefStatCreate(BaseModel):
    snapshot_date: date
    views: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    subscribers_gained: Optional[int] = None


class YouTubeBriefStatResponse(BaseModel):
    id: int
    brief_id: int
    snapshot_date: date
    views: Optional[int]
    likes: Optional[int]
    comments: Optional[int]
    subscribers_gained: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_brief_or_404(brief_id: int, user_id: int, db: Session) -> YouTubeBrief:
    brief = (
        db.query(YouTubeBrief)
        .filter(YouTubeBrief.id == brief_id, YouTubeBrief.user_id == user_id)
        .first()
    )
    if not brief:
        raise HTTPException(status_code=404, detail="YouTube brief not found")
    return brief


# ---------------------------------------------------------------------------
# Song-scoped endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/songs/{song_id}/youtube-briefs",
    response_model=YouTubeBriefResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_brief(
    song_id: int,
    body: YouTubeBriefCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate and save a YouTube video brief for a song."""
    song = db.query(Song).filter(Song.id == song_id, Song.user_id == current_user.id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    generator = YouTubeBriefGenerator()
    result = generator.generate(song, body.concept_type, body.key_message, body.context)

    brief = YouTubeBrief(
        user_id=current_user.id,
        song_id=song_id,
        concept_type=body.concept_type,
        key_message=body.key_message,
        context=body.context,
        seo_title=result.get("seo_title"),
        hook_paragraph=result.get("hook_paragraph"),
        chapters=result.get("chapters"),
        video_description=result.get("video_description"),
        tags=result.get("tags"),
        status="draft",
    )
    db.add(brief)
    db.commit()
    db.refresh(brief)
    logger.info(f"Created YouTube brief id={brief.id} for song={song_id}")
    return brief


@router.get("/songs/{song_id}/youtube-briefs", response_model=list[YouTubeBriefResponse])
def list_briefs_for_song(
    song_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all YouTube briefs for a specific song."""
    song = db.query(Song).filter(Song.id == song_id, Song.user_id == current_user.id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    briefs = (
        db.query(YouTubeBrief)
        .filter(YouTubeBrief.song_id == song_id, YouTubeBrief.user_id == current_user.id)
        .order_by(YouTubeBrief.created_at.desc())
        .all()
    )
    return briefs


# ---------------------------------------------------------------------------
# User-level brief endpoints
# ---------------------------------------------------------------------------

@router.get("/youtube-briefs", response_model=list[YouTubeBriefResponse])
def list_all_briefs(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all YouTube briefs for the current user, optionally filtered by status."""
    q = db.query(YouTubeBrief).filter(YouTubeBrief.user_id == current_user.id)
    if status:
        q = q.filter(YouTubeBrief.status == status)
    return q.order_by(YouTubeBrief.created_at.desc()).all()


@router.get("/youtube-briefs/{brief_id}", response_model=YouTubeBriefResponse)
def get_brief(
    brief_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _get_brief_or_404(brief_id, current_user.id, db)


@router.patch("/youtube-briefs/{brief_id}", response_model=YouTubeBriefResponse)
def update_brief(
    brief_id: int,
    body: YouTubeBriefUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update brief status and/or fields. filmed_at auto-set on →filmed; published_at+url on →published."""
    brief = _get_brief_or_404(brief_id, current_user.id, db)

    if body.status is not None:
        if body.status not in VALID_STATUSES:
            raise HTTPException(
                status_code=422,
                detail=f"status must be one of: {', '.join(sorted(VALID_STATUSES))}",
            )
        if body.status == "published":
            url = body.youtube_url or brief.youtube_url
            if not url:
                raise HTTPException(
                    status_code=422,
                    detail="youtube_url is required when publishing a brief",
                )
            if not YOUTUBE_URL_PATTERN.match(url):
                raise HTTPException(
                    status_code=422,
                    detail="youtube_url must be a valid YouTube URL (youtube.com or youtu.be)",
                )
            brief.published_at = datetime.now(timezone.utc)
            brief.youtube_url = url
        elif body.status == "filmed":
            brief.filmed_at = datetime.now(timezone.utc)

        brief.status = body.status

    if body.youtube_url is not None and body.status != "published":
        brief.youtube_url = body.youtube_url
    if body.seo_title is not None:
        brief.seo_title = body.seo_title
    if body.key_message is not None:
        brief.key_message = body.key_message

    db.commit()
    db.refresh(brief)
    logger.info(f"Updated YouTube brief id={brief_id} status={brief.status}")
    return brief


@router.delete("/youtube-briefs/{brief_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brief(
    brief_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    brief = _get_brief_or_404(brief_id, current_user.id, db)
    db.delete(brief)
    db.commit()
    logger.info(f"Deleted YouTube brief id={brief_id}")


# ---------------------------------------------------------------------------
# Stats endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/youtube-briefs/{brief_id}/stats",
    response_model=YouTubeBriefStatResponse,
    status_code=status.HTTP_201_CREATED,
)
def log_stats(
    brief_id: int,
    body: YouTubeBriefStatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log a performance snapshot for a brief (upsert on duplicate date)."""
    brief = _get_brief_or_404(brief_id, current_user.id, db)

    existing = (
        db.query(YouTubeBriefStat)
        .filter(
            YouTubeBriefStat.brief_id == brief.id,
            YouTubeBriefStat.snapshot_date == body.snapshot_date,
        )
        .first()
    )

    if existing:
        for field in ("views", "likes", "comments", "subscribers_gained"):
            val = getattr(body, field)
            if val is not None:
                setattr(existing, field, val)
        db.commit()
        db.refresh(existing)
        return existing

    stat = YouTubeBriefStat(
        brief_id=brief.id,
        snapshot_date=body.snapshot_date,
        views=body.views,
        likes=body.likes,
        comments=body.comments,
        subscribers_gained=body.subscribers_gained,
    )
    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat


@router.get("/youtube-briefs/{brief_id}/stats", response_model=list[YouTubeBriefStatResponse])
def list_stats(
    brief_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    brief = _get_brief_or_404(brief_id, current_user.id, db)
    return (
        db.query(YouTubeBriefStat)
        .filter(YouTubeBriefStat.brief_id == brief.id)
        .order_by(YouTubeBriefStat.snapshot_date.desc())
        .all()
    )
