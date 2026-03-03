import logging
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.playlists import PlaylistResponse
from app.api.radio_stations import RadioStationResponse
from app.database import get_db
from app.models.playlist import Playlist
from app.models.radio_station import RadioStation
from app.models.song import Song
from app.models.user import User
from app.services.playlist_matcher import score_playlist, score_radio_station
from app.services.spotify import SpotifyService, parse_spotify_track_id
from app.utils.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/songs", tags=["songs"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class SongCreate(BaseModel):
    spotify_url: str
    story: str | None = None
    mood_tags: list[str] | None = None
    themes: list[str] | None = None
    comparable_artists: list[str] | None = None

    @field_validator("spotify_url")
    @classmethod
    def validate_spotify_url(cls, v: str) -> str:
        try:
            parse_spotify_track_id(v)
        except ValueError as e:
            raise ValueError(str(e)) from e
        return v


class SongUpdate(BaseModel):
    story: str | None = None
    mood_tags: list[str] | None = None
    themes: list[str] | None = None
    comparable_artists: list[str] | None = None
    genre: str | None = None
    language: str | None = None


class SongResponse(BaseModel):
    id: int
    spotify_track_id: str
    title: str
    artist_name: str
    album_name: str | None
    release_date: date | None
    duration_ms: int | None
    spotify_url: str | None
    album_image_url: str | None
    popularity: int | None
    story: str | None
    mood_tags: list | None
    themes: list | None
    comparable_artists: list | None
    genre: str | None
    language: str | None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("", response_model=SongResponse, status_code=status.HTTP_201_CREATED)
def create_song(
    body: SongCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    track_id = parse_spotify_track_id(body.spotify_url)
    logger.info(f"Creating song track_id={track_id} for user={current_user.id}")

    spotify = SpotifyService()
    try:
        metadata = spotify.get_track_metadata(track_id)
    except Exception as e:
        logger.error(f"Spotify fetch failed for {track_id}: {e}", exc_info=True)
        raise HTTPException(status_code=502, detail="Could not fetch track from Spotify")

    # Normalise release_date to a Python date object (Spotify returns strings like "2024-01-15")
    raw_date = metadata.get("release_date")
    if isinstance(raw_date, str):
        try:
            metadata["release_date"] = date.fromisoformat(raw_date[:10])
        except ValueError:
            metadata["release_date"] = None

    song = Song(
        user_id=current_user.id,
        **metadata,
        story=body.story,
        mood_tags=body.mood_tags,
        themes=body.themes,
        comparable_artists=body.comparable_artists,
    )

    try:
        # Use a savepoint so an IntegrityError doesn't roll back the outer transaction
        with db.begin_nested():
            db.add(song)
            db.flush()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Song already exists in your catalog")

    db.commit()
    db.refresh(song)
    logger.info(f"Song created id={song.id} title={song.title!r}")
    return song


@router.get("", response_model=list[SongResponse])
def list_songs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    songs = db.query(Song).filter(Song.user_id == current_user.id).all()
    logger.info(f"Listed {len(songs)} songs for user={current_user.id}")
    return songs


@router.get("/{song_id}", response_model=SongResponse)
def get_song(
    song_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    song = db.query(Song).filter(Song.id == song_id, Song.user_id == current_user.id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.patch("/{song_id}", response_model=SongResponse)
def update_song(
    song_id: int,
    body: SongUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    song = db.query(Song).filter(Song.id == song_id, Song.user_id == current_user.id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    updates = body.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(song, field, value)

    db.commit()
    db.refresh(song)
    logger.info(f"Updated song id={song_id} fields={list(updates.keys())} for user={current_user.id}")
    return song


@router.delete("/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_song(
    song_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    song = db.query(Song).filter(Song.id == song_id, Song.user_id == current_user.id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    db.delete(song)
    db.commit()
    logger.info(f"Deleted song id={song_id} for user={current_user.id}")


# ---------------------------------------------------------------------------
# Match endpoint
# ---------------------------------------------------------------------------

class PlaylistMatchEntry(BaseModel):
    playlist: PlaylistResponse
    score: int
    reasons: list[str]


class RadioStationMatchEntry(BaseModel):
    station: RadioStationResponse
    recommended: bool


class MatchResponse(BaseModel):
    playlists: list[PlaylistMatchEntry]
    radio_stations: list[RadioStationMatchEntry]


@router.get("/{song_id}/matches", response_model=MatchResponse)
def get_matches(
    song_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    song = db.query(Song).filter(Song.id == song_id, Song.user_id == current_user.id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    playlists = db.query(Playlist).filter(Playlist.is_active == True).all()  # noqa: E712
    playlist_entries = []
    for pl in playlists:
        sc, reasons = score_playlist(song, pl)
        playlist_entries.append(PlaylistMatchEntry(playlist=pl, score=sc, reasons=reasons))
    playlist_entries.sort(key=lambda e: e.score, reverse=True)

    stations = db.query(RadioStation).all()
    station_entries = []
    for st in stations:
        _label, recommended = score_radio_station(song, st)
        station_entries.append(RadioStationMatchEntry(station=st, recommended=recommended))

    logger.info(f"Matches computed for song_id={song_id} user={current_user.id}")
    return MatchResponse(playlists=playlist_entries, radio_stations=station_entries)
