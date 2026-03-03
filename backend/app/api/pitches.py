import logging
from datetime import datetime, timezone
from typing import Literal

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

VALID_STATUSES = Literal["sent", "responded", "added", "rejected", "no_response"]
VALID_METHODS = Literal["email", "spotify", "instagram_dm", "submithub"]


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class PitchCreate(BaseModel):
    song_id: int
    target_type: Literal["playlist", "radio"]
    playlist_id: int | None = None
    radio_station_id: int | None = None
    pitch_method: VALID_METHODS
    response_notes: str | None = None


class PitchUpdate(BaseModel):
    status: VALID_STATUSES | None = None
    response_notes: str | None = None
    response_date: datetime | None = None


class PitchResponse(BaseModel):
    id: int
    song_id: int
    target_type: str
    target_name: str | None
    playlist_id: int | None
    radio_station_id: int | None
    pitched_date: datetime
    pitch_method: str
    status: str
    response_date: datetime | None
    response_notes: str | None
    created_at: datetime


def _build_response(pitch: PitchSubmission) -> PitchResponse:
    """Construct PitchResponse, resolving target name from loaded relationships."""
    target_name: str | None = None
    if pitch.target_type == "playlist" and pitch.playlist:
        target_name = pitch.playlist.name
    elif pitch.target_type == "radio" and pitch.radio_station:
        target_name = pitch.radio_station.name

    return PitchResponse(
        id=pitch.id,
        song_id=pitch.song_id,
        target_type=pitch.target_type,
        target_name=target_name,
        playlist_id=pitch.playlist_id,
        radio_station_id=pitch.radio_station_id,
        pitched_date=pitch.pitched_date,
        pitch_method=pitch.pitch_method,
        status=pitch.status,
        response_date=pitch.response_date,
        response_notes=pitch.response_notes,
        created_at=pitch.created_at,
    )


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

    # Validate that the referenced target exists and matches target_type
    if body.target_type == "playlist":
        if not body.playlist_id:
            raise HTTPException(status_code=422, detail="playlist_id required when target_type is 'playlist'")
        if not db.get(Playlist, body.playlist_id):
            raise HTTPException(status_code=404, detail="Playlist not found")
    else:  # "radio"
        if not body.radio_station_id:
            raise HTTPException(status_code=422, detail="radio_station_id required when target_type is 'radio'")
        if not db.get(RadioStation, body.radio_station_id):
            raise HTTPException(status_code=404, detail="Radio station not found")

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
    return _build_response(pitch)


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
    return [_build_response(p) for p in pitches]


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
    return _build_response(pitch)
