from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.utils.logging_config import setup_logging

setup_logging(settings.log_level)

import logging  # noqa: E402 — must come after setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting Music Manager API — environment={settings.environment}")
    # Seed lookup tables on first boot (idempotent — skips if rows already exist)
    from sqlalchemy.exc import OperationalError
    from app.database import SessionLocal
    from app.services.seed import seed_playlists, seed_radio_stations
    db = SessionLocal()
    try:
        seed_playlists(db)
        seed_radio_stations(db)
        db.commit()
    except OperationalError:
        # Tables not created yet (pre-migration) — seed will run after first migration
        logger.warning("Seed skipped: tables not found. Run migrations first.")
        db.rollback()
    finally:
        db.close()
    yield
    logger.info("Shutting down Music Manager API")


app = FastAPI(
    title="Music Manager API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from app.api import auth, pitches, playlists, radio_stations, songs  # noqa: E402

app.include_router(auth.router, prefix="/api/v1")
app.include_router(songs.router, prefix="/api/v1")
app.include_router(playlists.router, prefix="/api/v1")
app.include_router(radio_stations.router, prefix="/api/v1")
app.include_router(pitches.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
