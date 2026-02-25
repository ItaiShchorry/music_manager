# Project Status - Music Promotion Tool

**Last Updated:** 2026-02-25

**Current Phase:** Week 1 Complete — Backend Foundation + Auth + Song CRUD

**Active Branch:** `feature/setup-project-structure`

---

## Quick Stats

- **Total Components:** 6 planned, 1 partially implemented (Component 1 — backend only)
- **Backend Endpoints:** 7 implemented (3 auth + 4 songs)
- **Frontend Pages:** 0 (not started — Week 2)
- **Database Tables (ORM):** 2 defined (`users`, `songs`) — migrations pending DB setup
- **Tests Written:** 29 passing, 0 failing
- **Deployment Status:** Not deployed

---

## Project Structure

```
music_manager/
├── Claude.md                 ✅ Instructions + TDD workflow
├── STATUS.md                 ✅ This file
├── PRD.md                    ✅ v1.1 — Product requirements
├── TECH_SPEC.md              ✅ v1.0 — Full technical specification
├── docs/                     ✅ 6 component design docs
├── backend/
│   ├── main.py               ✅ FastAPI app, CORS, routers
│   ├── requirements.txt      ✅ All deps pinned for Python 3.13
│   ├── pytest.ini            ✅ asyncio_mode=auto, testpaths=tests
│   ├── alembic.ini           ✅ Configured (DB URL via env.py)
│   ├── .env.example          ✅ All required env vars documented
│   ├── alembic/
│   │   ├── env.py            ✅ Wired to models; ready for migrations
│   │   └── versions/         ⏳ No migrations run yet (no DB locally)
│   ├── app/
│   │   ├── config.py         ✅ pydantic-settings, reads .env
│   │   ├── database.py       ✅ SQLAlchemy engine + get_db
│   │   ├── api/
│   │   │   ├── auth.py       ✅ /register, /login, /me
│   │   │   └── songs.py      ✅ CRUD + Spotify metadata on create
│   │   ├── models/
│   │   │   ├── user.py       ✅ User ORM model
│   │   │   └── song.py       ✅ Song ORM model (Spotify + manual fields)
│   │   ├── services/
│   │   │   └── spotify.py    ✅ parse_spotify_track_id() + SpotifyService
│   │   └── utils/
│   │       ├── auth.py       ✅ JWT + bcrypt (no passlib)
│   │       └── logging_config.py ✅ Rotating file + console handler
│   ├── logs/                 ✅ Created (.gitkeep)
│   └── tests/
│       ├── conftest.py       ✅ SQLite in-memory fixtures
│       ├── integration/
│       │   ├── test_us001_auth.py   ✅ 10 tests
│       │   └── test_us002_songs.py  ✅ 10 tests
│       └── unit/
│           └── test_us002_spotify_url_parsing.py  ✅ 9 tests
└── frontend/
    └── src/                  ⏳ Empty — Week 2
```

---

## Implementation Status by Component

### ✅ Completed

**Foundation**
- PRD.md v1.1 — product requirements with TDD mandate
- TECH_SPEC.md v1.0 — full DB schema, all API endpoints, business logic algorithms
- Backend boilerplate — FastAPI + SQLAlchemy + Alembic + logging + config
- Test infrastructure — SQLite in-memory, rollback-per-test isolation

**US-001: Authentication**
- `POST /api/v1/auth/register` — creates first user; blocks subsequent registrations (single-user lock)
- `POST /api/v1/auth/login` — OAuth2 password form, returns JWT
- `GET /api/v1/auth/me` — returns current user from JWT
- 10 tests: happy path, wrong password, non-existent user, single-user lock, invalid token

**US-002: Song CRUD + Spotify Parsing**
- `POST /api/v1/songs` — fetches Spotify metadata, stores with manual fields, deduplicates by track ID
- `GET /api/v1/songs` — lists all songs for authenticated user
- `GET /api/v1/songs/{id}` — get single song
- `DELETE /api/v1/songs/{id}` — delete song
- `parse_spotify_track_id()` — accepts full URL, URI (`spotify:track:id`), query-param URLs, or raw 22-char ID
- 19 tests: URL parsing (4 valid + 5 invalid), CRUD (happy paths + auth + 409 duplicate + 404)

### ⏳ Not Started

**Week 2 — Frontend scaffold + Song update (manual fields)**
- `PATCH /api/v1/songs/{id}` — update story, mood_tags, themes, comparable_artists
- React + Vite + TailwindCSS setup
- Login page, Songs list page, Song detail/edit page

**Week 3 — Component 2: Israeli Playlist & Radio Discovery**
- Playlist model + seed data (Israeli playlists + Galei Tzahal)
- Playlist match algorithm (genre/mood/language scoring)
- `GET /api/v1/playlists` + `GET /api/v1/playlists/match/{song_id}`
- Pitch submission tracking

**Week 4 — Component 3: SubmitHub Integration**
- SubmitHub campaign + submission models
- Budget allocation per submission

**Week 5 — Component 4: Campaign & Budget Management**
- Campaign model, expense tracking
- `POST /api/v1/campaigns/{id}/budget-recommendation` — Claude generates budget split
- Budget pacing alerts

**Week 6 — Component 5: Dashboard + Insights Engine**
- Dashboard snapshot model
- Health score calculation (streams 30% + save_rate 25% + follower_conv 20% + playlists 15% + ROI 10%)
- `GET /api/v1/dashboard/health-score`

**Week 7 — Component 6: Post Opportunity Engine**
- Signal detection (milestones, playlist adds, inactivity, Israeli calendar)
- `POST /api/v1/opportunities/generate` — Claude suggests post angles
- Not a caption writer — surfaces *what* to write about, not the post itself

---

## Database Schema

### Defined (ORM models exist, no migration run yet)
- `users` — id, email, hashed_password, name, is_active, created_at
- `songs` — id, user_id (FK), spotify_track_id (unique), title, artist_name, album_name, release_date, duration_ms, spotify_url, album_image_url, popularity, story, mood_tags (JSON), themes (JSON), comparable_artists (JSON), created_at, updated_at

### Pending (defined in TECH_SPEC.md, not implemented)
- `playlists`, `radio_stations`, `pitch_submissions`
- `campaigns`, `campaign_songs`, `budget_recommendations`, `expenses`, `campaign_performance`
- `submithub_campaigns`, `submithub_submissions`
- `dashboard_snapshots`, `insights`, `post_opportunities`

---

## API Endpoints

### Authentication (`/api/v1/auth`)
- ✅ `POST /register` — single-user lock enforced
- ✅ `POST /login` — returns JWT
- ✅ `GET /me` — requires auth

### Songs (`/api/v1/songs`)
- ✅ `POST /` — create (fetches Spotify metadata)
- ✅ `GET /` — list all for user
- ✅ `GET /{id}` — get one
- ⏳ `PATCH /{id}` — update manual fields (Week 2)
- ✅ `DELETE /{id}` — delete

### All other endpoints — not started

---

## Frontend Pages

### Completed
_None — Week 2_

### Pending
- ⏳ `/login` + `/register`
- ⏳ `/songs` — catalog list
- ⏳ `/songs/new` — add song via Spotify URL
- ⏳ `/songs/{id}` — view + edit manual fields
- ⏳ `/playlists` — discovery + match
- ⏳ `/campaigns` — campaign management
- ⏳ `/dashboard` — health score + insights
- ⏳ `/opportunities` — post angle suggestions

---

## Environment & Dev Setup

### Runtime
- **Python:** 3.13.5 (in `.venv/` at project root)
- **Venv activate:** `.venv\Scripts\Activate.ps1`
- **Run server:** from `backend/` → `.venv/Scripts/uvicorn main:app --reload`
- **Run tests:** from `backend/` → `.venv/Scripts/python -m pytest tests/ -v`
- **PostgreSQL:** NOT installed locally — using SQLite in-memory for all tests

### Required `.env` (copy from `backend/.env.example`)
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/music_manager
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/music_manager_test
SECRET_KEY=<generate random>
SPOTIFY_CLIENT_ID=<from Spotify Dashboard>
SPOTIFY_CLIENT_SECRET=<from Spotify Dashboard>
ANTHROPIC_API_KEY=<from Anthropic Console>
```

### Running migrations (once PostgreSQL is available)
```powershell
cd backend
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

---

## Known Gotchas & Reminders

**Python 3.13 compatibility**
- `passlib[bcrypt]` crashes on Python 3.13 — we use `bcrypt` directly instead. Do not re-add passlib.
- `psycopg2-binary` requires `>=2.9.10` for Python 3.13 wheels.

**SQLite vs PostgreSQL in tests**
- Tests use `sqlite:///:memory:` — no external DB needed.
- SQLite requires Python `date` objects, not strings. Always call `date.fromisoformat(raw[:10])` when converting Spotify's `release_date` string before inserting.
- Spotify `release_date` can be `"2024"`, `"2024-01"`, or `"2024-01-15"` — the `[:10]` slice handles all safely.

**SQLite transaction isolation in tests**
- Each test wraps a DB transaction that is rolled back after the test.
- Never call `db.rollback()` directly inside endpoint code — it rolls back the outer test transaction and breaks subsequent operations.
- Use `with db.begin_nested(): db.add(obj); db.flush()` to catch `IntegrityError` safely with a savepoint.

**Single-user tool**
- Registration is locked after the first user is created. Intentional — this is a personal tool. The 403 response includes "single-user" in the detail string (tested explicitly).

**Spotify URL parsing**
- `parse_spotify_track_id()` in `app/services/spotify.py` handles: full URLs, query-param URLs, `spotify:track:` URIs, and raw 22-char IDs. Raises `ValueError` for anything else (album/artist URLs, wrong domains, empty input).
- Always use this function for validation — the Pydantic `field_validator` on `SongCreate` calls it automatically.

**Test mocking**
- All Spotify API calls are mocked in integration tests: `patch("app.api.songs.SpotifyService")`.
- All Anthropic calls must be mocked in future tests — never make real API calls in tests.

---

## Technical Decisions (Confirmed)

- **Password hashing:** `bcrypt` direct (not passlib) — Python 3.13 compatibility
- **Tests:** SQLite in-memory with `StaticPool` — zero external dependencies
- **JWT:** HS256 via `python-jose`, 7-day expiry
- **DB session in tests:** rollback-per-test via nested connection/transaction
- **Date normalisation:** Spotify returns string dates; we convert to `date` object at the API layer before passing to ORM
- **Duplicate protection:** `begin_nested()` savepoint on song create to catch `IntegrityError` cleanly

---

## Next Steps (Week 2)

1. `PATCH /api/v1/songs/{id}` — update manual fields (story, mood_tags, themes, comparable_artists) — TDD
2. Frontend scaffold: React 18 + Vite + TailwindCSS + React Router + TanStack Query
3. Login + Register pages (wire to `/api/v1/auth`)
4. Songs list page + Add Song page (wire to `/api/v1/songs`)
5. Song detail/edit page (wire to `PATCH /api/v1/songs/{id}`)
