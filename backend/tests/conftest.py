"""
Shared pytest fixtures for all tests.

Uses SQLite in-memory so tests run with zero external dependencies.
Production uses PostgreSQL; the ORM abstracts the difference for all
features we currently test.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models.playlist import Playlist
from app.models.pitch_submission import PitchSubmission  # noqa: F401 — registers table
from app.models.generated_content import GeneratedContent  # noqa: F401 — registers table
from app.models.campaign import Campaign, Expense  # noqa: F401 — registers tables
from app.models.submithub import SubmitHubCampaign, SubmitHubSubmission  # noqa: F401 — registers tables
from app.models.dashboard import DashboardSnapshot, Insight  # noqa: F401 — registers tables
from app.models.post_opportunity import PostOpportunity  # noqa: F401 — registers table
from app.models.youtube_brief import YouTubeBrief, YouTubeBriefStat  # noqa: F401 — registers tables
from app.models.creation_entry import CreationEntry  # noqa: F401 — registers table
from app.models.user_progress import UserProgress  # noqa: F401 — registers table
from app.models.radio_station import RadioStation
from app.models.song import Song
from app.models.user import User
from app.utils.auth import create_access_token, hash_password
from main import app

SQLITE_URL = "sqlite:///:memory:"


# ---------------------------------------------------------------------------
# Database fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def engine():
    """In-memory SQLite engine; tables created once per session."""
    _engine = create_engine(
        SQLITE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # single connection reused across threads
    )
    Base.metadata.create_all(bind=_engine)
    yield _engine
    Base.metadata.drop_all(bind=_engine)


@pytest.fixture()
def db(engine):
    """
    DB session rolled back after each test — fast, isolated, no data leaks.
    """
    connection = engine.connect()
    transaction = connection.begin()
    TestSession = sessionmaker(bind=connection)
    session = TestSession()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# ---------------------------------------------------------------------------
# App / HTTP fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def client(db):
    """TestClient with get_db overridden to use the per-test session."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Data fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def sample_user(db) -> User:
    user = User(
        email="test@example.com",
        hashed_password=hash_password("password123"),
        name="Test User",
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture()
def auth_headers(sample_user: User) -> dict:
    token = create_access_token(sample_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def sample_song(db, sample_user) -> Song:
    from datetime import date
    song = Song(
        user_id=sample_user.id,
        spotify_track_id="4iV5W9uYEdYUVa79Axb7Rh",
        title="Test Song",
        artist_name="Test Artist",
        album_name="Test Album",
        release_date=date(2024, 1, 15),
        duration_ms=210000,
        spotify_url="https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh",
        popularity=65,
    )
    db.add(song)
    db.flush()
    return song


@pytest.fixture()
def sample_playlist(db) -> Playlist:
    playlist = Playlist(
        name="Israeli Indie",
        spotify_id="test_spotify_playlist_id",
        curator_name="Test Curator",
        curator_contact="curator@example.com",
        follower_count=2100,
        genres=["indie", "alternative"],
        languages=["hebrew"],
        mood_tags=["melancholic", "upbeat"],
        submission_method="email",
        is_active=True,
    )
    db.add(playlist)
    db.flush()
    return playlist


@pytest.fixture()
def sample_radio_station(db) -> RadioStation:
    station = RadioStation(
        name="Kan 88",
        name_hebrew="כאן 88",
        station_type="national",
        contact_email="88music@kan.org.il",
        genres_focus=["indie", "alternative", "world"],
        best_for=["new artists", "indie", "alternative"],
        submission_guidelines="Email MP3 + bio to 88music@kan.org.il",
        response_time="2-4 weeks",
        reach_description="National broadcast — ~200k weekly listeners",
    )
    db.add(station)
    db.flush()
    return station
