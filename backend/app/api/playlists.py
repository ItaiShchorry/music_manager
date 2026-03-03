import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.playlist import Playlist
from app.models.user import User
from app.utils.auth import get_current_user
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/playlists", tags=["playlists"])


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class PlaylistResponse(BaseModel):
    id: int
    name: str
    spotify_id: str | None
    curator_name: str | None
    curator_contact: str | None
    follower_count: int | None
    genres: list | None
    languages: list | None
    mood_tags: list | None
    submission_method: str | None
    submission_guidelines: str | None
    is_active: bool
    notes: str | None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("", response_model=list[PlaylistResponse])
def list_playlists(
    language: str | None = Query(None),
    genre: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Playlist).filter(Playlist.is_active == True)  # noqa: E712
    playlists = query.all()

    if language:
        lang_lower = language.lower()
        playlists = [
            p for p in playlists
            if p.languages and any(lang_lower == l.lower() for l in p.languages)
        ]

    if genre:
        genre_lower = genre.lower()
        playlists = [
            p for p in playlists
            if p.genres and any(genre_lower in g.lower() for g in p.genres)
        ]

    logger.info(f"Listed {len(playlists)} playlists for user={current_user.id}")
    return playlists
