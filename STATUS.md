# Project Status - Music Promotion Tool

**Last Updated:** 2026-03-06

**Current Phase:** Week 7 Complete — Creative Companion (US-016 through US-022)

**Active Branch:** `week7`

---

## Quick Stats

- **Total Components:** 9 implemented (6 core MVP + 3 Creative Companion)
- **Backend Endpoints:** 65+ implemented
- **Frontend Pages:** 10 (Login, Manager, Songs list, Add Song, Song detail/edit, Discover, Campaigns, Campaign detail, Dashboard, SubmitHub)
- **Database Tables (ORM):** 19 defined (`users`, `songs`, `playlists`, `radio_stations`, `pitch_submissions`, `generated_content`, `campaigns`, `campaign_songs`, `expenses`, `submithub_campaigns`, `submithub_submissions`, `dashboard_snapshots`, `insights`, `post_opportunities`, `youtube_briefs`, `youtube_brief_stats`, `creation_entries`, `user_progress`)
- **Tests Written:** 227 passing, 0 failing
- **Seed Data:** 25 Israeli playlists + 6 radio stations
- **Deployment Status:** Not deployed

---

## Project Structure

```
music_manager/
├── Claude.md                 ✅ Instructions + TDD workflow
├── STATUS.md                 ✅ This file
├── PRD.md                    ✅ v2.0 — Updated with Creative Companion vision
├── TECH_SPEC.md              ✅ v1.0 — Full technical specification
├── docs/                     ✅ 6 component design docs
├── backend/
│   ├── main.py               ✅ FastAPI app + 12 routers + StaticFiles /uploads
│   ├── requirements.txt      ✅ All deps pinned for Python 3.13
│   ├── pytest.ini            ✅ asyncio_mode=auto, testpaths=tests
│   ├── alembic.ini           ✅ Configured (DB URL via env.py)
│   ├── .env.example          ✅ All required env vars documented
│   ├── uploads/              ✅ User-uploaded files (gitignored content)
│   ├── alembic/
│   │   ├── env.py            ✅ Wired to all 19 models
│   │   └── versions/         ✅ 0001_week3_schema.py, 0002_generated_content.py
│   ├── app/
│   │   ├── config.py         ✅ pydantic-settings, reads .env
│   │   ├── database.py       ✅ SQLAlchemy engine + get_db
│   │   ├── api/
│   │   │   ├── auth.py       ✅ /register, /login, /me
│   │   │   ├── songs.py      ✅ Full CRUD + PATCH (incl. search_keywords) + matches
│   │   │   ├── playlists.py  ✅ GET /playlists (language + genre filter)
│   │   │   ├── radio_stations.py ✅ GET /radio-stations
│   │   │   ├── pitches.py    ✅ POST + GET /songs/{id}/pitches + PATCH
│   │   │   ├── content.py    ✅ POST + GET /songs/{id}/content
│   │   │   ├── campaigns.py  ✅ Campaign CRUD + budget recommendation + learnings
│   │   │   ├── submithub.py  ✅ SubmitHub campaign + submission tracking
│   │   │   ├── dashboard.py  ✅ Snapshots, health score, insights
│   │   │   ├── opportunities.py ✅ Generate + list + PATCH status (+ category field)
│   │   │   ├── youtube_briefs.py ✅ Full CRUD + lifecycle + stats (Week 7)
│   │   │   ├── challenges.py ✅ Complete challenge + file upload + list (Week 7)
│   │   │   └── progress.py   ✅ GET /me/progress (Week 7)
│   │   ├── models/
│   │   │   ├── user.py       ✅
│   │   │   ├── song.py       ✅ + search_keywords field (Week 7)
│   │   │   ├── playlist.py   ✅
│   │   │   ├── radio_station.py ✅
│   │   │   ├── pitch_submission.py ✅
│   │   │   ├── generated_content.py ✅
│   │   │   ├── campaign.py   ✅
│   │   │   ├── submithub.py  ✅
│   │   │   ├── dashboard.py  ✅
│   │   │   ├── post_opportunity.py ✅ + category field (Week 7)
│   │   │   ├── youtube_brief.py ✅ YouTubeBrief + YouTubeBriefStat (Week 7)
│   │   │   ├── creation_entry.py ✅ CreationEntry (Week 7)
│   │   │   └── user_progress.py ✅ UserProgress + compute_level() (Week 7)
│   │   ├── services/
│   │   │   ├── spotify.py    ✅
│   │   │   ├── seed.py       ✅
│   │   │   ├── playlist_matcher.py ✅
│   │   │   ├── content_generator.py ✅
│   │   │   ├── budget_recommender.py ✅
│   │   │   ├── insight_generator.py ✅
│   │   │   ├── health_score.py ✅
│   │   │   ├── opportunity_service.py ✅ Redesigned: creative + YouTube signals + category (Week 7)
│   │   │   ├── youtube_brief_generator.py ✅ Claude-powered YouTube brief (Week 7)
│   │   │   └── progress_service.py ✅ Streak + level + badge logic (Week 7)
│   │   └── utils/
│   │       ├── auth.py       ✅ JWT + bcrypt (no passlib)
│   │       └── logging_config.py ✅ Rotating file + console handler
│   ├── logs/                 ✅ Created (.gitkeep)
│   └── tests/
│       ├── conftest.py       ✅ SQLite fixtures (all 19 models imported)
│       ├── integration/
│       │   ├── test_us001_auth.py              ✅ 10 tests
│       │   ├── test_us002_songs.py             ✅ 19 tests
│       │   ├── test_us003_song_update.py       ✅ 7 tests
│       │   ├── test_us003b_song_genre_language.py ✅ 10 tests
│       │   ├── test_us004_playlist_match.py    ✅ 5 tests
│       │   ├── test_us005_playlists.py         ✅ 6 tests
│       │   ├── test_us006_pitches.py           ✅ 7 tests
│       │   ├── test_us007_content_generation.py ✅ 13 tests
│       │   ├── test_us008_campaigns.py         ✅ (Week 5)
│       │   ├── test_us009_submithub.py         ✅ (Week 5)
│       │   ├── test_us011_dashboard.py         ✅ (Week 6)
│       │   ├── test_us014_opportunities.py     ✅ (Week 6)
│       │   ├── test_us018_search_keywords.py   ✅ 5 tests (Week 7)
│       │   ├── test_us016_youtube_brief_generate.py ✅ 8 tests (Week 7)
│       │   ├── test_us017_youtube_brief_lifecycle.py ✅ 11 tests (Week 7)
│       │   ├── test_us019_creative_opportunity_engine.py ✅ 11 tests (Week 7)
│       │   ├── test_us021_challenge_completion.py ✅ 7 tests (Week 7)
│       │   └── test_us022_user_progress.py     ✅ 14 tests (Week 7)
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
        ├── App.tsx           ✅ / → /manager, /manager route added (Week 7)
        ├── index.css         ✅ Tailwind directives
        ├── vite-env.d.ts     ✅
        ├── types/index.ts    ✅ + YouTubeBrief, CreationEntry, UserProgress, updated PostOpportunity + Song (Week 7)
        ├── api/
        │   ├── client.ts     ✅ Axios + JWT interceptor + 401 redirect
        │   ├── auth.ts       ✅
        │   ├── songs.ts      ✅ + search_keywords (Week 7)
        │   ├── playlists.ts  ✅
        │   ├── pitches.ts    ✅
        │   ├── content.ts    ✅
        │   ├── campaigns.ts  ✅
        │   ├── dashboard.ts  ✅
        │   ├── opportunities.ts ✅
        │   ├── youtube.ts    ✅ Full YouTube brief API (Week 7)
        │   ├── challenges.ts ✅ Complete challenge + upload (Week 7)
        │   └── progress.ts   ✅ getProgress() (Week 7)
        ├── hooks/
        │   └── useAuth.ts    ✅
        ├── components/
        │   ├── ProtectedRoute.tsx      ✅
        │   ├── Nav.tsx                 ✅ Manager link (Week 7)
        │   ├── songs/
        │   │   └── SongCard.tsx        ✅
        │   ├── discover/
        │   │   ├── PlaylistCard.tsx    ✅
        │   │   └── RadioStationCard.tsx ✅
        │   ├── content/
        │   │   └── ContentPanel.tsx    ✅
        │   ├── opportunities/
        │   │   └── OpportunityCard.tsx ✅ Category-aware styling: creative/youtube/promotion (Week 7)
        │   ├── progress/
        │   │   └── ProgressWidget.tsx  ✅ Level + streak + badges (Week 7)
        │   ├── youtube/
        │   │   ├── YouTubeBriefPanel.tsx ✅ Generate + list briefs per song (Week 7)
        │   │   ├── YouTubeBriefCard.tsx  ✅ Expandable card + status lifecycle (Week 7)
        │   │   └── YouTubeQueueWidget.tsx ✅ In-progress briefs dashboard widget (Week 7)
        │   └── challenges/
        │       ├── ChallengeMode.tsx   ✅ Full-screen overlay (Week 7)
        │       └── CelebrationScreen.tsx ✅ Confetti + level + share (Week 7)
        └── pages/
            ├── LoginPage.tsx           ✅
            ├── ManagerPage.tsx         ✅ CREATE / SHARE / TRACK pillars (Week 7)
            ├── SongsPage.tsx           ✅
            ├── SongNewPage.tsx         ✅
            ├── SongDetailPage.tsx      ✅ + search_keywords TagInput + YouTubeBriefPanel (Week 7)
            ├── DiscoverPage.tsx        ✅
            ├── CampaignsPage.tsx       ✅
            ├── CampaignDetailPage.tsx  ✅
            ├── DashboardPage.tsx       ✅
            └── SubmitHubPage.tsx       ✅
```

---

## Implementation Status by Component

### ✅ Completed (US-001–015, Week 3–6)

**US-001: Authentication** — 10 tests
- `POST /register` (single-user lock), `POST /login` (JWT), `GET /me`

**US-002: Song CRUD + Spotify Parsing** — 19 tests
- Full CRUD, Spotify metadata fetch, duplicate detection, URL/URI/ID parsing

**US-003/003b: Song Update + Genre/Language** — 17 tests
- `PATCH /songs/{id}` — story, mood_tags, themes, comparable_artists, genre, language

**US-004: Playlist Match Algorithm** — 5 tests
- `GET /songs/{id}/matches` — scores all playlists + radio stations (0–100)

**US-005: Playlists + Radio Stations Listing** — 6 tests
- `GET /playlists?language=&genre=`, `GET /radio-stations`

**US-006: Pitch Submission Tracking** — 7 tests
- Pitch log per song, status updates (sent → added/rejected/no_response)

**US-007: Hebrew Content Generation** — 13 tests
- Claude generates social captions per tone + platform (Instagram/Facebook/TikTok)

**US-008–010: Campaign & Budget Management** — 18 tests
- Campaign CRUD, expense tracking, AI budget recommendations, apply learnings

**US-009: SubmitHub Integration** — 12 tests
- SubmitHub campaign planning + per-curator submission tracking, AI pitch brief

**US-011–013: Dashboard + Insights Engine** — 21 tests
- Manual Spotify data sync, health score (0–100), AI insights (Claude)

**US-014–015: Post Opportunity Suggestions** — 16 tests
- AI-generated post idea cards: stream milestones, playlist adds, inactivity, holidays
- Status lifecycle: used / dismissed / remind_later

### ✅ Completed (US-016–022, Week 7 — Creative Companion)

**US-016: YouTube Video Brief Generator** — 8 tests
- `POST /songs/{id}/youtube-briefs` — Claude generates SEO title, hook paragraph, chapters (3–5), description, tags
- Concept types: making_of | acoustic_session | production_breakdown | song_explained | live_performance
- Fallback placeholder when Claude fails; search_keywords included in prompt
- Multiple briefs per song allowed; status defaults to 'draft'

**US-017: Brief Lifecycle Management** — 11 tests
- Status transitions: draft → planned → filmed → published
- `filmed_at` auto-set on →filmed; `published_at` auto-set on →published
- `youtube_url` required + validated (youtu.be / youtube.com) when publishing → 422 without it
- `POST /youtube-briefs/{id}/stats` — log views/likes/comments/subscribers_gained (upsert per date)
- `GET /youtube-briefs` — list all user's briefs with optional `?status=` filter

**US-018: SEO Search Keywords on Song** — 5 tests
- `search_keywords: list[str] | null` field on Song model
- Included in `PATCH /songs/{id}` and `SongResponse`
- Empty list `[]` normalized to `null` at API layer
- Exposed in `SongDetailPage` as a TagInput (same UX as mood_tags)
- Passed to YouTubeBriefGenerator for use in video_description

**US-019: Creative Opportunity Engine** — 11 tests
- New `category` field on PostOpportunity: `'creative'` | `'youtube'` | `'promotion'`
- **6 new creative signal types** (category='creative'): lyric_prompt, catalog_gap, style_exploration, instrumental_challenge, song_experiment, cover_idea
- **4 new YouTube signal types** (category='youtube'): story_ready, no_video, youtube_milestone, brief_filmed_unpublished
- Redesigned Claude prompt: role as creative manager + full catalog context + diversity axes
- `OpportunityCard` updated: creative=amber ("Accept Challenge"), youtube=red ("Plan Video"), promotion=indigo ("Use This")

**US-021: Challenge Completion Flow** — 7 tests
- `POST /challenges/{opportunity_id}/complete` — saves `CreationEntry`, marks opportunity 'used', updates `UserProgress`
- `POST /uploads` — multipart file upload; stored at `backend/uploads/{user_id}/{uuid}_{filename}`
- `GET /challenges` — list user's creations with optional `?status=` filter
- **ChallengeMode overlay** — full-screen challenge UI with text editor; completion triggers CelebrationScreen
- **CelebrationScreen** — shows level, streak, badges earned, auto-generated shareable caption with copy button

**US-022: User Progress & Gamification** — 14 tests
- `UserProgress` model: streak_current, streak_best, last_challenge_date, total_completed, level, badges (JSON)
- Level thresholds: newcomer (0–4) → emerging (5–14) → pro (15–29) → expert (30+)
- Badges: first_spark, three_day_streak, week_on_fire, ten_creations, publisher, youtube_debut
- Streak logic: yesterday → +1; today → no change; gap → reset to 1
- `GET /me/progress` — returns full progress object
- **ProgressWidget** — level badge + streak counter + progress bar + recent badge emojis

**US-020: Manager Homepage** — (frontend)
- `/` → `/manager` redirect; `/manager` is the new homepage
- **CREATE section** — 3 creative/youtube opportunity cards (quests) + YouTubeQueueWidget + ProgressWidget
- **SHARE section** — promotion cards + active campaign links
- **TRACK section** — health score card + AI insights + quick links

---

## Database Schema

### Tables (all 19 ORM models)

| Table | Description |
|-------|-------------|
| `users` | Auth — id, email, hashed_password, name |
| `songs` | Song profile — Spotify metadata + manual fields + `search_keywords` (Week 7) |
| `playlists` | 25 seeded Israeli playlists |
| `radio_stations` | 6 seeded Israeli stations |
| `pitch_submissions` | Pitch history per song |
| `generated_content` | Hebrew social captions (Claude) |
| `campaigns` | Release campaigns with budget |
| `campaign_songs` | Many-to-many association |
| `expenses` | Per-channel spend tracking |
| `submithub_campaigns` | SubmitHub campaign plans |
| `submithub_submissions` | Per-curator submission tracking |
| `dashboard_snapshots` | Daily Spotify metrics + health score |
| `insights` | AI-generated insight cards |
| `post_opportunities` | Post idea cards + `category` field (Week 7) |
| `youtube_briefs` | YouTube video briefs (Week 7) |
| `youtube_brief_stats` | Performance snapshots per brief (Week 7) |
| `creation_entries` | Challenge completion outputs (Week 7) |
| `user_progress` | Streak + level + badges per user (Week 7) |

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
- ✅ `PATCH /{id}` — update manual fields incl. genre, language, **search_keywords**
- ✅ `DELETE /{id}` — delete
- ✅ `GET /{id}/matches` — ranked playlist + radio station matches
- ✅ `GET /{id}/pitches` — pitch history for song
- ✅ `POST /{id}/content` — generate Hebrew social content (Claude)
- ✅ `GET /{id}/content` — list previously generated content
- ✅ `POST /{id}/youtube-briefs` — generate YouTube brief (Claude) (Week 7)
- ✅ `GET /{id}/youtube-briefs` — list briefs for song (Week 7)

### Playlists / Radio (`/api/v1/playlists`, `/api/v1/radio-stations`)
- ✅ `GET /playlists` — optional `?language=` and `?genre=` filters
- ✅ `GET /radio-stations` — full list

### Pitches (`/api/v1/pitches`)
- ✅ `POST /` — log a new pitch
- ✅ `PATCH /{id}` — update status / response notes

### Content (`/api/v1/songs/{id}/content`)
- ✅ `POST /` — generate Hebrew captions
- ✅ `GET /` — list generated content

### Campaigns (`/api/v1/campaigns`)
- ✅ Full CRUD + budget recommendation + apply learnings

### SubmitHub (`/api/v1/submithub-campaigns`)
- ✅ Campaign + submission CRUD + AI pitch brief

### Dashboard (`/api/v1/dashboard`)
- ✅ `POST /snapshots` — sync daily metrics
- ✅ `GET /health-score` — latest score + label
- ✅ `POST /insights/generate` — AI insight cards
- ✅ `GET /insights` — list active insights
- ✅ `PATCH /insights/{id}` — dismiss / action

### Opportunities (`/api/v1/opportunities`)
- ✅ `GET /` — list active (status=active)
- ✅ `POST /generate` — generate via Claude (now with category + creative signals)
- ✅ `PATCH /{id}` — used / dismissed / remind_later

### YouTube Briefs (`/api/v1/youtube-briefs`) — Week 7
- ✅ `GET /` — list all user's briefs (`?status=` filter)
- ✅ `GET /{id}` — single brief
- ✅ `PATCH /{id}` — update status / youtube_url (422 if publish without URL)
- ✅ `DELETE /{id}` — hard delete (204)
- ✅ `POST /{id}/stats` — log performance snapshot (upsert)
- ✅ `GET /{id}/stats` — list snapshots

### Challenges (`/api/v1/challenges`) — Week 7
- ✅ `POST /{opportunity_id}/complete` — save CreationEntry + update progress
- ✅ `GET /` — list user's creations (`?status=` filter)
- ✅ `POST /uploads` — multipart file upload

### Progress (`/api/v1/me/progress`) — Week 7
- ✅ `GET /me/progress` — return UserProgress

---

## Frontend Routes

| Route | Page | Status |
|-------|------|--------|
| `/` | → redirect to `/manager` | ✅ Week 7 |
| `/login` | LoginPage | ✅ |
| `/manager` | ManagerPage (CREATE/SHARE/TRACK) | ✅ Week 7 |
| `/dashboard` | DashboardPage | ✅ |
| `/songs` | SongsPage | ✅ |
| `/songs/new` | SongNewPage | ✅ |
| `/songs/:id` | SongDetailPage | ✅ |
| `/discover` | DiscoverPage | ✅ |
| `/campaigns` | CampaignsPage | ✅ |
| `/campaigns/:id` | CampaignDetailPage | ✅ |
| `/songs/:id/submithub` | SubmitHubPage | ✅ |

> **Note:** No registration page in UI. Use Swagger at `localhost:8000/docs` → `POST /api/v1/auth/register`. One-time setup.

---

## Environment & Dev Setup

### Running locally

**Backend** (from `backend/`):
```powershell
# One-time: create the SQLite database (all 19 tables + seed data)
..\.venv\Scripts\python -c "
from app.database import engine, Base
import app.models.user, app.models.song
import app.models.playlist, app.models.radio_station, app.models.pitch_submission
import app.models.generated_content, app.models.campaign, app.models.submithub
import app.models.dashboard, app.models.post_opportunity
import app.models.youtube_brief, app.models.creation_entry, app.models.user_progress
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
ANTHROPIC_API_KEY=<from Anthropic Console — required for content generation>
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Running tests
```powershell
# from backend/
..\.venv\Scripts\python -m pytest tests/ -v          # all 227 tests
..\.venv\Scripts\python -m pytest tests/ -k "us016"  # one user story
```

---

## Known Gotchas & Reminders

**Python 3.13 compatibility**
- `passlib[bcrypt]` crashes on Python 3.13 — we use `bcrypt` directly. Do not re-add passlib.
- `psycopg2-binary` requires `>=2.9.10` for Python 3.13 wheels.

**SQLite vs PostgreSQL**
- Tests use `sqlite:///:memory:` — no external DB needed.
- SQLite requires Python `date` objects, not strings. Always call `date.fromisoformat(raw[:10])`.
- `UniqueConstraint` on `(brief_id, snapshot_date)` works in SQLite for upsert patterns.

**SQLite transaction isolation in tests**
- Each test wraps in a DB transaction that rolls back after the test.
- Never call `db.rollback()` inside endpoint code — it rolls back the outer test transaction.
- Use `with db.begin_nested(): db.add(obj); db.flush()` to catch `IntegrityError` safely.

**Anthropic mock pattern (confirmed)**
```python
with patch("app.services.<module>.anthropic") as patched:
    patched.Anthropic.return_value = mock_client
    # run test
```
The module-level `anthropic` import is patched directly (not the class). `patched.Anthropic.return_value` sets what `anthropic.Anthropic()` returns inside the service.

**Category field on PostOpportunity**
- Default is `'promotion'` — existing signals that predate Week 7 are safe.
- Creative signals must always include `category: 'creative'` in the dict; YouTube signals: `category: 'youtube'`.

**UserProgress upsert**
- Created on first `POST /challenges/{id}/complete` call — no explicit creation needed.
- `update_progress()` in `progress_service.py` handles the upsert pattern.

**YouTube URL validation**
- Regex: `^https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+`
- 422 returned if `youtube_url` is missing or invalid when patching status to `published`.

**File uploads**
- Stored at `backend/uploads/{user_id}/{uuid}_{safe_filename}`
- Served via FastAPI `StaticFiles` mounted at `/uploads`
- Directory auto-created per user on first upload

**Always commit after writes**
- `db.flush()` alone does NOT persist — `db.commit()` required.
- Tests don't catch missing commits because the open test transaction keeps flushed data visible.

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
- **Claude model:** `claude-sonnet-4-20250514` across all AI services
- **Opportunity categories:** creative / youtube / promotion — drives UI styling + button labels
- **Level thresholds:** newcomer(0-4) / emerging(5-14) / pro(15-29) / expert(30+) — stored in `user_progress.level`
- **Streak calculation:** server-side in `progress_service.update_progress()` — date comparison against `last_challenge_date`
- **YouTube brief fallback:** `_fallback_brief()` returns structured placeholder with generic hook/chapters when Claude fails

---

## Observations & Lessons (Week 7)

**What worked well**
- TDD cycle clean throughout — writing tests first revealed the correct model relationships before building
- The `collect_signals()` redesign (accepting `songs` param directly) allowed catalog-aware creative signals without extra DB queries inside the service
- `progress_service.py` as a standalone module keeps the challenge endpoint thin and the logic unit-testable
- Category-aware `OpportunityCard` with a single `CATEGORY_STYLES` map kept the component clean despite 3 different visual modes

**Decisions made during implementation**
- `UserProgress` is created lazily (on first challenge complete) rather than at registration — simpler, no migration risk for existing users
- `search_keywords: []` normalized to `null` at the API layer — avoids empty-list edge cases in Claude prompts and frontend display
- `YouTubeBriefStat` uses `Date` (not `DateTime`) for `snapshot_date` — consistent with `DashboardSnapshot` pattern; SQLite-compatible
- `CelebrationScreen` fetches progress via `useQuery` (not passed as prop) — decouples the completion flow from knowing the pre-completion state; refetch on mount shows the updated values
- File upload UUID-prefixes the filename (`{uuid}_{safe_name}`) — prevents collisions without a separate file registry table

---

## Next Steps (Phase 2 Candidates)

**US-023: Creative Review System** (designed in PRD, not yet implemented)
- Option A: AI feedback on submitted text via Claude (post-challenge "Get Feedback" button)
- Option B: Self-reflection prompts (2 questions after celebration screen)
- Option C: Weekly Manager Report (Claude coaching summary)
- Recommendation: start with B (simplest), then A for text entries

**Infrastructure**
- Spotify for Artists API auto-sync (replace manual stat entry)
- AI audio analysis for song profiling
- Meta/Google Ads API for automated budget execution
- Israeli current events feed for richer opportunity signals
- Export features (CSV pitch history, PDF campaigns)
- Deploy to cloud (Railway / Render / Fly.io + managed PostgreSQL)
