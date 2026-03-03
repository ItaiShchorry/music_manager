import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pitch_submission import PitchSubmission
from app.models.playlist import Playlist
from app.models.radio_station import RadioStation
from app.models.song import Song
from app.models.user import User
from app.utils.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(tags=["pitches"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class PitchCreate(BaseModel):
    song_id: int
    target_type: str          # "playlist" | "radio"
    playlist_id: int | None = None
    radio_station_id: int | None = None
    pitch_method: str         # "email" | "spotify" | "instagram_dm" | "submithub"
    response_notes: str | None = None


class PitchUpdate(BaseModel):
    status: str | None = None
    response_notes: str | None = None
    response_date: datetime | None = None


class PitchResponse(BaseModel):
    id: int
    song_id: int
    target_type: str
    playlist_id: int | None
    radio_station_id: int | None
    pitched_date: datetime
    pitch_method: str
    status: str
    response_date: datetime | None
    response_notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/pitches", response_model=PitchResponse, status_code=status.HTTP_201_CREATED)
def create_pitch(
    body: PitchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verify song exists and belongs to current user
    song = db.query(Song).filter(
        Song.id == body.song_id, Song.user_id == current_user.id
    ).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    pitch = PitchSubmission(
        song_id=body.song_id,
        target_type=body.target_type,
        playlist_id=body.playlist_id,
        radio_station_id=body.radio_station_id,
        pitch_method=body.pitch_method,
        response_notes=body.response_notes,
        pitched_date=datetime.now(timezone.utc),
    )
    db.add(pitch)
    db.commit()
    db.refresh(pitch)
    logger.info(
        f"Pitch created id={pitch.id} song_id={body.song_id} "
        f"target={body.target_type} for user={current_user.id}"
    )
    return pitch


@router.get("/songs/{song_id}/pitches", response_model=list[PitchResponse])
def get_pitches_for_song(
    song_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    song = db.query(Song).filter(
        Song.id == song_id, Song.user_id == current_user.id
    ).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    pitches = (
        db.query(PitchSubmission)
        .filter(PitchSubmission.song_id == song_id)
        .order_by(PitchSubmission.pitched_date.desc())
        .all()
    )
    return pitches


@router.patch("/pitches/{pitch_id}", response_model=PitchResponse)
def update_pitch(
    pitch_id: int,
    body: PitchUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verify pitch belongs to current user (via song)
    pitch = (
        db.query(PitchSubmission)
        .join(Song, Song.id == PitchSubmission.song_id)
        .filter(PitchSubmission.id == pitch_id, Song.user_id == current_user.id)
        .first()
    )
    if not pitch:
        raise HTTPException(status_code=404, detail="Pitch not found")

    updates = body.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(pitch, field, value)

    db.commit()
    db.refresh(pitch)
    logger.info(f"Pitch updated id={pitch_id} fields={list(updates.keys())} for user={current_user.id}")
    return pitch
