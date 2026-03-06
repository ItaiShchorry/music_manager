"""Post Opportunity API: generate, list, and update status."""
import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database import get_db
from app.models.post_opportunity import PostOpportunity
from app.models.user import User
from app.services.opportunity_service import OpportunityGenerator

logger = logging.getLogger(__name__)
router = APIRouter(tags=["opportunities"])

VALID_STATUSES = {"used", "dismissed", "remind_later"}


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class OpportunityResponse(BaseModel):
    id: int
    song_id: Optional[int]
    hook: str
    why_now: str
    signal_type: str
    category: str
    suggested_platform: Optional[str]
    hashtag_suggestions: Optional[list]
    timing_note: Optional[str]
    status: str
    used_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class GenerateRequest(BaseModel):
    song_id: Optional[int] = None


class OpportunityUpdate(BaseModel):
    status: str  # used | dismissed | remind_later


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/opportunities", response_model=list[OpportunityResponse])
def list_opportunities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all active post opportunities for the current user."""
    items = (
        db.query(PostOpportunity)
        .filter(
            PostOpportunity.user_id == current_user.id,
            PostOpportunity.status == "active",
        )
        .order_by(PostOpportunity.created_at.desc())
        .all()
    )
    return items


@router.post("/opportunities/generate", response_model=list[OpportunityResponse], status_code=201)
def generate_opportunities(
    body: GenerateRequest = GenerateRequest(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Ask Claude to generate fresh post opportunity cards based on current signals."""
    generator = OpportunityGenerator()
    raw_items = generator.generate(user_id=current_user.id, db=db, song_id=body.song_id)

    created = []
    for item in raw_items:
        opp = PostOpportunity(
            user_id=current_user.id,
            song_id=body.song_id,
            hook=item.get("hook", ""),
            why_now=item.get("why_now", ""),
            signal_type=item.get("signal_type", "tip"),
            category=item.get("category", "promotion"),
            suggested_platform=item.get("suggested_platform"),
            hashtag_suggestions=item.get("hashtag_suggestions"),
            timing_note=item.get("timing_note"),
            status="active",
        )
        db.add(opp)
        created.append(opp)

    db.commit()
    for opp in created:
        db.refresh(opp)

    logger.info(f"Generated {len(created)} post opportunities for user {current_user.id}")
    return created


@router.patch("/opportunities/{opportunity_id}", response_model=OpportunityResponse)
def update_opportunity(
    opportunity_id: int,
    body: OpportunityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark an opportunity as used, dismissed, or remind_later."""
    opp = (
        db.query(PostOpportunity)
        .filter(
            PostOpportunity.id == opportunity_id,
            PostOpportunity.user_id == current_user.id,
        )
        .first()
    )
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    if body.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=422,
            detail=f"status must be one of: {', '.join(sorted(VALID_STATUSES))}",
        )

    opp.status = body.status
    if body.status == "used":
        opp.used_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(opp)
    logger.info(f"Updated opportunity {opportunity_id} → status={body.status}")
    return opp
