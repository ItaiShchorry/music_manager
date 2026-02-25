# Project Status - Music Promotion Tool

**Last Updated:** 2026-02-25

**Current Phase:** Week 2 Complete — PATCH endpoint + Full Frontend (Component 1 end-to-end)

**Active Branch:** `feature/setup-project-structure`

---

## Quick Stats

- **Total Components:** 6 planned, 1 fully implemented end-to-end (Component 1)
- **Backend Endpoints:** 8 implemented (3 auth + 5 songs)
- **Frontend Pages:** 4 (Login, Songs list, Add Song, Song detail/edit)
- **Database Tables (ORM):** 2 defined (`users`, `songs`)
- **Tests Written:** 36 passing, 0 failing
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
│   │   └── versions/         ⏳ No migrations run yet (using SQLite locally)
│   ├── app/
│   │   ├── config.py         ✅ pydantic-settings, reads .env
│   │   ├── database.py       ✅ SQLAlchemy engine + get_db
│   │   ├── api/
│   │   │   ├── auth.py       ✅ /register, /login, /me
│   │   │   └── songs.py      ✅ Full CRUD + PATCH manual fields
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
│       │   ├── test_us001_auth.py          ✅ 10 tests
│       │   ├── test_us002_songs.py         ✅ 19 tests
│       │   └── test_us003_song_update.py   ✅ 7 tests
│       └── unit/
│           └── test_us002_spotify_url_parsing.py  ✅ 9 tests (5 invalid + 4 valid)
└── frontend/
    ├── index.html            ✅
    ├── package.json          ✅ React 18, Vite, TailwindCSS 3, TanStack Query
    ├── vite.config.ts        ✅ Proxy /api → localhost:8000
    ├── tailwind.config.ts    ✅
    ├── tsconfig.json         ✅
    └── src/
        ├── main.tsx          ✅
        ├── App.tsx           ✅ React Router v6, QueryClientProvider
        ├── index.css         ✅ Tailwind directives
        ├── vite-env.d.ts     ✅ import.meta.env types
        ├── types/index.ts    ✅ User, Song, LoginRequest, TokenResponse
        ├── api/
        │   ├── client.ts     ✅ Axios + JWT interceptor + 401 redirect
        │   ├── auth.ts       ✅ login(), getMe()
        │   └── songs.ts      ✅ listSongs, getSong, createSong, updateSong, deleteSong
        ├── hooks/
        │   └── useAuth.ts    ✅ Token lifecycle, user state, login/logout
        ├── components/
        │   ├── ProtectedRoute.tsx      ✅ Redirects to /login if no token
        │   └── songs/
        │       └── SongCard.tsx        ✅ Album art, title, artist, year
        └── pages/
            ├── LoginPage.tsx           ✅ react-hook-form + zod validation
            ├── SongsPage.tsx           ✅ TanStack Query grid + empty state + skeleton
            ├── SongNewPage.tsx         ✅ Spotify URL input + mutation
            └── SongDetailPage.tsx      ✅ Read-only metadata + editable manual fields
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

**US-003: Song Update (Manual Fields)**
- `PATCH /api/v1/songs/{id}` — partial update of story, mood_tags, themes, comparable_artists
- Uses `model_dump(exclude_unset=True)` — only fields sent in the request body are changed
- 7 tests: happy path, partial update, empty body, auth required, 404, other-user isolation

**Frontend — Component 1 UI**
- React 18 + Vite + TailwindCSS 3 + React Router v6 + TanStack Query + react-hook-form + zod
- API layer: axios client with JWT Bearer interceptor, 401 auto-redirects to /login
- `LoginPage` — email/password form, zod validation, stores token on success
- `SongsPage` — song grid, loading skeleton, empty state, "Add Song" button
- `SongNewPage` — Spotify URL input, imports metadata on submit, navigates to detail
- `SongDetailPage` — read-only Spotify metadata + editable story/tags/themes/comparable artists with chip-based tag input
- `SongCard` — reusable album art card
- `ProtectedRoute` — redirects unauthenticated users to /login
- `npm run build` passes with zero TypeScript errors

### ⏳ Not Started

**Week 3 — Component 2: Israeli Playlist & Radio Discovery**
- Playlist model + seed data (Israeli playlists + Galei Tzahal)
- Playlist match algorithm (genre/mood/language scoring)
- `GET /api/v1/playlists` + `GET /api/v1/playlists/match/{song_id}`
- Pitch submission tracking
- Frontend: `/playlists` page

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

### Defined (ORM models exist)
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
- ✅ `PATCH /{id}` — update manual fields (partial, exclude_unset)
- ✅ `DELETE /{id}` — delete

### All other endpoints — not started

---

## Frontend Routes

| Route | Page | Status |
|-------|------|--------|
| `/` | → redirect to `/songs` | ✅ |
| `/login` | LoginPage | ✅ |
| `/songs` | SongsPage | ✅ |
| `/songs/new` | SongNewPage | ✅ |
| `/songs/:id` | SongDetailPage | ✅ |
| `/playlists` | — | ⏳ Week 3 |
| `/campaigns` | — | ⏳ Week 4–5 |
| `/dashboard` | — | ⏳ Week 6 |
| `/opportunities` | — | ⏳ Week 7 |

> **Note:** No registration page exists in the UI. To create your account, use Swagger at `localhost:8000/docs` → `POST /api/v1/auth/register`. The single-user lock means this is a one-time step.

---

## Environment & Dev Setup

### Running locally

**Backend** (from `backend/`):
```powershell
# One-time: create the SQLite database
..\.venv\Scripts\python -c "from app.database import engine, Base; import app.models.user, app.models.song; Base.metadata.create_all(engine)"

# Start the server
..\.venv\Scripts\uvicorn main:app --reload
# → http://localhost:8000
# → http://localhost:8000/docs  (Swagger UI)
```

**Frontend** (from `frontend/`, use Git Bash):
```bash
npm run dev
# → http://localhost:5173
```

### Required `backend/.env`
```
DATABASE_URL=sqlite:///./music_manager.db
SECRET_KEY=<any long random string>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
SPOTIFY_CLIENT_ID=<from Spotify Developer Dashboard>
SPOTIFY_CLIENT_SECRET=<from Spotify Developer Dashboard>
ENVIRONMENT=development
LOG_LEVEL=INFO
```

> Spotify credentials: free at developer.spotify.com/dashboard — create an app, select "Web API", copy Client ID + Secret. Uses Client Credentials flow (no user OAuth, no redirect URI actually called).

### Running tests
```powershell
# from backend/
..\.venv\Scripts\python -m pytest tests/ -v         # all 36 tests
..\.venv\Scripts\python -m pytest tests/ -k "us003"  # one user story
```

### Windows notes
- Use **Git Bash** for `npm run dev` — PowerShell execution policy blocks `.ps1` scripts on corporate machines
- Python venv: activate with `.venv\Scripts\Activate.ps1` in PowerShell, or prefix commands with `..\.venv\Scripts\python`

---

## Known Gotchas & Reminders

**Python 3.13 compatibility**
- `passlib[bcrypt]` crashes on Python 3.13 — we use `bcrypt` directly. Do not re-add passlib.
- `psycopg2-binary` requires `>=2.9.10` for Python 3.13 wheels.

**SQLite vs PostgreSQL**
- Tests use `sqlite:///:memory:` — no external DB needed.
- Local dev uses `sqlite:///./music_manager.db` (created by the one-liner above).
- SQLite requires Python `date` objects, not strings. Always call `date.fromisoformat(raw[:10])` when converting Spotify's `release_date` before inserting.
- Spotify `release_date` can be `"2024"`, `"2024-01"`, or `"2024-01-15"` — the `[:10]` slice handles all safely.

**SQLite transaction isolation in tests**
- Each test wraps in a DB transaction that rolls back after the test.
- Never call `db.rollback()` inside endpoint code — it rolls back the outer test transaction.
- Use `with db.begin_nested(): db.add(obj); db.flush()` to catch `IntegrityError` safely.

**Always commit after writes**
- `db.flush()` alone does NOT persist data — session closes with a rollback if no `db.commit()`.
- Pattern: `with db.begin_nested(): db.add(obj); db.flush()` → catch IntegrityError → `db.commit(); db.refresh(obj)`.
- Tests don't catch missing commits because the test session's open transaction keeps flushed data visible.

**Single-user tool**
- Registration is locked after the first user. Intentional. The 403 detail string contains "single-user" (tested explicitly).

**Spotify URL parsing**
- `parse_spotify_track_id()` handles: full URLs, query-param URLs, `spotify:track:` URIs, raw 22-char IDs.
- Always use this — the Pydantic `field_validator` on `SongCreate` calls it automatically.

**Test mocking**
- All Spotify API calls are mocked: `patch("app.api.songs.SpotifyService")`.
- All Anthropic calls must be mocked in future tests — never make real API calls in tests.

---

## Technical Decisions (Confirmed)

- **Password hashing:** `bcrypt` direct (not passlib) — Python 3.13 compatibility
- **Tests:** SQLite in-memory with `StaticPool` — zero external dependencies
- **JWT:** HS256 via `python-jose`, 7-day expiry
- **DB session in tests:** rollback-per-test via nested connection/transaction
- **Date normalisation:** Spotify returns string dates; convert to `date` object at API layer before ORM
- **Duplicate protection:** `begin_nested()` savepoint on song create to catch `IntegrityError` cleanly
- **Partial updates:** `model_dump(exclude_unset=True)` on PATCH — only sent fields are written
- **Frontend state management:** TanStack Query for server state; local `useState` for form fields
- **Spotify auth:** Client Credentials flow (server-to-server) — no user OAuth, no redirect URI needed

---

## Next Steps (Week 3)

1. Component 2 — Israeli Playlist & Radio Discovery (backend TDD first)
2. Playlist seed data — curated list of Israeli playlists + Galei Tzahal stations
3. Match algorithm — score songs against playlists by genre/mood/language
4. Frontend — `/playlists` page with match results and pitch submission tracking
