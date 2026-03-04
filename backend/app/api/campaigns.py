import logging
from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.campaign import Campaign, Expense
from app.models.song import Song
from app.models.user import User
from app.services.budget_recommender import BudgetRecommender
from app.utils.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(tags=["campaigns"])

ExpenseCategory = Literal[
    "playlist_pitching", "social_ads", "content", "radio_promotion",
    "submithub", "pr", "other"
]

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class SongBrief(BaseModel):
    id: int
    title: str
    artist_name: str
    model_config = {"from_attributes": True}


class CampaignCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    release_type: Literal["single", "ep", "album"]
    start_date: date
    end_date: date
    budget_total: float = Field(..., gt=0)
    primary_goal: Literal["awareness", "growth", "monetization"] | None = None
    notes: str | None = None
    song_ids: list[int] = []


class CampaignUpdate(BaseModel):
    name: str | None = None
    status: Literal["planning", "active", "completed"] | None = None
    notes: str | None = None
    primary_goal: Literal["awareness", "growth", "monetization"] | None = None


class CampaignResponse(BaseModel):
    id: int
    name: str
    release_type: str
    start_date: date
    end_date: date
    budget_total: float
    budget_spent: float
    primary_goal: str | None
    status: str
    budget_recommendation: dict | None
    notes: str | None
    songs: list[SongBrief]
    created_at: datetime
    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_campaign(cls, c: Campaign) -> "CampaignResponse":
        return cls(
            id=c.id,
            name=c.name,
            release_type=c.release_type,
            start_date=c.start_date,
            end_date=c.end_date,
            budget_total=float(c.budget_total),
            budget_spent=float(c.budget_spent),
            primary_goal=c.primary_goal,
            status=c.status,
            budget_recommendation=c.budget_recommendation,
            notes=c.notes,
            songs=[SongBrief(id=s.id, title=s.title, artist_name=s.artist_name) for s in c.songs],
            created_at=c.created_at,
        )


class ExpenseCreate(BaseModel):
    expense_date: date
    amount: float = Field(..., gt=0)
    category: ExpenseCategory
    subcategory: str | None = None
    description: str | None = None


class ExpenseResponse(BaseModel):
    id: int
    campaign_id: int
    expense_date: date
    amount: float
    category: str
    subcategory: str | None
    description: str | None
    created_at: datetime

    @classmethod
    def from_orm(cls, e: Expense) -> "ExpenseResponse":
        return cls(
            id=e.id,
            campaign_id=e.campaign_id,
            expense_date=e.expense_date,
            amount=float(e.amount),
            category=e.category,
            subcategory=e.subcategory,
            description=e.description,
            created_at=e.created_at,
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_campaign_or_404(campaign_id: int, user: User, db: Session) -> Campaign:
    c = db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.user_id == user.id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return c


# ---------------------------------------------------------------------------
# Campaign endpoints
# ---------------------------------------------------------------------------

@router.post("/campaigns", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    body: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    songs = []
    for sid in body.song_ids:
        song = db.query(Song).filter(Song.id == sid, Song.user_id == current_user.id).first()
        if not song:
            raise HTTPException(status_code=404, detail=f"Song {sid} not found")
        songs.append(song)

    campaign = Campaign(
        user_id=current_user.id,
        name=body.name,
        release_type=body.release_type,
        start_date=body.start_date,
        end_date=body.end_date,
        budget_total=Decimal(str(body.budget_total)),
        primary_goal=body.primary_goal,
        notes=body.notes,
        songs=songs,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    logger.info(f"Created campaign id={campaign.id} for user={current_user.id}")
    return CampaignResponse.from_orm_campaign(campaign)


@router.get("/campaigns", response_model=list[CampaignResponse])
def list_campaigns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    campaigns = (
        db.query(Campaign)
        .filter(Campaign.user_id == current_user.id)
        .order_by(Campaign.created_at.desc())
        .all()
    )
    return [CampaignResponse.from_orm_campaign(c) for c in campaigns]


@router.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return CampaignResponse.from_orm_campaign(_get_campaign_or_404(campaign_id, current_user, db))


@router.patch("/campaigns/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: int,
    body: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    c = _get_campaign_or_404(campaign_id, current_user, db)
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(c, field, value)
    db.commit()
    db.refresh(c)
    return CampaignResponse.from_orm_campaign(c)


@router.delete("/campaigns/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    c = _get_campaign_or_404(campaign_id, current_user, db)
    db.delete(c)
    db.commit()


# ---------------------------------------------------------------------------
# Budget recommendation
# ---------------------------------------------------------------------------

@router.post("/campaigns/{campaign_id}/budget-recommendation")
def budget_recommendation(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    c = _get_campaign_or_404(campaign_id, current_user, db)
    recommender = BudgetRecommender()
    rec = recommender.generate(c, c.songs)
    c.budget_recommendation = rec
    db.commit()
    logger.info(f"Budget recommendation generated for campaign_id={campaign_id}")
    return rec


# ---------------------------------------------------------------------------
# Expense endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/campaigns/{campaign_id}/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_expense(
    campaign_id: int,
    body: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    c = _get_campaign_or_404(campaign_id, current_user, db)
    expense = Expense(
        campaign_id=c.id,
        user_id=current_user.id,
        expense_date=body.expense_date,
        amount=Decimal(str(body.amount)),
        category=body.category,
        subcategory=body.subcategory,
        description=body.description,
    )
    db.add(expense)

    # Update budget_spent on the campaign
    c.budget_spent = Decimal(str(float(c.budget_spent) + body.amount))
    db.commit()
    db.refresh(expense)
    logger.info(f"Expense ${body.amount} added to campaign_id={campaign_id}")
    return ExpenseResponse.from_orm(expense)


@router.get("/campaigns/{campaign_id}/expenses", response_model=list[ExpenseResponse])
def list_expenses(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_campaign_or_404(campaign_id, current_user, db)
    expenses = (
        db.query(Expense)
        .filter(Expense.campaign_id == campaign_id)
        .order_by(Expense.expense_date.desc())
        .all()
    )
    return [ExpenseResponse.from_orm(e) for e in expenses]
