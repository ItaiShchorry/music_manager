import logging
from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.campaign import Campaign
from app.models.song import Song
from app.models.submithub import SubmitHubCampaign, SubmitHubSubmission
from app.models.user import User
from app.utils.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(tags=["submithub"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class SHCampaignCreate(BaseModel):
    song_id: int
    campaign_id: int | None = None
    budget_allocated: float | None = None
    curator_count: int | None = None
    notes: str | None = None


class SHCampaignResponse(BaseModel):
    id: int
    song_id: int
    campaign_id: int | None
    campaign_code: str
    budget_allocated: float | None
    curator_count: int | None
    status: str
    notes: str | None
    created_at: datetime

    @classmethod
    def from_orm(cls, c: SubmitHubCampaign) -> "SHCampaignResponse":
        return cls(
            id=c.id,
            song_id=c.song_id,
            campaign_id=c.campaign_id,
            campaign_code=c.campaign_code,
            budget_allocated=float(c.budget_allocated) if c.budget_allocated is not None else None,
            curator_count=c.curator_count,
            status=c.status,
            notes=c.notes,
            created_at=c.created_at,
        )


class SubmissionCreate(BaseModel):
    curator_name: str = Field(..., min_length=1, max_length=255)
    curator_genre_focus: list[str] | None = None
    curator_approval_rate: float | None = None
    submission_date: date | None = None
    cost: float = 3.0


class SubmissionUpdate(BaseModel):
    response_status: Literal["pending", "approved", "declined"] | None = None
    response_date: date | None = None
    curator_feedback: str | None = None
    playlist_added: bool | None = None
    playlist_url: str | None = None


class SubmissionResponse(BaseModel):
    id: int
    submithub_campaign_id: int
    curator_name: str
    curator_genre_focus: list[str] | None
    curator_approval_rate: float | None
    submission_date: date | None
    cost: float
    response_status: str
    response_date: date | None
    curator_feedback: str | None
    playlist_added: bool
    playlist_url: str | None
    created_at: datetime

    @classmethod
    def from_orm(cls, s: SubmitHubSubmission) -> "SubmissionResponse":
        return cls(
            id=s.id,
            submithub_campaign_id=s.submithub_campaign_id,
            curator_name=s.curator_name,
            curator_genre_focus=s.curator_genre_focus,
            curator_approval_rate=s.curator_approval_rate,
            submission_date=s.submission_date,
            cost=float(s.cost),
            response_status=s.response_status,
            response_date=s.response_date,
            curator_feedback=s.curator_feedback,
            playlist_added=s.playlist_added,
            playlist_url=s.playlist_url,
            created_at=s.created_at,
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _generate_code(db: Session) -> str:
    """Generate a unique SH-YYYYMMDD-NNN code."""
    today = datetime.now(UTC).strftime("%Y%m%d")
    prefix = f"SH-{today}-"
    count = db.query(SubmitHubCampaign).filter(
        SubmitHubCampaign.campaign_code.like(f"{prefix}%")
    ).count()
    return f"{prefix}{count + 1:03d}"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/submithub-campaigns", response_model=SHCampaignResponse, status_code=status.HTTP_201_CREATED)
def create_sh_campaign(
    body: SHCampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    song = db.query(Song).filter(Song.id == body.song_id, Song.user_id == current_user.id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    if body.campaign_id is not None:
        camp = db.query(Campaign).filter(
            Campaign.id == body.campaign_id,
            Campaign.user_id == current_user.id,
        ).first()
        if not camp:
            raise HTTPException(status_code=404, detail="Campaign not found")

    sh = SubmitHubCampaign(
        user_id=current_user.id,
        song_id=body.song_id,
        campaign_id=body.campaign_id,
        campaign_code=_generate_code(db),
        budget_allocated=Decimal(str(body.budget_allocated)) if body.budget_allocated else None,
        curator_count=body.curator_count,
        notes=body.notes,
    )
    db.add(sh)
    db.commit()
    db.refresh(sh)
    logger.info(f"Created SubmitHub campaign {sh.campaign_code} for song_id={body.song_id}")
    return SHCampaignResponse.from_orm(sh)


@router.get("/songs/{song_id}/submithub", response_model=list[SHCampaignResponse])
def list_sh_campaigns_for_song(
    song_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    song = db.query(Song).filter(Song.id == song_id, Song.user_id == current_user.id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    campaigns = (
        db.query(SubmitHubCampaign)
        .filter(SubmitHubCampaign.song_id == song_id)
        .order_by(SubmitHubCampaign.created_at.desc())
        .all()
    )
    return [SHCampaignResponse.from_orm(c) for c in campaigns]


@router.post(
    "/submithub-campaigns/{sh_campaign_id}/submissions",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_submission(
    sh_campaign_id: int,
    body: SubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sh = db.query(SubmitHubCampaign).filter(
        SubmitHubCampaign.id == sh_campaign_id,
        SubmitHubCampaign.user_id == current_user.id,
    ).first()
    if not sh:
        raise HTTPException(status_code=404, detail="SubmitHub campaign not found")

    sub = SubmitHubSubmission(
        submithub_campaign_id=sh_campaign_id,
        curator_name=body.curator_name,
        curator_genre_focus=body.curator_genre_focus,
        curator_approval_rate=body.curator_approval_rate,
        submission_date=body.submission_date,
        cost=Decimal(str(body.cost)),
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    logger.info(f"Added submission to SH campaign {sh_campaign_id}: curator={body.curator_name}")
    return SubmissionResponse.from_orm(sub)


@router.get(
    "/submithub-campaigns/{sh_campaign_id}/submissions",
    response_model=list[SubmissionResponse],
)
def list_submissions(
    sh_campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sh = db.query(SubmitHubCampaign).filter(
        SubmitHubCampaign.id == sh_campaign_id,
        SubmitHubCampaign.user_id == current_user.id,
    ).first()
    if not sh:
        raise HTTPException(status_code=404, detail="SubmitHub campaign not found")

    subs = (
        db.query(SubmitHubSubmission)
        .filter(SubmitHubSubmission.submithub_campaign_id == sh_campaign_id)
        .order_by(SubmitHubSubmission.created_at.desc())
        .all()
    )
    return [SubmissionResponse.from_orm(s) for s in subs]


@router.patch("/submithub-submissions/{submission_id}", response_model=SubmissionResponse)
def update_submission(
    submission_id: int,
    body: SubmissionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sub = (
        db.query(SubmitHubSubmission)
        .join(SubmitHubCampaign, SubmitHubSubmission.submithub_campaign_id == SubmitHubCampaign.id)
        .filter(
            SubmitHubSubmission.id == submission_id,
            SubmitHubCampaign.user_id == current_user.id,
        )
        .first()
    )
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(sub, field, value)
    db.commit()
    db.refresh(sub)
    logger.info(f"Updated submission id={submission_id} status={sub.response_status}")
    return SubmissionResponse.from_orm(sub)
