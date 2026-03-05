# Music Manager — Israeli Music Promotion Tool

A personal full-stack web application built as a promotion command center for an independent Israeli artist releasing mainstream Hebrew pop. It centralizes song profiles, promotion targeting, campaign strategy, budget recommendations, pitch tracking, and AI-powered social content generation in one place.

---

## Why This Exists

Promoting a song in Israel — especially mainstream Hebrew pop — involves a fragmented landscape of Spotify playlists, radio stations, SubmitHub curators, and social channels. Without a system, every release means:

- Searching Google and Instagram for relevant playlists, getting inconsistent results
- Cold emailing curators with no record of who was contacted or what happened
- Dividing a limited budget arbitrarily across channels with no ROI awareness
- Writing social posts from scratch every time, missing timely hooks
- Staring at raw Spotify for Artists numbers with no idea what to actually do next

**Target:** reduce promotion admin from 4–8 hours per release to under 1.5 hours, while increasing coverage and making every decision data-informed rather than gut-driven.

The tool is a **strategic advisor, not an autopilot.** You approve every recommendation and act manually — the tool provides structure, curated data, and AI suggestions.

---

## Features

### 1. Song Catalog (Component 1)

The foundation of everything else. Each song has two layers of data:

**Spotify metadata** (auto-fetched on add):
- Title, artist, album, release date, duration, cover art, popularity
- Accepted as full URL, `spotify:track:` URI, or raw 22-character track ID

**Manual creative profile** (you fill in):
- **Story** — the narrative behind the song (used in AI content generation)
- **Genre** — free text, e.g. "mainstream Hebrew pop" (used for playlist matching)
- **Language** — Hebrew / English / Both (used for playlist matching)
- **Mood tags** — e.g. "melancholic", "upbeat", "romantic" (used for matching + content)
- **Themes** — e.g. "heartbreak", "nostalgia" (used for content generation)
- **Comparable artists** — e.g. "Omer Adam, Noa Kirel" (context for AI suggestions)

The more complete the profile, the better the match scores and the more targeted the AI output.

---

### 2. Israeli Playlist & Radio Discovery (Component 2)

Given a song, the tool scores every playlist in the database (0–100) and every radio station, then presents them ranked with reasons.

**How matching works:**
- Genre overlap (40 pts) — word-overlap between your genre and the playlist's genre tags
- Language match (35 pts) — exact match or "both" broadens eligibility
- Mood tag overlap (up to 25 pts) — shared mood tags between song and playlist

**Radio stations** get a simpler label: Recommended / Secondary / Low match, based on genre overlap count.

**Seeded database:**
- 25 Israeli Spotify playlists (from 558 to 76,800 followers), covering mainstream Hebrew pop, indie, acoustic, and cross-genre categories
- 6 Israeli radio stations: Galei Tzahal, Kan Gimel, Kan 88, 103FM, Eco 99FM, Radio Haifa

From the Discover page, you can select a song, see ranked targets, and click **Mark Pitched** to log a submission with method (email / Spotify / Instagram DM / SubmitHub).

---

### 3. SubmitHub Integration (Component 3)

Plan and track SubmitHub campaigns for a specific song.

- Create a SubmitHub campaign with an auto-generated code (format: `SH-YYYYMMDD-NNN`), budget allocation, and target curator count
- Log individual curator submissions with curator name, genre focus, approval rate, and cost
- Record outcomes: pending → approved / declined
- Track whether the curator added you to a playlist and save the playlist URL
- Optionally link to a main promotion campaign for unified budget visibility

---

### 4. Campaign & Budget Management (Component 4)

Organize a full promotion push (single, EP, or album) with budget tracking and AI recommendations.

**Campaign lifecycle:**
1. Create a campaign: name, release type, start/end dates, total budget, primary goal (Awareness / Grow Fanbase / Monetize), and attach songs
2. Click **Get AI Recommendation** to have Claude generate a channel budget split tailored to your release type, genre profile, and goal — with per-channel rationale
3. Log expenses as you spend: date, amount, category (playlist pitching / social ads / content / radio promotion / SubmitHub / other), subcategory, notes
4. The budget bar updates in real time as expenses accumulate; turns orange at 80%+ spent

**AI budget recommendation** produces a split across 6 channels: playlist pitching, SubmitHub, social ads, content creation, radio promotion, and other — each with a dollar amount, percentage, and rationale paragraph, plus a top-level strategic tip.

---

### 5. Dashboard & Insights Engine (Component 5)

A weekly health check for your catalog's performance.

**Sync Spotify data** (manual — copy from Spotify for Artists):
- Total streams (28-day), monthly listeners, followers, saves, playlist adds
- Week-over-week trends for streams, listeners, and followers

**Health Score (0–100)** is auto-calculated on each sync:

| Component | Weight | What it measures |
|-----------|--------|-----------------|
| Streams trend | 30% | Growing, stable, or declining? |
| Save rate | 25% | (Saves ÷ Streams) × 100 — above 5% target? |
| Follower conversion | 20% | (Followers ÷ Monthly Listeners) × 100 |
| Playlist adds | 15% | New adds in the past week |
| Campaign ROI | 10% | Cost per stream (from campaign expenses) |

Labels: **Excellent** (85–100) · **Healthy** (70–84) · **Needs Work** (50–69) · **Critical** (<50)

**AI Insights** — click Generate Insights to have Claude analyze your current snapshot and produce insight cards:
- 🎉 **Momentum Alert** — when a pitch was accepted
- ⚠️ **Performance Warning** — when streams are dropping
- 🔥 **Opportunity** — detected patterns worth acting on
- 💡 **Optimization Tip** — low save rate, low follower conversion, etc.

Each insight has a title, explanation, and a specific recommended action. Dismiss it or mark it as Done.

---

### 6. Hebrew Social Content Generation (Component 6)

Generate ready-to-post social media captions from your song's creative profile.

**Inputs:**
- Post type: single release / EP release / milestone / playlist add / general
- Platforms: Instagram / Facebook / TikTok (can select multiple)
- Tones: emotional / playful / mysterious / proud (can select multiple)
- Key message and optional context for this post

**Output:** One generation = one Hebrew caption + one English caption per tone × platform combination, trimmed to platform limits (Instagram 150 chars, Facebook 80, TikTok 100), with Hebrew + English hashtags.

Each result has a **Copy** button. All generations are stored per song so you can refer back to previous sessions.

The generation uses Claude (`claude-sonnet-4-20250514`) and factors in the song's story, mood tags, themes, comparable artists, and genre.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, FastAPI, SQLAlchemy 2.0 |
| Database | SQLite (dev) / PostgreSQL (prod-ready) |
| Auth | JWT (HS256), bcrypt, 7-day token expiry |
| AI | Anthropic Python SDK, Claude Sonnet 4 |
| Migrations | Alembic |
| Frontend | React 18, TypeScript, Vite |
| Styling | TailwindCSS 3 |
| Data fetching | TanStack Query v5 |
| HTTP client | Axios |

---

## Project Structure

```
music_manager/
├── backend/
│   ├── main.py                  # FastAPI app, all routers, lifespan (seed on boot)
│   ├── .env                     # Not committed — see .env.example
│   ├── requirements.txt
│   ├── alembic/                 # DB migrations
│   │   └── versions/            # 0001, 0002, 0003 — sequential schema history
│   ├── app/
│   │   ├── api/                 # Route handlers (one file per domain)
│   │   │   ├── auth.py          # /register, /login, /me
│   │   │   ├── songs.py         # CRUD + Spotify fetch + match + content
│   │   │   ├── playlists.py     # GET /playlists (filtered)
│   │   │   ├── radio_stations.py
│   │   │   ├── pitches.py       # Pitch log + status updates
│   │   │   ├── content.py       # Hebrew content generation
│   │   │   ├── campaigns.py     # Campaign CRUD + budget recommendation + expenses
│   │   │   ├── submithub.py     # SubmitHub campaigns + submissions
│   │   │   └── dashboard.py     # Snapshot sync + health score + insights
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── services/
│   │   │   ├── spotify.py       # Spotify API client + URL parser
│   │   │   ├── seed.py          # 25 playlists + 6 radio stations (idempotent)
│   │   │   ├── playlist_matcher.py  # score_playlist() + score_radio_station()
│   │   │   ├── health_score.py  # calculate_health_score() + health_label()
│   │   │   ├── budget_recommender.py  # Claude budget allocation
│   │   │   ├── insight_generator.py   # Claude insight cards
│   │   │   └── content_generator.py   # Claude Hebrew captions
│   │   └── utils/
│   │       ├── auth.py          # JWT + bcrypt helpers
│   │       └── logging_config.py
│   └── tests/
│       ├── conftest.py          # SQLite in-memory fixtures (no external DB needed)
│       ├── integration/         # test_us001 through test_us013
│       └── unit/                # test_us002_spotify_url_parsing
└── frontend/
    └── src/
        ├── App.tsx              # Routes
        ├── types/index.ts       # All TypeScript interfaces
        ├── api/                 # One file per backend domain
        ├── components/
        │   ├── Nav.tsx
        │   ├── ProtectedRoute.tsx
        │   ├── songs/           # SongCard
        │   ├── discover/        # PlaylistCard, RadioStationCard
        │   └── content/         # ContentPanel
        └── pages/
            ├── DashboardPage.tsx
            ├── SongsPage.tsx
            ├── SongNewPage.tsx
            ├── SongDetailPage.tsx
            ├── DiscoverPage.tsx
            ├── CampaignsPage.tsx
            ├── CampaignDetailPage.tsx
            └── LoginPage.tsx
```

---

## Local Setup

### Prerequisites

- Python 3.11+ (tested on 3.13.5)
- Node.js 18+
- A Spotify Developer account (free)
- An Anthropic API key (for AI features)

### 1. Clone and install

```bash
git clone <repo-url>
cd music_manager
```

```powershell
# Windows — create and activate virtual environment (from repo root)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

```bash
# Install frontend dependencies (Git Bash or any terminal)
cd frontend
npm install
```

### 2. Configure environment

Create `backend/.env` (copy from `.env.example`):

```env
DATABASE_URL=sqlite:///./music_manager.db
SECRET_KEY=<any long random string — generate with: python -c "import secrets; print(secrets.token_hex(32))">
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

SPOTIFY_CLIENT_ID=<from Spotify Developer Dashboard>
SPOTIFY_CLIENT_SECRET=<from Spotify Developer Dashboard>

ANTHROPIC_API_KEY=<from console.anthropic.com>

ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Getting Spotify credentials:** Go to [developer.spotify.com](https://developer.spotify.com/dashboard), create an app, copy the Client ID and Client Secret. No redirect URIs needed — this uses the Client Credentials flow (server-to-server only).

**Getting Anthropic API key:** Go to [console.anthropic.com](https://console.anthropic.com), create an API key. Required for: budget recommendations, insight generation, and Hebrew content generation.

### 3. Initialize the database

This creates all tables and loads the Israeli playlist/radio seed data (one-time):

```powershell
# From backend/
..\.venv\Scripts\python -c "
from app.database import engine, Base
import app.models.user, app.models.song
import app.models.playlist, app.models.radio_station, app.models.pitch_submission
import app.models.generated_content, app.models.campaign, app.models.submithub
import app.models.dashboard
Base.metadata.create_all(engine)
from app.database import SessionLocal
from app.services.seed import seed_playlists, seed_radio_stations
db = SessionLocal()
seed_playlists(db); seed_radio_stations(db); db.commit(); db.close()
print('Database ready.')
"
```

### 4. Register your user account

There is no registration page in the UI — this is a single-user tool. Register once via Swagger:

1. Start the backend: `..\.venv\Scripts\uvicorn main:app --reload` (from `backend/`)
2. Open [http://localhost:8000/docs](http://localhost:8000/docs)
3. Find `POST /api/v1/auth/register` → Try it out → fill in name, email, password → Execute
4. Registration is locked after the first user is created

### 5. Run the app

Open **two terminals**:

```powershell
# Terminal 1 — Backend (from backend/)
..\.venv\Scripts\uvicorn main:app --reload
# API: http://localhost:8000
# Swagger docs: http://localhost:8000/docs
```

```bash
# Terminal 2 — Frontend (from frontend/, Git Bash)
npm run dev
# App: http://localhost:5173
```

Open [http://localhost:5173](http://localhost:5173), log in with the account you registered, and you're in.

---

## Using the Tool — Typical Workflow

### Adding a new release

1. Go to **Songs** → **Add Song**
2. Paste the Spotify URL, URI, or track ID → metadata is auto-fetched
3. Open the song detail page and fill in the creative profile:
   - Write a short **story** (1–3 sentences about the song's meaning)
   - Set **genre** (e.g. "mainstream Hebrew pop")
   - Set **language** (Hebrew / English / Both)
   - Add **mood tags** (comma-separated: e.g. melancholic, hopeful)
   - Add **themes** and **comparable artists**
4. Save — the song is now ready for matching and content generation

### Finding promotion targets

1. Go to **Discover**
2. Select your song from the dropdown
3. The page shows all 25 Israeli playlists ranked by match score (0–100%), with reasons
4. Below that: all 6 radio stations with Recommended / Secondary labels
5. Click **Mark Pitched** on any target to log the submission

### Tracking pitches

- All logged pitches appear in the **Pitch History** table on each song's detail page
- Update status as responses come in: sent → responded → added / rejected / no_response
- When a pitch is marked **added**, it surfaces as a Momentum Alert on the Dashboard

### Planning a campaign

1. Go to **Campaigns** → **+ New Campaign**
2. Fill in name, release type, goal, dates, budget, and attach songs
3. Open the campaign → click **Get AI Recommendation** for a budget split
4. As you spend money, click **+ Add Expense** to log it
5. The budget bar shows how much you've used; the AI recommendation shows planned vs. actual

### Syncing analytics

1. Go to **Dashboard** → **Sync Spotify Data**
2. Open Spotify for Artists, copy your numbers for the past 28 days
3. Fill in: total streams, monthly listeners, followers, saves, playlist adds
4. Optionally enter week-over-week trend percentages
5. Click **Save Data** — your Health Score updates immediately
6. Click **Generate Insights** to get AI-powered action cards

### Generating social content

1. Open any song's detail page → scroll to **Social Content**
2. Select post type, platforms, and tones
3. Add a key message and optional context (e.g. "just hit 5K streams")
4. Click **Generate** — captions appear in Hebrew (RTL) and English with hashtags
5. Copy the ones you want to use

---

## Running Tests

All tests use an in-memory SQLite database — no external services required (Spotify and Anthropic calls are mocked).

```powershell
# From backend/
..\.venv\Scripts\python -m pytest tests/ -v         # all 142 tests
..\.venv\Scripts\python -m pytest tests/ -k "us008" # one user story
..\.venv\Scripts\python -m pytest tests/unit/       # unit tests only
```

All 142 tests must pass before committing. A failing test blocks the commit.

---

## Notes

- **Single-user tool** — registration is locked after the first account is created. There is no multi-user support.
- **AI features require `ANTHROPIC_API_KEY`** — budget recommendations, insight generation, and Hebrew content generation all call Claude. If the key is missing or the call fails, graceful fallbacks are used (rule-based budget split, rule-based insights).
- **Spotify credentials are optional for manual entry** — if no Spotify credentials are configured, the song creation endpoint will fail. You can still use the rest of the tool if songs were added previously.
- **SQLite is used in development** — switching to PostgreSQL for production requires changing only `DATABASE_URL` in `.env`. The ORM and migrations are fully compatible.
- **Hebrew text is RTL** — captions generated in Hebrew are displayed with `dir="rtl"` in the content panel.
- **Logs** are written to `backend/logs/` (rotating file) and also to the console.
