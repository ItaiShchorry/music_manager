import logging
from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.generated_content import GeneratedContent
from app.models.song import Song
from app.models.user import User
from app.services.content_generator import HebrewContentGenerator
from app.utils.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/songs", tags=["content"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ContentRequest(BaseModel):
    post_type: Literal["release", "bts", "story", "engagement", "thank_you"] = "release"
    key_message: str | None = None
    context: str | None = None
    tones: list[Literal["emotional", "excited", "casual"]] = ["emotional", "excited", "casual"]
    platforms: list[Literal["instagram", "facebook", "tiktok"]] = ["instagram", "facebook", "tiktok"]


class GeneratedContentResponse(BaseModel):
    id: int
    song_id: int
    post_type: str
    platform: str
    tone: str
    caption_hebrew: str | None
    caption_english: str | None
    hashtags: list | None
    character_count: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/{song_id}/content",
    response_model=list[GeneratedContentResponse],
    status_code=status.HTTP_201_CREATED,
)
def generate_content(
    song_id: int,
    body: ContentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    song = db.query(Song).filter(Song.id == song_id, Song.user_id == current_user.id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    logger.info(
        f"Generating {len(body.tones)} tone(s) × {len(body.platforms)} platform(s) "
        f"for song_id={song_id} user={current_user.id}"
    )

    generator = HebrewContentGenerator()
    variants = generator.generate_for_song(
        song=song,
        post_type=body.post_type,
        platforms=body.platforms,
        tones=body.tones,
        key_message=body.key_message or "",
        context=body.context or "",
    )

    saved = []
    for v in variants:
        content = GeneratedContent(
            user_id=current_user.id,
            song_id=song_id,
            post_type=body.post_type,
            platform=v["platform"],
            tone=v["tone"],
            caption_hebrew=v["caption_hebrew"],
            caption_english=v["caption_english"],
            hashtags=v["hashtags"],
            character_count=v["character_count"],
        )
        db.add(content)
        saved.append(content)

    db.commit()
    for c in saved:
        db.refresh(c)

    logger.info(f"Saved {len(saved)} content items for song_id={song_id}")
    return saved


@router.get("/{song_id}/content", response_model=list[GeneratedContentResponse])
def list_content(
    song_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    song = db.query(Song).filter(Song.id == song_id, Song.user_id == current_user.id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    items = (
        db.query(GeneratedContent)
        .filter(GeneratedContent.song_id == song_id)
        .order_by(GeneratedContent.created_at.desc())
        .all()
    )
    return items
