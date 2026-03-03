import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.radio_station import RadioStation
from app.models.user import User
from app.utils.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/radio-stations", tags=["radio-stations"])


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class RadioStationResponse(BaseModel):
    id: int
    name: str
    name_hebrew: str | None
    station_type: str
    contact_email: str | None
    contact_phone: str | None
    website: str | None
    genres_focus: list | None
    best_for: list | None
    submission_guidelines: str | None
    response_time: str | None
    reach_description: str | None
    notes: str | None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("", response_model=list[RadioStationResponse])
def list_radio_stations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stations = db.query(RadioStation).all()
    logger.info(f"Listed {len(stations)} radio stations for user={current_user.id}")
    return stations
