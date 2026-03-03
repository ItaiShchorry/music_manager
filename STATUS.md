# Project Status - Music Promotion Tool

**Last Updated:** 2026-03-03

**Current Phase:** Week 3 Complete — Component 2 (Israeli Playlist & Radio Discovery) end-to-end

**Active Branch:** `week3`

---

## Quick Stats

- **Total Components:** 6 planned, 1.5 fully implemented (Component 1 + Component 2 backend/frontend)
- **Backend Endpoints:** 16 implemented (3 auth + 6 songs + 1 playlists + 1 radio-stations + 3 pitches + 1 match + health)
- **Frontend Pages:** 5 (Login, Songs list, Add Song, Song detail/edit, Discover)
- **Database Tables (ORM):** 5 defined (`users`, `songs`, `playlists`, `radio_stations`, `pitch_submissions`)
- **Tests Written:** 64 passing, 0 failing
- **Seed Data:** 25 Israeli playlists + 6 radio stations
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
│   ├── main.py               ✅ FastAPI app, CORS, 5 routers
│   ├── requirements.txt      ✅ All deps pinned for Python 3.13
│   ├── pytest.ini            ✅ asyncio_mode=auto, testpaths=tests
│   ├── alembic.ini           ✅ Configured (DB URL via env.py)
│   ├── .env.example          ✅ All required env vars documented
│   ├── alembic/
│   │   ├── env.py            ✅ Wired to all 5 models
│   │   └── versions/         ⏳ No migrations run yet (SQLite locally)
│   ├── app/
│   │   ├── config.py         ✅ pydantic-settings, reads .env
│   │   ├── database.py       ✅ SQLAlchemy engine + get_db
│   │   ├── api/
│   │   │   ├── auth.py       ✅ /register, /login, /me
│   │   │   ├── songs.py      ✅ Full CRUD + PATCH + GET /{id}/matches
│   │   │   ├── playlists.py  ✅ GET /playlists (language + genre filter)
│   │   │   ├── radio_stations.py ✅ GET /radio-stations
│   │   │   └── pitches.py    ✅ POST + GET /songs/{id}/pitches + PATCH
│   │   ├── models/
│   │   │   ├── user.py       ✅
│   │   │   ├── song.py       ✅ + genre, language fields (Week 3)
│   │   │   ├── playlist.py   ✅ Week 3
│   │   │   ├── radio_station.py ✅ Week 3
│   │   │   └── pitch_submission.py ✅ Week 3
│   │   ├── services/
│   │   │   ├── spotify.py    ✅ parse_spotify_track_id() + SpotifyService
│   │   │   ├── seed.py       ✅ seed_playlists() + seed_radio_stations()
│   │   │   └── playlist_matcher.py ✅ score_playlist() + score_radio_station()
│   │   └── utils/
│   │       ├── auth.py       ✅ JWT + bcrypt (no passlib)
│   │       └── logging_config.py ✅ Rotating file + console handler
│   ├── logs/                 ✅ Created (.gitkeep)
│   └── tests/
│       ├── conftest.py       ✅ SQLite fixtures + sample_playlist, sample_radio_station
│       ├── integration/
│       │   ├── test_us001_auth.py              ✅ 10 tests
│       │   ├── test_us002_songs.py             ✅ 19 tests
│       │   ├── test_us003_song_update.py       ✅ 7 tests
│       │   ├── test_us003b_song_genre_language.py ✅ 10 tests (Week 3)
│       │   ├── test_us004_playlist_match.py    ✅ 5 tests (Week 3)
│       │   ├── test_us005_playlists.py         ✅ 6 tests (Week 3)
│       │   └── test_us006_pitches.py           ✅ 7 tests (Week 3)
│       └── unit/
│           └── test_us002_spotify_url_parsing.py ✅ 9 tests
└── frontend/
    ├── index.html            ✅
    ├── package.json          ✅ React 18, Vite, TailwindCSS 3, TanStack Query
    ├── vite.config.ts        ✅ Proxy /api → localhost:8000
    ├── tailwind.config.ts    ✅
    ├── tsconfig.json         ✅
    └── src/
        ├── main.tsx          ✅
        ├── App.tsx           ✅ + /discover route (Week 3)
        ├── index.css         ✅ Tailwind directives
        ├── vite-env.d.ts     ✅
        ├── types/index.ts    ✅ + Playlist, RadioStation, MatchResponse, PitchSubmission
        ├── api/
        │   ├── client.ts     ✅ Axios + JWT interceptor + 401 redirect
        │   ├── auth.ts       ✅ login(), getMe()
        │   ├── songs.ts      ✅ + genre/language in updateSong patch type
        │   ├── playlists.ts  ✅ listPlaylists(), getMatchesForSong() (Week 3)
        │   └── pitches.ts    ✅ createPitch(), getPitchesForSong(), updatePitch() (Week 3)
        ├── hooks/
        │   └── useAuth.ts    ✅ Token lifecycle, user state, login/logout
        ├── components/
        │   ├── ProtectedRoute.tsx      ✅
        │   ├── Nav.tsx                 ✅ Songs | Discover nav bar (Week 3)
        │   ├── songs/
        │   │   └── SongCard.tsx        ✅
        │   └── discover/
        │       ├── PlaylistCard.tsx    ✅ Score badge + Mark Pitched modal (Week 3)
        │       └── RadioStationCard.tsx ✅ Recommended badge + pitch modal (Week 3)
        └── pages/
            ├── LoginPage.tsx           ✅
            ├── SongsPage.tsx           ✅ + Nav bar
            ├── SongNewPage.tsx         ✅
            ├── SongDetailPage.tsx      ✅ + genre/language fields + pitch history table
            └── DiscoverPage.tsx        ✅ Song selector → ranked playlists + radio (Week 3)
```

---

## Implementation Status by Component

### ✅ Completed

**Foundation**
- PRD.md v1.1, TECH_SPEC.md v1.0, backend boilerplate, test infrastructure

**US-001: Authentication** — 10 tests
- `POST /register` (single-user lock), `POST /login` (JWT), `GET /me`

**US-002: Song CRUD + Spotify Parsing** — 19 tests
- Full CRUD, Spotify metadata fetch, duplicate detection, URL/URI/ID parsing

**US-003: Song Update (Manual Fields)** — 7 tests
- `PATCH /songs/{id}` — story, mood_tags, themes, comparable_artists

**US-003b: Song Genre + Language** — 10 tests
- Extended `PATCH /songs/{id}` to accept `genre` (free text) and `language` (hebrew/english/both)
- Required for accurate playlist matching

**US-004: Playlist Match Algorithm** — 5 tests
- `GET /songs/{id}/matches` — scores all active playlists (0–100) and all radio stations
- Scoring: genre word overlap (40 pts) + language match (35 pts) + mood tag overlap (25 pts max)
- Radio stations: genre overlap → "Recommended" / "Secondary" / "Low match"
- Returns playlists sorted by score desc; bare songs (no profile) still get all playlists at 0

**US-005: Playlists + Radio Stations Listing** — 6 tests
- `GET /playlists?language=hebrew&genre=indie` — server-side filtering
- `GET /radio-stations` — full list, no filtering (small curated list)
- Seed data: 25 Israeli playlists + 6 stations loaded via `seed.py`

**US-006: Pitch Submission Tracking** — 7 tests
- `POST /pitches` — log a pitch (playlist or radio), defaults status="sent"
- `GET /songs/{song_id}/pitches` — history, ordered by pitched_date desc
- `PATCH /pitches/{id}` — update status (sent → responded → added / rejected / no_response)
- Auth + song ownership enforced on all endpoints

**Frontend — Component 1 + 2 UI**
- `Nav.tsx` — persistent top nav: Songs | Discover
- `SongDetailPage` — added genre text input + language dropdown; pitch history table with inline status selector
- `DiscoverPage` — song selector → ranked playlist cards + radio station cards; "no profile" warning with link to detail page
- `PlaylistCard` — score % badge (green/yellow/gray), genre chips, reason tags, "Mark Pitched" modal with method selector
- `RadioStationCard` — "Recommended"/"Secondary" badge, genre chips, "Mark Pitched" modal
- `npm run build` passes with zero TypeScript errors

### ⏳ Not Started

**Week 4 — Component 6: Hebrew Content Generation**
- `POST /api/v1/songs/{id}/content` — Claude generates Instagram/Facebook/TikTok captions in Hebrew
- 3 tone variants per platform; character limit enforcement; Hebrew + English hashtag mix
- Frontend: content generation panel on SongDetailPage

**Week 5 — Component 3: SubmitHub Integration**
- SubmitHub campaign + submission models
- Budget allocation per submission
- `POST /api/v1/songs/{id}/submithub-submit`

**Week 6 — Component 4: Campaign & Budget Management**
- Campaign model, expense tracking
- `POST /api/v1/campaigns/{id}/budget-recommendation` — Claude generates budget split
- Budget pacing alerts

**Week 7 — Component 5: Dashboard + Insights Engine**
- Dashboard snapshot model
- Health score calculation (streams 30% + save_rate 25% + follower_conv 20% + playlists 15% + ROI 10%)
- `GET /api/v1/dashboard/health-score`

---

## Database Schema

### Defined (ORM models exist)
- `users` — id, email, hashed_password, name, is_active, created_at
- `songs` — id, user_id (FK), spotify_track_id (unique), title, artist_name, album_name, release_date, duration_ms, spotify_url, album_image_url, popularity, story, mood_tags (JSON), themes (JSON), comparable_artists (JSON), **genre**, **language**, created_at, updated_at
- `playlists` — id, name, spotify_id, curator_name, curator_contact, follower_count, genres (JSON), languages (JSON), mood_tags (JSON), submission_method, submission_guidelines, is_active, notes, created_at
- `radio_stations` — id, name, name_hebrew, station_type, contact_email, contact_phone, website, genres_focus (JSON), best_for (JSON), submission_guidelines, response_time, reach_description, notes, created_at
- `pitch_submissions` — id, song_id (FK), target_type, playlist_id (FK nullable), radio_station_id (FK nullable), pitched_date, pitch_method, status, response_date, response_notes, created_at

### Pending (defined in TECH_SPEC.md, not implemented)
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
- ✅ `PATCH /{id}` — update manual fields incl. genre + language
- ✅ `DELETE /{id}` — delete
- ✅ `GET /{id}/matches` — ranked playlist + radio station matches
- ✅ `GET /{id}/pitches` — pitch history for song

### Playlists (`/api/v1/playlists`)
- ✅ `GET /` — list all active, optional `?language=` and `?genre=` filters

### Radio Stations (`/api/v1/radio-stations`)
- ✅ `GET /` — list all

### Pitches (`/api/v1/pitches`)
- ✅ `POST /` — log a new pitch (playlist or radio)
- ✅ `PATCH /{id}` — update status / response notes

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
| `/discover` | DiscoverPage | ✅ Week 3 |
| `/campaigns` | — | ⏳ Week 5–6 |
| `/dashboard` | — | ⏳ Week 7 |

> **Note:** No registration page exists in the UI. Use Swagger at `localhost:8000/docs` → `POST /api/v1/auth/register`. One-time setup.

---

## Environment & Dev Setup

### Running locally

**Backend** (from `backend/`):
```powershell
# One-time: create the SQLite database (includes all 5 tables + seed data)
..\.venv\Scripts\python -c "
from app.database import engine, Base
import app.models.user, app.models.song
import app.models.playlist, app.models.radio_station, app.models.pitch_submission
Base.metadata.create_all(engine)
from app.database import SessionLocal
from app.services.seed import seed_playlists, seed_radio_stations
db = SessionLocal()
seed_playlists(db); seed_radio_stations(db); db.commit(); db.close()
"

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

### Running tests
```powershell
# from backend/
..\.venv\Scripts\python -m pytest tests/ -v         # all 64 tests
..\.venv\Scripts\python -m pytest tests/ -k "us004" # one user story
```

---

## Known Gotchas & Reminders

**Python 3.13 compatibility**
- `passlib[bcrypt]` crashes on Python 3.13 — we use `bcrypt` directly. Do not re-add passlib.
- `psycopg2-binary` requires `>=2.9.10` for Python 3.13 wheels.

**SQLite vs PostgreSQL**
- Tests use `sqlite:///:memory:` — no external DB needed.
- SQLite requires Python `date` objects, not strings. Always call `date.fromisoformat(raw[:10])`.
- Spotify `release_date` can be `"2024"`, `"2024-01"`, or `"2024-01-15"` — the `[:10]` slice handles all.

**SQLite transaction isolation in tests**
- Each test wraps in a DB transaction that rolls back after the test.
- Never call `db.rollback()` inside endpoint code — it rolls back the outer test transaction.
- Use `with db.begin_nested(): db.add(obj); db.flush()` to catch `IntegrityError` safely.

**Always commit after writes**
- `db.flush()` alone does NOT persist data — `db.commit()` required.
- Tests don't catch missing commits because the open test transaction keeps flushed data visible.

**Match algorithm design note**
- `score_playlist()` returns `(score: int, reasons: list[str])` — reasons are human-readable ("genre match", "language match", "mood match").
- `score_radio_station()` returns `(label: str, is_recommended: bool)` — simpler because it's a small fixed list.
- Song with no profile fields (genre=None, language=None, mood_tags=None) scores 0 on all playlists — this is intentional; the Discover page shows a warning with a link to edit the song profile.

**Seed data is idempotent**
- `seed_playlists(db)` and `seed_radio_stations(db)` skip if tables already have rows.
- Call them at startup or as a one-liner (see setup command above).

**Pitch ownership**
- `POST /pitches` validates that the song_id belongs to `current_user` — prevents pitching other users' songs.
- `PATCH /pitches/{id}` joins through Song to enforce the same ownership check.

**Single-user tool**
- Registration is locked after the first user. The 403 detail string contains "single-user" (tested).

**Spotify URL parsing**
- `parse_spotify_track_id()` handles: full URLs, query-param URLs, `spotify:track:` URIs, raw 22-char IDs.

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
- **Spotify auth:** Client Credentials flow (server-to-server) — no user OAuth needed
- **Match scoring:** genre word-overlap (not exact match) so "mainstream Hebrew pop" matches "hebrew pop" playlists
- **Radio scoring:** genre-overlap count only (2+ → Recommended, 1 → Secondary) — simpler than playlist scoring, appropriate for a small fixed list

---

## Observations & Lessons (Week 3)

**What worked well**
- TDD cycle was smooth: write tests → red → implement → green, no surprises
- The `score_playlist()` word-overlap approach (splitting genre string into words and checking if any word appears in each playlist genre tag) avoids brittle exact-string matching while remaining deterministic and testable
- Idempotent seed functions keep the test suite fast and the dev setup simple
- The `sample_playlist` + `sample_radio_station` fixtures in conftest give all test files a realistic baseline without hitting the seed data

**Decisions made during implementation**
- Match endpoint lives in `songs.py` (not a separate file) since it's a sub-resource of a song — keeps routing intuitive (`/songs/{id}/matches`)
- `PlaylistCard` and `RadioStationCard` each own their "Mark Pitched" modal state locally — no shared modal component needed at this scale
- The Discover page warns (amber text) when the selected song has no profile fields, with a direct link to the Song Detail page — better UX than silently returning all-zero scores
- `PitchRow` inline status dropdown: color-coded via a static map, no extra library needed

**Things to watch for in Week 4**
- Hebrew content generation (Component 6) will require mocking the Anthropic client in all tests — make sure the mock returns the right `content[0].text` structure
- The `claude-sonnet-4-20250514` model ID from CLAUDE.md should be used, not the generic alias

---

## Next Steps (Week 4)

1. **Component 6 — Hebrew Content Generation**
   - `POST /api/v1/songs/{id}/content` — Claude Sonnet 4 generates captions
   - 3 tone variants per platform (Instagram, Facebook, TikTok)
   - Character limits: Instagram 125–150, Facebook 40–80, TikTok 50–100
   - Hebrew + English hashtag mix (3–5 each)
   - Frontend: content generation panel on SongDetailPage or new tab

2. **Seed data wiring** — call `seed_playlists` + `seed_radio_stations` from app lifespan in `main.py` so a freshly initialised DB auto-populates
