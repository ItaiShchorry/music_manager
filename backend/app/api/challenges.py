"""Challenge Completion API — file uploads + creation entries."""
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.creation_entry import CreationEntry
from app.models.post_opportunity import PostOpportunity
from app.models.user import User
from app.services.progress_service import update_progress
from app.utils.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(tags=["challenges"])

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ChallengeCompleteRequest(BaseModel):
    content_type: str  # text | audio | video | image | link
    text_content: Optional[str] = None
    file_url: Optional[str] = None
    external_url: Optional[str] = None
    caption_draft: Optional[str] = None


class CreationEntryResponse(BaseModel):
    id: int
    user_id: int
    opportunity_id: Optional[int]
    content_type: str
    text_content: Optional[str]
    file_url: Optional[str]
    external_url: Optional[str]
    caption_draft: Optional[str]
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UploadResponse(BaseModel):
    file_url: str
    filename: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/challenges/{opportunity_id}/complete",
    response_model=CreationEntryResponse,
    status_code=status.HTTP_201_CREATED,
)
def complete_challenge(
    opportunity_id: int,
    body: ChallengeCompleteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submit a completed challenge — saves CreationEntry, marks opportunity used, updates progress."""
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

    entry = CreationEntry(
        user_id=current_user.id,
        opportunity_id=opportunity_id,
        content_type=body.content_type,
        text_content=body.text_content,
        file_url=body.file_url,
        external_url=body.external_url,
        caption_draft=body.caption_draft,
        status="draft",
    )
    db.add(entry)

    # Mark opportunity as used
    opp.status = "used"
    opp.used_at = datetime.now(timezone.utc)

    db.flush()

    # Update user progress (streak + level + badges)
    update_progress(current_user.id, db)

    db.commit()
    db.refresh(entry)
    logger.info(f"Challenge completed: entry_id={entry.id} user={current_user.id} opp={opportunity_id}")
    return entry


@router.get("/challenges", response_model=list[CreationEntryResponse])
def list_creations(
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List the current user's creation entries."""
    q = db.query(CreationEntry).filter(CreationEntry.user_id == current_user.id)
    if status_filter:
        q = q.filter(CreationEntry.status == status_filter)
    return q.order_by(CreationEntry.created_at.desc()).all()


@router.post(
    "/uploads",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload an audio/video/image file and return the stored URL."""
    user_upload_dir = os.path.join(UPLOADS_DIR, str(current_user.id))
    os.makedirs(user_upload_dir, exist_ok=True)

    # Prefix with UUID to avoid collisions
    safe_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(user_upload_dir, safe_name)

    contents = file.file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # Return relative URL
    file_url = f"/uploads/{current_user.id}/{safe_name}"
    logger.info(f"File uploaded: {file_url} user={current_user.id}")
    return UploadResponse(file_url=file_url, filename=file.filename)
