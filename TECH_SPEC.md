# Technical Specifications
## Israeli Music Promotion Tool — Personal Edition

**Version:** 1.0
**Date:** February 24, 2026
**Status:** Draft — Awaiting Review
**Based on:** PRD v1.1
**Stack:** Python 3.11 / FastAPI · React 18 / TypeScript · PostgreSQL 15

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Database Schema](#2-database-schema)
3. [API Endpoints](#3-api-endpoints)
4. [Business Logic](#4-business-logic)
5. [External Service Integrations](#5-external-service-integrations)
6. [Security Specifications](#6-security-specifications)
7. [Performance Requirements](#7-performance-requirements)
8. [Infrastructure & Development Setup](#8-infrastructure--development-setup)
9. [Testing Strategy](#9-testing-strategy)
10. [Monitoring & Observability](#10-monitoring--observability)
11. [Feasibility Review](#11-feasibility-review)
12. [Open Technical Questions](#12-open-technical-questions)

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────┐
│              User Browser                    │
│   React 18 SPA (TypeScript + TailwindCSS)    │
└────────────────────┬────────────────────────┘
                     │ HTTPS / JSON
                     ▼
┌─────────────────────────────────────────────┐
│           FastAPI Backend                    │
│   /api/v1/*  ·  JWT Auth  ·  Rate Limiting  │
│                                             │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐ │
│  │ Songs &  │ │Campaign &│ │  Dashboard  │ │
│  │Playlists │ │ Budget   │ │ & Insights  │ │
│  └──────────┘ └──────────┘ └─────────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐ │
│  │ Pitches  │ │SubmitHub │ │Opportunity  │ │
│  │ Tracker  │ │ Planner  │ │   Engine    │ │
│  └──────────┘ └──────────┘ └─────────────┘ │
└──────┬──────────────┬───────────────────────┘
       │              │
       ▼              ▼
┌──────────────┐  ┌───────────────────────────┐
│  PostgreSQL  │  │     External Services      │
│  Database    │  │  ┌──────────┐ ┌─────────┐  │
│              │  │  │ Spotify  │ │Anthropic│  │
│              │  │  │  Web API │ │   API   │  │
└──────────────┘  │  └──────────┘ └─────────┘  │
                  └───────────────────────────┘
```

### 1.2 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Backend language | Python | 3.11+ | Core runtime |
| Backend framework | FastAPI | 0.115+ | API server, routing, validation |
| ORM | SQLAlchemy | 2.0+ | Database access (async) |
| Migrations | Alembic | 1.13+ | Schema versioning |
| Async HTTP client | httpx | 0.27+ | External API calls |
| Auth | python-jose + passlib | latest | JWT + password hashing |
| Task runner | — | — | No background workers in MVP; Claude calls are synchronous |
| Frontend language | TypeScript | 5.0+ | Type safety |
| Frontend framework | React | 18+ | UI |
| Build tool | Vite | 5.0+ | Dev server + bundling |
| Styling | TailwindCSS | 3.4+ | Utility-first CSS |
| Data fetching | TanStack Query | 5.0+ | Server state, caching, refetch |
| Routing | React Router | 6+ | Client-side routing |
| Forms | React Hook Form + Zod | latest | Form state + validation |
| HTTP client (frontend) | axios | 1.7+ | API calls with interceptors |
| Database | PostgreSQL | 15+ | Primary data store |
| AI | Anthropic Python SDK | 0.34+ | Claude Sonnet 4 |
| Music metadata | Spotipy | 2.24+ | Spotify Web API wrapper |

### 1.3 Backend Module Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI app init, middleware, routers
│   ├── config.py                # Settings (pydantic-settings, env vars)
│   ├── database.py              # SQLAlchemy engine + session
│   │
│   ├── api/                     # Route handlers (thin — delegate to services)
│   │   ├── auth.py
│   │   ├── songs.py
│   │   ├── playlists.py
│   │   ├── radio_stations.py
│   │   ├── pitches.py
│   │   ├── campaigns.py
│   │   ├── expenses.py
│   │   ├── submithub.py
│   │   ├── dashboard.py
│   │   ├── opportunities.py
│   │   └── spotify.py
│   │
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── song.py
│   │   ├── playlist.py
│   │   ├── radio_station.py
│   │   ├── pitch.py
│   │   ├── campaign.py
│   │   ├── expense.py
│   │   ├── performance.py
│   │   ├── submithub.py
│   │   ├── dashboard.py
│   │   ├── opportunity.py
│   │   └── insight.py
│   │
│   ├── schemas/                 # Pydantic request/response models
│   │   ├── song.py
│   │   ├── campaign.py
│   │   ├── opportunity.py
│   │   └── ...
│   │
│   ├── services/                # Business logic
│   │   ├── spotify_service.py       # Spotify API wrapper
│   │   ├── health_score_service.py  # Health score calculation
│   │   ├── budget_recommendation_service.py  # AI budget splits
│   │   ├── opportunity_service.py   # Post opportunity generation
│   │   ├── insight_service.py       # Dashboard insight cards
│   │   ├── playlist_match_service.py # Song-to-playlist matching
│   │   └── submithub_service.py     # SubmitHub brief generation
│   │
│   └── utils/
│       ├── auth.py              # JWT helpers
│       ├── logging.py           # Logger setup
│       └── pagination.py        # Cursor-based pagination helpers
│
├── alembic/                     # Migration scripts
├── tests/
└── requirements.txt
```

### 1.4 Frontend Module Structure

```
frontend/
├── src/
│   ├── main.tsx                 # App entry point
│   ├── App.tsx                  # Router setup
│   │
│   ├── pages/
│   │   ├── DashboardPage.tsx
│   │   ├── SongsPage.tsx
│   │   ├── SongDetailPage.tsx
│   │   ├── SongNewPage.tsx
│   │   ├── DiscoverPage.tsx
│   │   ├── CampaignsPage.tsx
│   │   ├── CampaignDetailPage.tsx
│   │   ├── OpportunitiesPage.tsx
│   │   └── LoginPage.tsx
│   │
│   ├── components/
│   │   ├── common/              # Reusable: Button, Card, Badge, Modal...
│   │   ├── songs/               # SongCard, SongProfileForm, SpotifyFetch
│   │   ├── campaigns/           # CampaignCard, BudgetRecommendation, ExpenseForm
│   │   ├── dashboard/           # HealthScore, InsightCard, MetricsGrid
│   │   ├── discover/            # PlaylistCard, RadioCard, PitchTracker
│   │   └── opportunities/       # OpportunityCard, OpportunityFeed
│   │
│   ├── hooks/
│   │   ├── useSongs.ts
│   │   ├── useCampaigns.ts
│   │   ├── useDashboard.ts
│   │   └── useOpportunities.ts
│   │
│   ├── api/                     # axios API functions (one file per domain)
│   │   ├── client.ts            # axios instance with JWT interceptor
│   │   ├── songs.ts
│   │   ├── campaigns.ts
│   │   ├── dashboard.ts
│   │   └── opportunities.ts
│   │
│   ├── types/                   # TypeScript interfaces mirroring API schemas
│   └── utils/
│       ├── hebrew.ts            # RTL helpers, Hebrew formatting
│       └── currency.ts          # USD/ILS formatting
│
├── index.html
├── vite.config.ts
├── tailwind.config.ts
└── package.json
```

---

## 2. Database Schema

### 2.1 Design Principles

- All primary keys are UUIDs (`gen_random_uuid()`)
- All tables have `created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()`
- Soft deletes not used — hard delete with `ON DELETE CASCADE` where appropriate
- Array columns (`TEXT[]`) used for tags, genres, mood_tags — acceptable for personal-scale tool
- `JSONB` used for raw API responses and flexible metadata
- All monetary values in `DECIMAL(10,2)` (USD)

### 2.2 Complete Schema

```sql
-- ============================================================
-- EXTENSION
-- ============================================================
CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- for gen_random_uuid()


-- ============================================================
-- USERS
-- Single user in practice, but auth is enforced for security
-- ============================================================
CREATE TABLE users (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email                   VARCHAR(255) UNIQUE NOT NULL,
    password_hash           VARCHAR(255) NOT NULL,
    full_name               VARCHAR(255),

    -- Spotify OAuth tokens
    spotify_user_id         VARCHAR(255),
    spotify_access_token    TEXT,
    spotify_refresh_token   TEXT,
    spotify_token_expires_at TIMESTAMP WITH TIME ZONE,

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login_at           TIMESTAMP WITH TIME ZONE
);


-- ============================================================
-- SONGS
-- Full song profile: Spotify metadata + creative profile
-- AI fields are nullable — populated in Phase 2
-- ============================================================
CREATE TABLE songs (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Basic identity
    title                   VARCHAR(255) NOT NULL,
    title_hebrew            VARCHAR(255),
    title_english           VARCHAR(255),
    artist_name             VARCHAR(255),
    release_date            DATE,
    duration_ms             INTEGER,

    -- Spotify link
    spotify_uri             VARCHAR(255) UNIQUE,         -- spotify:track:xxx
    spotify_track_id        VARCHAR(255) UNIQUE,         -- ID portion only
    isrc                    VARCHAR(50),
    album_name              VARCHAR(255),
    album_artwork_url       TEXT,

    -- Spotify audio features (from API — read-only)
    tempo                   DECIMAL(6,2),
    musical_key             INTEGER,                     -- 0–11 (C, C#, D…)
    musical_mode            SMALLINT,                    -- 0=minor, 1=major
    time_signature          SMALLINT,
    energy                  DECIMAL(4,3),                -- 0.0–1.0
    valence                 DECIMAL(4,3),                -- 0.0–1.0 (sad→happy)
    acousticness            DECIMAL(4,3),
    danceability            DECIMAL(4,3),
    instrumentalness        DECIMAL(4,3),
    liveness                DECIMAL(4,3),
    loudness                DECIMAL(6,2),                -- dB
    speechiness             DECIMAL(4,3),

    -- User-entered creative profile
    primary_genre           VARCHAR(100),
    secondary_genres        TEXT[],
    language_primary        VARCHAR(50) DEFAULT 'hebrew', -- 'hebrew', 'english', 'mixed'
    language_secondary      VARCHAR(50),

    mood_tags               TEXT[],                      -- ['melancholic', 'uplifting', ...]
    lyrical_themes          TEXT[],                      -- ['heartbreak', 'nostalgia', ...]
    vocal_style             TEXT[],
    production_style        TEXT[],

    story_behind_song       TEXT,                        -- 200+ words; required for full profile
    comparable_artists      TEXT,                        -- comma-separated

    golden_minute_start     INTEGER,                     -- seconds
    golden_minute_end       INTEGER,
    golden_minute_note      TEXT,

    -- Israeli-specific metadata
    featured_artists        TEXT[],
    recording_location      VARCHAR(255),
    producer                VARCHAR(255),
    radio_ready_galei_tzahal BOOLEAN DEFAULT FALSE,
    radio_ready_kan_gimel   BOOLEAN DEFAULT FALSE,
    radio_ready_kan_88      BOOLEAN DEFAULT FALSE,
    festival_tags           TEXT[],

    personal_notes          TEXT,
    is_draft                BOOLEAN DEFAULT FALSE,

    -- Phase 2 AI analysis fields (NULL in MVP)
    ai_analysis_provider    VARCHAR(50),
    ai_analysis_timestamp   TIMESTAMP WITH TIME ZONE,
    ai_analysis_raw_json    JSONB,
    ai_genre_primary        VARCHAR(100),
    ai_mood_tags            TEXT[],
    ai_lyrical_themes       TEXT[],
    ai_story_draft          TEXT,
    ai_golden_minute_start  INTEGER,
    ai_golden_minute_end    INTEGER,

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_songs_user_id ON songs(user_id);
CREATE INDEX idx_songs_release_date ON songs(release_date DESC);
CREATE INDEX idx_songs_spotify_track_id ON songs(spotify_track_id);


-- ============================================================
-- PLAYLISTS
-- Curated database of Israeli Spotify playlists
-- Seeded via migration; admin-updated manually
-- ============================================================
CREATE TABLE playlists (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name                    VARCHAR(255) NOT NULL,
    spotify_playlist_id     VARCHAR(255) UNIQUE,
    spotify_url             TEXT,

    curator_name            VARCHAR(255),
    curator_contact         VARCHAR(255),               -- email or IG handle
    curator_contact_method  VARCHAR(50),                -- 'email', 'instagram_dm', 'spotify_for_artists'

    follower_count          INTEGER,
    follower_count_updated  DATE,                       -- when follower count was last verified

    -- Matching criteria
    genres                  TEXT[] NOT NULL,
    languages               TEXT[] NOT NULL,            -- ['hebrew', 'english', 'both']
    mood_tags               TEXT[],

    submission_method       VARCHAR(50),                -- 'spotify_for_artists', 'email', 'instagram_dm', 'submithub'
    submission_guidelines   TEXT,

    is_active               BOOLEAN DEFAULT TRUE,
    is_editorial            BOOLEAN DEFAULT FALSE,      -- Spotify-curated editorial (no direct pitch)
    notes                   TEXT,

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_playlists_genres ON playlists USING GIN(genres);
CREATE INDEX idx_playlists_languages ON playlists USING GIN(languages);
CREATE INDEX idx_playlists_follower_count ON playlists(follower_count DESC);


-- ============================================================
-- RADIO STATIONS
-- Israeli radio contacts and submission info
-- Seeded via migration
-- ============================================================
CREATE TABLE radio_stations (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name                    VARCHAR(255) NOT NULL,
    name_hebrew             VARCHAR(255),
    station_type            VARCHAR(50),                -- 'national', 'regional', 'online', 'university'

    contact_email           VARCHAR(255),
    contact_phone           VARCHAR(50),
    website                 VARCHAR(500),

    genres_focus            TEXT[] NOT NULL,
    best_for                TEXT[],                     -- ['indie', 'mainstream pop', 'alternative']

    submission_guidelines   TEXT NOT NULL,
    submission_method       VARCHAR(50),                -- 'email', 'web_form', 'instagram_dm'
    response_time_estimate  VARCHAR(100),               -- '1-2 weeks'

    reach_description       VARCHAR(255),
    priority_rank           SMALLINT DEFAULT 5,         -- 1=highest for this genre

    notes                   TEXT,
    is_active               BOOLEAN DEFAULT TRUE,

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- ============================================================
-- PITCH SUBMISSIONS
-- Log of every pitch made: playlist, radio, or other
-- ============================================================
CREATE TABLE pitch_submissions (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    song_id                 UUID NOT NULL REFERENCES songs(id) ON DELETE CASCADE,
    campaign_id             UUID REFERENCES campaigns(id) ON DELETE SET NULL,

    target_type             VARCHAR(20) NOT NULL,       -- 'playlist', 'radio', 'blog', 'other'
    target_playlist_id      UUID REFERENCES playlists(id) ON DELETE SET NULL,
    target_radio_id         UUID REFERENCES radio_stations(id) ON DELETE SET NULL,
    target_name             VARCHAR(255),               -- fallback if not in DB

    pitched_at              TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    pitch_method            VARCHAR(50),                -- 'email', 'spotify_for_artists', 'instagram_dm'
    pitch_notes             TEXT,                       -- what you wrote/sent

    status                  VARCHAR(50) DEFAULT 'sent', -- 'sent', 'responded', 'added', 'rejected', 'no_response'
    responded_at            TIMESTAMP WITH TIME ZONE,
    response_notes          TEXT,                       -- curator feedback (copy-paste)

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_pitches_song_id ON pitch_submissions(song_id);
CREATE INDEX idx_pitches_campaign_id ON pitch_submissions(campaign_id);
CREATE INDEX idx_pitches_status ON pitch_submissions(status);


-- ============================================================
-- CAMPAIGNS
-- Promotion campaigns: single / EP / album
-- ============================================================
CREATE TABLE campaigns (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    name                    VARCHAR(255) NOT NULL,
    release_type            VARCHAR(20) NOT NULL DEFAULT 'single', -- 'single', 'ep', 'album'

    start_date              DATE NOT NULL,
    end_date                DATE NOT NULL,

    budget_total            DECIMAL(10,2) NOT NULL,

    -- Phase breakdown (auto-calculated from dates or manually set)
    pre_release_start       DATE,
    launch_week_start       DATE,
    post_release_start      DATE,

    primary_goal            VARCHAR(50),                -- 'awareness', 'growth', 'monetization'
    status                  VARCHAR(50) DEFAULT 'planning', -- 'planning', 'active', 'completed'
    notes                   TEXT,

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_campaigns_user_id ON campaigns(user_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);


-- ============================================================
-- CAMPAIGN SONGS
-- Many-to-many: campaigns <-> songs
-- ============================================================
CREATE TABLE campaign_songs (
    campaign_id             UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    song_id                 UUID NOT NULL REFERENCES songs(id) ON DELETE CASCADE,
    song_order              SMALLINT DEFAULT 0,         -- for EP/album track ordering
    PRIMARY KEY (campaign_id, song_id)
);


-- ============================================================
-- BUDGET RECOMMENDATIONS
-- AI-generated budget split per campaign
-- Stored separately from actual spend for comparison
-- ============================================================
CREATE TABLE budget_recommendations (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id             UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,

    -- Generated allocation (what AI recommended)
    playlist_pitching_pct   DECIMAL(5,2),               -- percentage
    playlist_pitching_amt   DECIMAL(10,2),              -- dollar amount
    submithub_pct           DECIMAL(5,2),
    submithub_amt           DECIMAL(10,2),
    social_ads_pct          DECIMAL(5,2),
    social_ads_amt          DECIMAL(10,2),
    content_creation_pct    DECIMAL(5,2),
    content_creation_amt    DECIMAL(10,2),
    pr_blogs_pct            DECIMAL(5,2),
    pr_blogs_amt            DECIMAL(10,2),
    other_pct               DECIMAL(5,2),
    other_amt               DECIMAL(10,2),

    -- Rationale from Claude (JSON: { "playlist_pitching": "reason...", ... })
    rationale_json          JSONB,

    -- User edits (what was actually approved)
    artist_approved_json    JSONB,                      -- same shape as above, post-adjustment
    approved_at             TIMESTAMP WITH TIME ZONE,

    -- Context used for generation (for debugging / learning)
    generation_context_json JSONB,                      -- listener tier, release type, past ROI used

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- ============================================================
-- EXPENSES
-- Manual expense tracking per campaign
-- ============================================================
CREATE TABLE expenses (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id             UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    song_id                 UUID REFERENCES songs(id) ON DELETE SET NULL,

    expense_date            DATE NOT NULL,
    amount                  DECIMAL(10,2) NOT NULL,

    category                VARCHAR(100) NOT NULL,      -- 'playlist_pitching', 'submithub', 'social_ads', 'content', 'pr_blogs', 'other'
    subcategory             VARCHAR(100),               -- 'instagram_ads', 'facebook_ads', 'photo_shoot', ...
    description             TEXT,

    source                  VARCHAR(50) DEFAULT 'manual', -- 'manual' (Phase 2: 'api_meta', 'api_google')
    external_id             VARCHAR(255),

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_expenses_campaign_id ON expenses(campaign_id);
CREATE INDEX idx_expenses_category ON expenses(category);


-- ============================================================
-- CAMPAIGN PERFORMANCE
-- Daily metric snapshots (manually synced from Spotify for Artists)
-- ============================================================
CREATE TABLE campaign_performance (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id             UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    song_id                 UUID NOT NULL REFERENCES songs(id) ON DELETE CASCADE,

    metric_date             DATE NOT NULL,

    -- Streaming metrics
    streams_total           INTEGER DEFAULT 0,
    streams_today           INTEGER DEFAULT 0,

    -- Engagement
    saves_total             INTEGER DEFAULT 0,
    saves_today             INTEGER DEFAULT 0,
    playlist_adds_total     INTEGER DEFAULT 0,

    -- Audience
    monthly_listeners       INTEGER DEFAULT 0,
    followers_total         INTEGER DEFAULT 0,

    -- Optional social
    instagram_followers     INTEGER,
    instagram_reach         INTEGER,

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    UNIQUE (campaign_id, song_id, metric_date)
);

CREATE INDEX idx_performance_campaign_song ON campaign_performance(campaign_id, song_id);
CREATE INDEX idx_performance_date ON campaign_performance(metric_date DESC);


-- ============================================================
-- SUBMITHUB CAMPAIGNS
-- Tracks a SubmitHub batch per song
-- ============================================================
CREATE TABLE submithub_campaigns (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id             UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    song_id                 UUID NOT NULL REFERENCES songs(id) ON DELETE CASCADE,

    campaign_code           VARCHAR(50) UNIQUE,         -- e.g. CAMP-20260224-001
    created_date            DATE NOT NULL DEFAULT CURRENT_DATE,

    budget_allocated        DECIMAL(10,2),
    budget_spent            DECIMAL(10,2) DEFAULT 0,
    curator_count           SMALLINT DEFAULT 0,

    status                  VARCHAR(50) DEFAULT 'active', -- 'active', 'completed'
    notes                   TEXT,

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- ============================================================
-- SUBMITHUB SUBMISSIONS
-- Per-curator result tracking
-- ============================================================
CREATE TABLE submithub_submissions (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submithub_campaign_id   UUID NOT NULL REFERENCES submithub_campaigns(id) ON DELETE CASCADE,

    curator_name            VARCHAR(255) NOT NULL,
    curator_genre_focus     TEXT[],
    curator_approval_rate   DECIMAL(5,2),               -- e.g. 20.5 = 20.5%

    submission_date         DATE,
    cost                    DECIMAL(5,2),               -- $1 or $3

    response_status         VARCHAR(50) DEFAULT 'pending', -- 'pending', 'approved', 'declined'
    response_date           DATE,
    curator_feedback        TEXT,

    playlist_added          BOOLEAN DEFAULT FALSE,
    playlist_url            TEXT,

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- ============================================================
-- DASHBOARD SNAPSHOTS
-- Daily aggregated metrics for the dashboard
-- ============================================================
CREATE TABLE dashboard_snapshots (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    snapshot_date           DATE NOT NULL,

    -- Aggregate streaming metrics
    total_streams_28d       INTEGER DEFAULT 0,
    total_monthly_listeners INTEGER DEFAULT 0,
    total_followers         INTEGER DEFAULT 0,
    total_saves_28d         INTEGER DEFAULT 0,
    total_playlist_adds_28d INTEGER DEFAULT 0,

    -- Calculated metrics
    save_rate               DECIMAL(5,2),               -- (saves/streams)*100
    follower_conversion_rate DECIMAL(5,2),              -- (followers/listeners)*100

    -- Health score
    health_score            SMALLINT,                   -- 0–100

    -- Week-over-week deltas (%)
    streams_delta_pct       DECIMAL(6,2),
    listeners_delta_pct     DECIMAL(6,2),
    followers_delta_pct     DECIMAL(6,2),

    -- Raw input (what user typed in from Spotify for Artists)
    raw_input_json          JSONB,

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    UNIQUE (user_id, snapshot_date)
);

CREATE INDEX idx_snapshots_user_date ON dashboard_snapshots(user_id, snapshot_date DESC);


-- ============================================================
-- INSIGHTS
-- AI-generated actionable insight cards shown on dashboard
-- ============================================================
CREATE TABLE insights (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    insight_type            VARCHAR(50) NOT NULL,       -- 'momentum', 'warning', 'opportunity', 'tip', 'milestone'
    priority                VARCHAR(20) DEFAULT 'medium', -- 'high', 'medium', 'low'

    title                   VARCHAR(255) NOT NULL,
    description             TEXT NOT NULL,
    action_text             VARCHAR(255),
    action_link             VARCHAR(500),               -- internal route (e.g. /discover?song=xxx)

    related_song_id         UUID REFERENCES songs(id) ON DELETE SET NULL,
    related_campaign_id     UUID REFERENCES campaigns(id) ON DELETE SET NULL,

    status                  VARCHAR(50) DEFAULT 'active', -- 'active', 'dismissed', 'actioned'
    expires_at              TIMESTAMP WITH TIME ZONE,

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_insights_user_status ON insights(user_id, status);


-- ============================================================
-- POST OPPORTUNITIES
-- AI-generated post angle suggestions (not written posts)
-- ============================================================
CREATE TABLE post_opportunities (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    song_id                 UUID REFERENCES songs(id) ON DELETE SET NULL,
    campaign_id             UUID REFERENCES campaigns(id) ON DELETE SET NULL,

    -- The suggestion
    hook                    TEXT NOT NULL,              -- 1-2 sentence angle/idea
    why_now                 TEXT NOT NULL,              -- explanation of the signal
    signal_type             VARCHAR(50) NOT NULL,       -- 'milestone', 'playlist_add', 'inactivity', 'calendar', 'trend', 'campaign_event'

    suggested_platform      VARCHAR(50),                -- 'instagram', 'facebook', 'tiktok', 'all'
    hashtag_suggestions     TEXT[],                     -- mix of Hebrew + English
    timing_note             TEXT,                       -- e.g. "Post before Friday evening"

    -- Status
    status                  VARCHAR(50) DEFAULT 'active', -- 'active', 'used', 'dismissed', 'remind_later'
    remind_at               TIMESTAMP WITH TIME ZONE,   -- set when 'remind_later'
    used_at                 TIMESTAMP WITH TIME ZONE,

    expires_at              TIMESTAMP WITH TIME ZONE,   -- time-sensitive opportunities auto-expire

    created_at              TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_opportunities_user_status ON post_opportunities(user_id, status);
```

### 2.3 Key Relationships Diagram

```
users (1)
  ├──< songs (many)
  │     └──< campaign_songs >──< campaigns
  │
  ├──< campaigns (many)
  │     ├──< budget_recommendations
  │     ├──< expenses
  │     ├──< campaign_performance
  │     ├──< pitch_submissions
  │     └──< submithub_campaigns
  │           └──< submithub_submissions
  │
  ├──< dashboard_snapshots
  ├──< insights
  └──< post_opportunities

playlists (global, no user_id — shared database)
radio_stations (global, no user_id — shared database)

pitch_submissions ──> playlists (nullable FK)
pitch_submissions ──> radio_stations (nullable FK)
```

### 2.4 Alembic Migration Strategy

```
alembic/versions/
  0001_initial_schema.py          # All tables above
  0002_seed_playlists.py          # 50+ Israeli playlists
  0003_seed_radio_stations.py     # 10+ Israeli radio stations
```

- Never modify existing migrations — always add new ones
- Each migration has both `upgrade()` and `downgrade()`
- Run before every deployment: `alembic upgrade head`

---

## 3. API Endpoints

### 3.1 Conventions

- Base path: `/api/v1/`
- Authentication: `Authorization: Bearer <jwt>` header on all protected endpoints
- Error format (RFC 7807):
```json
{
  "detail": "Human-readable message",
  "error_code": "SONG_NOT_FOUND",
  "status": 404
}
```
- Pagination: `?limit=20&offset=0` (offset-based; dataset is small for personal tool)
- All timestamps: ISO 8601 with timezone (`2026-02-24T10:00:00Z`)

---

### 3.2 Auth Endpoints

#### `POST /api/v1/auth/login`
```json
// Request
{ "email": "artist@example.com", "password": "SecurePass123!" }

// Response 200
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "expires_in": 604800,
  "user": { "id": "uuid", "email": "artist@example.com", "full_name": "Your Name" }
}

// Error 401
{ "detail": "Invalid credentials", "error_code": "INVALID_CREDENTIALS", "status": 401 }
```

#### `GET /api/v1/auth/me`
```json
// Response 200
{
  "id": "uuid",
  "email": "artist@example.com",
  "full_name": "Your Name",
  "spotify_connected": true,
  "created_at": "2026-02-24T10:00:00Z"
}
```

---

### 3.3 Song Endpoints

#### `GET /api/v1/songs`
Query params: `?limit=20&offset=0&genre=pop&language=hebrew&is_draft=false`
```json
// Response 200
{
  "items": [
    {
      "id": "uuid",
      "title": "שיר חדש",
      "title_english": "New Song",
      "primary_genre": "pop",
      "language_primary": "hebrew",
      "release_date": "2026-01-15",
      "album_artwork_url": "https://i.scdn.co/...",
      "is_draft": false,
      "profile_complete": true,
      "created_at": "2026-02-01T12:00:00Z"
    }
  ],
  "total": 18,
  "limit": 20,
  "offset": 0
}
```

#### `POST /api/v1/songs/fetch-spotify`
Fetches metadata from a Spotify URL without saving.
```json
// Request
{ "spotify_url": "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh" }

// Response 200
{
  "spotify_track_id": "4iV5W9uYEdYUVa79Axb7Rh",
  "spotify_uri": "spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
  "title": "שיר חדש",
  "artist_name": "Artist Name",
  "album_name": "Album Name",
  "album_artwork_url": "https://i.scdn.co/...",
  "duration_ms": 210000,
  "release_date": "2026-01-15",
  "isrc": "IL-ABC-26-00001",
  "audio_features": {
    "tempo": 120.5,
    "musical_key": 5,
    "musical_mode": 1,
    "energy": 0.72,
    "valence": 0.55,
    "acousticness": 0.15,
    "danceability": 0.68,
    "instrumentalness": 0.001,
    "liveness": 0.08,
    "loudness": -5.2,
    "speechiness": 0.04
  }
}

// Error 422 — bad URL
{ "detail": "Invalid Spotify track URL", "error_code": "INVALID_SPOTIFY_URL", "status": 422 }

// Error 404 — track not found on Spotify
{ "detail": "Track not found on Spotify", "error_code": "SPOTIFY_TRACK_NOT_FOUND", "status": 404 }
```

#### `POST /api/v1/songs`
```json
// Request (minimal — Spotify fields come from fetch-spotify first)
{
  "spotify_track_id": "4iV5W9uYEdYUVa79Axb7Rh",
  "title": "שיר חדש",
  "title_hebrew": "שיר חדש",
  "title_english": "New Song",
  "primary_genre": "pop",
  "language_primary": "hebrew",
  "mood_tags": ["uplifting", "energetic"],
  "lyrical_themes": ["love", "hope"],
  "vocal_style": ["powerful", "smooth"],
  "production_style": ["full_production", "electronic_elements"],
  "story_behind_song": "כתבתי את השיר הזה...",
  "comparable_artists": "Hanan Ben Ari, Static & Ben El",
  "radio_ready_galei_tzahal": true,
  "is_draft": false
}

// Response 201
{ "id": "uuid", ...full song object }
```

#### `GET /api/v1/songs/{song_id}`
Returns full song object including all profile fields.

#### `PUT /api/v1/songs/{song_id}`
Partial update — only provided fields are changed.

#### `DELETE /api/v1/songs/{song_id}`
```json
// Response 204 No Content
```

#### `POST /api/v1/songs/{song_id}/duplicate`
Copies mood_tags, lyrical_themes, vocal_style, production_style, comparable_artists, primary_genre from specified song into a new blank draft.
```json
// Request
{ "source_song_id": "uuid-of-song-to-copy-from" }

// Response 201 — new draft song with copied fields
{ "id": "new-uuid", "is_draft": true, ...copied fields }
```

---

### 3.4 Playlist Endpoints

#### `GET /api/v1/playlists`
Query params: `?genres=pop,mainstream&languages=hebrew&min_followers=500&max_followers=50000&submission_method=email`
```json
// Response 200
{
  "items": [
    {
      "id": "uuid",
      "name": "Israeli Hits 2026",
      "spotify_url": "https://open.spotify.com/playlist/...",
      "curator_name": "Eddie T Malakh",
      "curator_contact": "eddietmalakh@gmail.com",
      "curator_contact_method": "email",
      "follower_count": 14600,
      "genres": ["pop", "mainstream", "hebrew"],
      "languages": ["hebrew"],
      "submission_method": "email",
      "is_editorial": false
    }
  ],
  "total": 58,
  "limit": 20,
  "offset": 0
}
```

#### `GET /api/v1/playlists/match/{song_id}`
Returns playlists ranked by match score for a given song.
```json
// Response 200
{
  "items": [
    {
      "playlist": { ...playlist object },
      "match_score": 92,
      "match_reasons": [
        "Genre match: pop (primary)",
        "Language match: Hebrew",
        "Mood overlap: uplifting"
      ],
      "already_pitched": false
    }
  ]
}
```

#### `GET /api/v1/playlists/{playlist_id}`
Full playlist detail.

---

### 3.5 Radio Station Endpoints

#### `GET /api/v1/radio-stations`
Query params: `?genres=mainstream,pop`
```json
// Response 200
{
  "items": [
    {
      "id": "uuid",
      "name": "Galei Tzahal",
      "name_hebrew": "גלי צה\"ל",
      "station_type": "national",
      "contact_email": null,
      "website": "https://glz.co.il",
      "genres_focus": ["mainstream", "pop", "rock"],
      "submission_guidelines": "Submit via website form with Spotify link...",
      "submission_method": "web_form",
      "response_time_estimate": "2-4 weeks",
      "reach_description": "Largest radio audience in Israel",
      "priority_rank": 1
    }
  ]
}
```

---

### 3.6 Pitch Submission Endpoints

#### `GET /api/v1/pitches`
Query params: `?song_id=uuid&status=sent&target_type=playlist`
```json
// Response 200
{
  "items": [
    {
      "id": "uuid",
      "song_id": "uuid",
      "target_type": "playlist",
      "target_playlist": { "id": "uuid", "name": "Israeli Hits 2026" },
      "pitched_at": "2026-02-20T10:00:00Z",
      "pitch_method": "email",
      "status": "sent",
      "responded_at": null,
      "response_notes": null
    }
  ],
  "summary": {
    "total": 12,
    "sent": 8,
    "responded": 3,
    "added": 1,
    "rejected": 2,
    "no_response": 1
  }
}
```

#### `POST /api/v1/pitches`
```json
// Request
{
  "song_id": "uuid",
  "campaign_id": "uuid",
  "target_type": "playlist",
  "target_playlist_id": "uuid",
  "pitch_method": "email",
  "pitch_notes": "Sent to eddie@... mentioning our 14K stream milestone"
}
// Response 201
```

#### `PUT /api/v1/pitches/{pitch_id}`
Used to update status + response notes after curator responds.
```json
// Request
{
  "status": "rejected",
  "responded_at": "2026-02-22T15:00:00Z",
  "response_notes": "Doesn't fit our current playlist direction this month"
}
```

---

### 3.7 Campaign Endpoints

#### `GET /api/v1/campaigns`
Query params: `?status=active`

#### `POST /api/v1/campaigns`
```json
// Request
{
  "name": "Spring Single Push",
  "release_type": "single",
  "start_date": "2026-03-01",
  "end_date": "2026-04-15",
  "budget_total": 300.00,
  "primary_goal": "awareness",
  "song_ids": ["uuid-song-1"]
}
// Response 201 — campaign object
```

#### `GET /api/v1/campaigns/{campaign_id}`
Full campaign detail including:
- Attached songs
- Budget recommendation (if generated)
- Total expenses to date
- Active phase (pre_release / launch_week / post_release)

#### `POST /api/v1/campaigns/{campaign_id}/budget-recommendation`
Triggers Claude to generate a budget recommendation.
```json
// Request (optional override context)
{
  "monthly_listeners": 8500,
  "notes": "I have premium SubmitHub credits already"
}

// Response 200
{
  "id": "rec-uuid",
  "campaign_id": "uuid",
  "allocations": {
    "playlist_pitching": { "pct": 50, "amt": 150.00, "rationale": "Highest ROI channel for Hebrew pop at your listener tier. Direct pitches to mainstream playlists should be your primary focus." },
    "submithub":         { "pct": 25, "amt": 75.00,  "rationale": "Guaranteed 48h responses with curator feedback. 10-15 targeted curators at $3 each gives good coverage for $30-45." },
    "social_ads":        { "pct": 15, "amt": 45.00,  "rationale": "Supplementary — useful for targeting Israeli pop fans on Instagram but lower ROI than playlisting at this budget level." },
    "content_creation":  { "pct": 5,  "amt": 15.00,  "rationale": "Keep minimal — focus spend on distribution, not creation." },
    "pr_blogs":          { "pct": 5,  "amt": 15.00,  "rationale": "One or two Hebrew music blog pitches for credibility." },
    "other":             { "pct": 0,  "amt": 0,       "rationale": "" }
  },
  "overall_rationale": "At $300 with 8.5K monthly listeners you're in the emerging tier. Concentrate budget on playlist pitching — spreading too thin at this budget produces minimal results. SubmitHub provides accountability (paid curators must respond). Save social ads for when you have $500+ per campaign.",
  "created_at": "2026-02-24T10:00:00Z"
}
```

#### `PUT /api/v1/campaigns/{campaign_id}/budget-recommendation/{rec_id}/approve`
Saves artist's final approved allocation (may differ from AI recommendation).
```json
// Request
{
  "approved_allocations": {
    "playlist_pitching": { "pct": 45, "amt": 135.00 },
    "submithub":         { "pct": 30, "amt": 90.00 },
    "social_ads":        { "pct": 20, "amt": 60.00 },
    "content_creation":  { "pct": 5,  "amt": 15.00 },
    "pr_blogs":          { "pct": 0,  "amt": 0 },
    "other":             { "pct": 0,  "amt": 0 }
  }
}
// Response 200
```

#### `POST /api/v1/campaigns/{campaign_id}/apply-learnings`
Generates a new budget recommendation for a *future* campaign, using historical ROI data from this completed campaign as additional context.
```json
// Response 200 — same shape as budget-recommendation response
// but rationale references past performance:
// "In your Spring Single Push, social ads cost $0.18/stream vs playlist pitching at $0.04/stream.
//  Reducing social ads allocation accordingly."
```

---

### 3.8 Expense Endpoints

#### `GET /api/v1/campaigns/{campaign_id}/expenses`
```json
// Response 200
{
  "items": [...expense objects],
  "totals_by_category": {
    "playlist_pitching": 80.00,
    "submithub": 36.00,
    "social_ads": 25.00,
    "content_creation": 0,
    "pr_blogs": 0,
    "other": 6.00
  },
  "total_spent": 147.00,
  "budget_total": 300.00,
  "budget_remaining": 153.00,
  "spend_pct": 49.0
}
```

#### `POST /api/v1/campaigns/{campaign_id}/expenses`
```json
// Request
{
  "expense_date": "2026-03-10",
  "amount": 25.00,
  "category": "social_ads",
  "subcategory": "instagram_ads",
  "description": "Story ads targeting Israeli pop fans aged 18-35"
}
// Response 201
```

---

### 3.9 Campaign Performance Endpoints

#### `POST /api/v1/campaigns/{campaign_id}/performance/sync`
Manual data entry — user copies numbers from Spotify for Artists.
```json
// Request
{
  "song_id": "uuid",
  "metric_date": "2026-03-10",
  "streams_total": 4200,
  "saves_total": 380,
  "monthly_listeners": 1100,
  "followers_total": 412,
  "playlist_adds_total": 3
}
// Response 201
```

#### `GET /api/v1/campaigns/{campaign_id}/roi`
```json
// Response 200
{
  "total_spent": 147.00,
  "total_streams": 2340,
  "cost_per_stream": 0.063,
  "benchmark_cost_per_stream": { "low": 0.01, "high": 0.05 },
  "benchmark_status": "above_average",
  "by_channel": [
    {
      "category": "playlist_pitching",
      "spent": 80.00,
      "streams_attributed": 1100,
      "cost_per_stream": 0.073,
      "roi_score": 78,
      "planned_amt": 135.00,
      "variance_pct": -40.7
    },
    {
      "category": "submithub",
      "spent": 36.00,
      "streams_attributed": 520,
      "cost_per_stream": 0.069,
      "roi_score": 82,
      "planned_amt": 90.00,
      "variance_pct": -60.0
    }
  ]
}
```

---

### 3.10 Dashboard Endpoints

#### `POST /api/v1/dashboard/sync`
User manually enters weekly metrics from Spotify for Artists.
```json
// Request
{
  "snapshot_date": "2026-03-10",
  "streams_28d": 12450,
  "monthly_listeners": 892,
  "followers": 348,
  "saves_28d": 1008,
  "playlist_adds_28d": 5
}

// Response 200
{
  "snapshot_date": "2026-03-10",
  "health_score": 78,
  "save_rate": 8.1,
  "follower_conversion_rate": 39.0,
  "streams_delta_pct": 35.0,
  "listeners_delta_pct": 28.0,
  "followers_delta_pct": 12.0
}
```

#### `GET /api/v1/dashboard`
```json
// Response 200
{
  "latest_snapshot": { ...snapshot object },
  "health_score": 78,
  "health_label": "Healthy",
  "health_color": "yellow",
  "key_metrics": {
    "streams_28d": 12450,
    "monthly_listeners": 892,
    "followers": 348,
    "save_rate": 8.1,
    "playlist_adds_28d": 5
  },
  "active_campaigns": [ ...campaign summaries ],
  "top_actions": [
    { "priority": "high", "action": "Submit to 5 new playlists", "reason": "Lev Kavu'a has momentum — save rate 8.1% makes it attractive to curators", "link": "/discover" }
  ],
  "recent_insights": [ ...top 3 active insights ]
}
```

#### `GET /api/v1/dashboard/insights`
```json
// Response 200
{
  "items": [
    {
      "id": "uuid",
      "insight_type": "momentum",
      "priority": "high",
      "title": "Added to \"Israeli Hits 2026\"",
      "description": "14,600 followers · Added 3 hours ago",
      "action_text": "Thank the curator on Instagram",
      "action_link": "/pitches?song=uuid",
      "status": "active"
    }
  ]
}
```

#### `PUT /api/v1/dashboard/insights/{insight_id}`
```json
// Request
{ "status": "actioned" }  // or "dismissed"
```

---

### 3.11 Post Opportunity Endpoints

#### `GET /api/v1/opportunities`
```json
// Response 200
{
  "items": [
    {
      "id": "uuid",
      "hook": "Your song just crossed 5,000 streams — tell your followers what that milestone means to you",
      "why_now": "Milestone detected: 5,000 total streams reached today",
      "signal_type": "milestone",
      "suggested_platform": "instagram",
      "hashtag_suggestions": ["#מוזיקה_ישראלית", "#5000_השמעות", "#תודה", "#IsraeliPop", "#milestone"],
      "timing_note": "Post today or tomorrow while the milestone is fresh",
      "status": "active",
      "song": { "id": "uuid", "title": "שיר חדש" },
      "created_at": "2026-03-10T08:00:00Z"
    }
  ],
  "total_active": 4
}
```

#### `POST /api/v1/opportunities/generate`
Triggers Claude to scan current signals and generate a fresh batch.
```json
// Request (optional filter)
{ "song_id": "uuid" }  // generate for a specific song, or omit for all

// Response 200
{ "generated": 4, "items": [ ...new opportunity cards ] }
```

#### `PUT /api/v1/opportunities/{opportunity_id}`
```json
// Mark as used
{ "status": "used" }

// Dismiss
{ "status": "dismissed" }

// Remind later (3 days)
{ "status": "remind_later" }
```

---

### 3.12 Spotify OAuth Endpoints

#### `GET /api/v1/spotify/auth`
Redirects user to Spotify OAuth authorization page.
- Scopes: `user-read-private user-read-email`
- State parameter: CSRF token

#### `GET /api/v1/spotify/callback`
Handles OAuth callback, exchanges code for tokens, stores in DB.
- Redirects to frontend `/settings?spotify=connected` on success.

---

## 4. Business Logic

### 4.1 Health Score Calculation

```python
# backend/services/health_score_service.py

def calculate_health_score(snapshot: DashboardSnapshot) -> int:
    """
    0-100 score from 5 weighted components.
    Input: a single dashboard snapshot with deltas already computed.
    """

    def score_streams_trend(delta_pct: float) -> int:
        if delta_pct > 20:  return 100
        if delta_pct > 10:  return 80
        if delta_pct > 0:   return 60
        if delta_pct > -10: return 40
        return 20

    def score_save_rate(rate: float) -> int:
        if rate >= 15:  return 100
        if rate >= 10:  return 85
        if rate >= 5:   return 70
        if rate >= 3:   return 50
        return 30

    def score_follower_conversion(rate: float) -> int:
        if rate >= 10:  return 100
        if rate >= 7:   return 85
        if rate >= 5:   return 70
        if rate >= 3:   return 50
        return 30

    def score_playlist_adds(adds: int) -> int:
        if adds >= 5:   return 100
        if adds >= 3:   return 80
        if adds >= 1:   return 60
        return 40

    def score_campaign_roi(cost_per_stream: float | None) -> int:
        if cost_per_stream is None:     return 60  # no campaign = neutral
        if cost_per_stream <= 0.03:     return 100
        if cost_per_stream <= 0.05:     return 80
        if cost_per_stream <= 0.10:     return 60
        return 40

    weights = [
        (score_streams_trend(snapshot.streams_delta_pct or 0),            0.30),
        (score_save_rate(snapshot.save_rate or 0),                         0.25),
        (score_follower_conversion(snapshot.follower_conversion_rate or 0),0.20),
        (score_playlist_adds(snapshot.total_playlist_adds_28d or 0),       0.15),
        (score_campaign_roi(get_latest_campaign_roi()),                    0.10),
    ]

    return round(sum(score * weight for score, weight in weights))
```

### 4.2 Playlist Match Algorithm

```python
# backend/services/playlist_match_service.py

def match_playlists_for_song(song: Song, playlists: list[Playlist]) -> list[dict]:
    """
    Returns playlists sorted by match score with reasons.
    Score: 0-100.
    """
    results = []

    for playlist in playlists:
        score = 0
        reasons = []

        # Genre match (40 pts)
        song_genres = {song.primary_genre} | set(song.secondary_genres or [])
        playlist_genres = set(playlist.genres)
        genre_overlap = song_genres & playlist_genres
        if genre_overlap:
            pts = min(40, len(genre_overlap) * 20)
            score += pts
            reasons.append(f"Genre match: {', '.join(genre_overlap)}")

        # Language match (30 pts)
        song_lang = song.language_primary
        if song_lang in playlist.languages or 'both' in playlist.languages:
            score += 30
            reasons.append(f"Language match: {song_lang}")
        elif song.language_secondary in playlist.languages:
            score += 15
            reasons.append(f"Secondary language match")

        # Mood match (20 pts)
        song_moods = set(song.mood_tags or [])
        playlist_moods = set(playlist.mood_tags or [])
        mood_overlap = song_moods & playlist_moods
        if mood_overlap:
            pts = min(20, len(mood_overlap) * 10)
            score += pts
            reasons.append(f"Mood overlap: {', '.join(list(mood_overlap)[:2])}")

        # Submission method available (10 pts)
        if playlist.submission_method != 'spotify_for_artists' or playlist.curator_contact:
            score += 10
            reasons.append("Direct submission available")

        if score > 0:
            results.append({
                "playlist": playlist,
                "match_score": min(100, score),
                "match_reasons": reasons
            })

    return sorted(results, key=lambda x: x["match_score"], reverse=True)
```

### 4.3 Budget Recommendation Engine

```python
# backend/services/budget_recommendation_service.py

async def generate_budget_recommendation(
    campaign: Campaign,
    monthly_listeners: int,
    historical_roi: dict | None,
    anthropic_client
) -> dict:
    """
    Calls Claude to generate a justified budget split.
    Returns structured allocation JSON.
    """

    artist_tier = (
        "emerging"   if monthly_listeners < 10_000  else
        "developing" if monthly_listeners < 100_000 else
        "established"
    )

    historical_context = ""
    if historical_roi:
        historical_context = f"""
Past campaign ROI data:
{json.dumps(historical_roi, indent=2)}
Use this to upweight channels that historically performed well for this artist.
"""

    prompt = f"""You are a music marketing strategist specializing in the Israeli mainstream pop market.

Generate a specific, justified budget allocation for this promotion campaign.

CAMPAIGN DETAILS:
- Budget: ${campaign.budget_total:.2f}
- Release type: {campaign.release_type}
- Campaign duration: {(campaign.end_date - campaign.start_date).days} days
- Primary goal: {campaign.primary_goal}

ARTIST CONTEXT:
- Monthly listeners: {monthly_listeners:,}
- Artist tier: {artist_tier}
- Market: Israel, mainstream Hebrew pop
- Primary target: Galei Tzahal, large Hebrew Spotify playlists, SubmitHub curators
{historical_context}

CHANNEL OPTIONS:
1. playlist_pitching — Direct pitches to Israeli playlist curators (email/DM)
2. submithub — SubmitHub platform ($1-3 per curator submission, 70% response rate)
3. social_ads — Instagram/Facebook ads targeting Israeli pop fans
4. content_creation — Photo shoots, video content, visual assets
5. pr_blogs — Hebrew music blog outreach
6. other — Any other spend

RULES:
- Total must equal 100%
- Minimum viable spend per active channel: $10 (don't spread too thin)
- For budgets under $200: use maximum 3 channels
- For budgets $200-500: use maximum 4 channels
- If artist is emerging: prioritize playlist_pitching and submithub heavily
- Provide honest rationale — include warnings if budget is very low

Respond ONLY with valid JSON in this exact format:
{{
  "allocations": {{
    "playlist_pitching": {{ "pct": 50, "amt": 150.00, "rationale": "..." }},
    "submithub":         {{ "pct": 25, "amt": 75.00,  "rationale": "..." }},
    "social_ads":        {{ "pct": 15, "amt": 45.00,  "rationale": "..." }},
    "content_creation":  {{ "pct": 5,  "amt": 15.00,  "rationale": "..." }},
    "pr_blogs":          {{ "pct": 5,  "amt": 15.00,  "rationale": "..." }},
    "other":             {{ "pct": 0,  "amt": 0,       "rationale": "" }}
  }},
  "overall_rationale": "2-3 sentences explaining the overall strategy logic"
}}"""

    response = await anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.content[0].text)
```

### 4.4 Post Opportunity Engine

```python
# backend/services/opportunity_service.py

async def generate_opportunities(
    user_id: str,
    db: Session,
    anthropic_client,
    song_id: str | None = None
) -> list[dict]:
    """
    Scans current signals and asks Claude to generate post opportunity cards.
    """

    signals = collect_signals(user_id, db, song_id)

    if not signals:
        return []

    prompt = f"""You are a social media strategist for an Israeli mainstream pop musician.

Based on the signals below, generate 3-5 post opportunity cards. Each is a *suggestion of what to post about* — NOT the actual post text.

ARTIST CONTEXT:
- Genre: mainstream Hebrew pop
- Primary platforms: Instagram, Facebook
- Audience: Israeli fans aged 18-40
- Language: Hebrew (primary), English (secondary)

CURRENT SIGNALS:
{json.dumps(signals, indent=2, ensure_ascii=False)}

ISRAELI CALENDAR CONTEXT:
- Today: {date.today().isoformat()}
- Upcoming holidays: {get_upcoming_israeli_holidays()}
- Shabbat: Friday evening through Saturday evening (lower engagement window)

RULES FOR EACH OPPORTUNITY:
- hook: 1-2 sentences describing what to write about (NOT the post itself)
- why_now: explain the signal that makes this timely
- signal_type: one of: milestone, playlist_add, inactivity, calendar, trend, campaign_event
- suggested_platform: instagram | facebook | tiktok | all
- hashtag_suggestions: 4-8 tags (mix Hebrew + English), relevant to this specific hook
- timing_note: specific timing advice if relevant (e.g., "post before Shabbat starts Friday 6pm")

Only generate opportunities that are genuinely timely and relevant. Better to return 2 great ones than 5 mediocre ones.

Respond ONLY with valid JSON array:
[
  {{
    "hook": "...",
    "why_now": "...",
    "signal_type": "...",
    "suggested_platform": "...",
    "hashtag_suggestions": ["#...", "..."],
    "timing_note": "..."
  }}
]"""

    response = await anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.content[0].text)


def collect_signals(user_id: str, db: Session, song_id: str | None) -> list[dict]:
    """Gather all signals that could trigger post opportunities."""
    signals = []

    # 1. Stream milestones
    milestones = [1_000, 5_000, 10_000, 25_000, 50_000, 100_000]
    songs = db.query(Song).filter(Song.user_id == user_id).all()
    for song in songs:
        latest = get_latest_stream_count(song.id, db)
        for milestone in milestones:
            if latest and latest >= milestone and not milestone_already_posted(song.id, milestone, db):
                signals.append({
                    "type": "milestone",
                    "song_title": song.title,
                    "milestone": milestone,
                    "current_streams": latest
                })

    # 2. New playlist adds (pitches that changed to 'added' in last 7 days)
    recent_adds = db.query(PitchSubmission).filter(
        PitchSubmission.user_id == user_id,
        PitchSubmission.status == 'added',
        PitchSubmission.responded_at >= datetime.now() - timedelta(days=7)
    ).all()
    for pitch in recent_adds:
        signals.append({
            "type": "playlist_add",
            "song_title": pitch.song.title,
            "playlist_name": pitch.target_playlist.name if pitch.target_playlist else pitch.target_name,
            "days_ago": (datetime.now() - pitch.responded_at).days
        })

    # 3. Inactivity (no opportunity used in X days)
    last_used = db.query(PostOpportunity).filter(
        PostOpportunity.user_id == user_id,
        PostOpportunity.status == 'used'
    ).order_by(PostOpportunity.used_at.desc()).first()

    if not last_used or (datetime.now() - last_used.used_at).days >= 7:
        signals.append({
            "type": "inactivity",
            "days_since_last_post_idea_used": (datetime.now() - last_used.used_at).days if last_used else 30
        })

    # 4. Recent releases (within last 30 days)
    recent_songs = [s for s in songs if s.release_date and (date.today() - s.release_date).days <= 30]
    for song in recent_songs:
        days_since = (date.today() - song.release_date).days
        signals.append({
            "type": "recent_release",
            "song_title": song.title,
            "days_since_release": days_since
        })

    return signals
```

### 4.5 Budget Pacing Alert

```python
def check_budget_pacing(campaign: Campaign, total_spent: float) -> dict | None:
    """Returns alert dict if spending is off-pace, else None."""
    today = date.today()
    campaign_days = (campaign.end_date - campaign.start_date).days
    days_elapsed = (today - campaign.start_date).days

    if campaign_days == 0 or days_elapsed <= 0:
        return None

    pct_time_elapsed = days_elapsed / campaign_days
    pct_budget_spent = total_spent / float(campaign.budget_total)

    # 80% budget consumed
    if pct_budget_spent >= 0.80:
        return {
            "type": "budget_80pct",
            "message": f"80% of budget consumed with {int((1 - pct_time_elapsed) * 100)}% of campaign remaining.",
            "severity": "warning"
        }

    # More than 20% ahead of expected pace
    if pct_budget_spent > pct_time_elapsed + 0.20:
        overage_pct = round((pct_budget_spent - pct_time_elapsed) * 100)
        return {
            "type": "ahead_of_pace",
            "message": f"Spending {overage_pct}% ahead of expected pace. Consider slowing down to preserve budget for launch week.",
            "severity": "info"
        }

    return None
```

---

## 5. External Service Integrations

### 5.1 Spotify Web API

**Authentication for track fetching:** Client Credentials Flow (app-level, no user login needed for metadata).
**Authentication for user data (Phase 2):** Authorization Code Flow with PKCE.

```python
# backend/services/spotify_service.py

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyService:

    def __init__(self, client_id: str, client_secret: str):
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.client = spotipy.Spotify(auth_manager=auth_manager)

    def fetch_track(self, spotify_url: str) -> dict:
        """
        Fetches track metadata + audio features from a Spotify URL.
        Raises SpotifyAPIError on failure.
        """
        try:
            track_id = self._extract_track_id(spotify_url)
            track = self.client.track(track_id)
            features = self.client.audio_features(track_id)[0]
            return self._merge_track_data(track, features)
        except spotipy.SpotifyException as e:
            if e.http_status == 401:
                raise SpotifyAuthError("Spotify credentials invalid")
            if e.http_status == 404:
                raise SpotifyTrackNotFound(f"Track not found: {track_id}")
            raise SpotifyAPIError(f"Spotify API error: {e}")

    def _extract_track_id(self, url: str) -> str:
        """Handles URLs: https://open.spotify.com/track/ID or spotify:track:ID"""
        if "spotify:track:" in url:
            return url.split("spotify:track:")[1]
        if "open.spotify.com/track/" in url:
            return url.split("/track/")[1].split("?")[0]
        raise ValueError("Invalid Spotify track URL")
```

**Endpoints used:**
- `GET /v1/tracks/{id}` — title, artist, album, artwork, release date, ISRC
- `GET /v1/audio-features/{id}` — tempo, key, energy, valence, etc.

**Rate limits:**
- 100 requests / 30 seconds per app
- All fetched track data cached in `songs` table — never re-fetch unless user requests refresh
- Implement exponential backoff on 429 responses

**Error handling:**
| HTTP Status | Action |
|-------------|--------|
| 401 | Re-authenticate with client credentials |
| 404 | Return user-friendly "track not found" error |
| 429 | Backoff 1s, 2s, 4s — then fail with error |
| 5xx | Retry up to 3 times — then fail gracefully |

---

### 5.2 Anthropic API

**Model:** `claude-sonnet-4-20250514`

**Used for two features:**
1. Budget recommendation generation
2. Post opportunity generation

```python
# backend/config.py / shared client setup

from anthropic import AsyncAnthropic

def get_anthropic_client() -> AsyncAnthropic:
    return AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
```

**Token budget per call:**

| Feature | Input tokens (est.) | Output tokens (est.) | Cost/call (est.) |
|---------|--------------------|-----------------------|-----------------|
| Budget recommendation | ~600 | ~400 | ~$0.003 |
| Opportunity generation | ~800 | ~600 | ~$0.004 |

**Daily rate limit (self-imposed):**
```python
# Prevent runaway costs — 20 Claude calls/day max
MAX_CLAUDE_CALLS_PER_DAY = 20
```

**Error handling:**
| Error | Action |
|-------|--------|
| `APIConnectionError` | Retry once after 2s; if fails, return 503 with user message |
| `RateLimitError` | Return 429 to frontend with "Try again in a moment" |
| `APIStatusError` 500 | Log full error, return 502 to frontend |
| JSON parse failure | Log raw response, return 422 with "AI response was malformed" |

**Response validation:**
All Claude responses are JSON. Validate with Pydantic before saving:
```python
class BudgetAllocationItem(BaseModel):
    pct: float = Field(ge=0, le=100)
    amt: float = Field(ge=0)
    rationale: str

class BudgetRecommendationResponse(BaseModel):
    allocations: dict[str, BudgetAllocationItem]
    overall_rationale: str

    @validator('allocations')
    def total_must_equal_100(cls, v):
        total = sum(item.pct for item in v.values())
        if abs(total - 100) > 0.5:
            raise ValueError(f"Allocations sum to {total}%, not 100%")
        return v
```

---

## 6. Security Specifications

### 6.1 Authentication

- **Algorithm:** HS256 JWT (RS256 not needed for single-user personal tool)
- **Token lifetime:** 7 days
- **Secret:** 64-character random string in `SECRET_KEY` env var
- **No refresh token flow in MVP** — user simply re-logs in after expiry
- **Single account:** Only one user may register. After first registration, registration endpoint is disabled.

```python
# Enforce single-user: block registration if any user exists
@router.post("/auth/register", status_code=201)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).count() > 0:
        raise HTTPException(403, "This is a single-user application")
    ...
```

### 6.2 API Key Security

```
# .env file — NEVER commit to git
ANTHROPIC_API_KEY=sk-ant-...
SPOTIFY_CLIENT_ID=...
SPOTIFY_CLIENT_SECRET=...
SECRET_KEY=64-random-chars
DATABASE_URL=postgresql://user:pass@localhost/music_promo
```

`.gitignore` must include:
```
.env
*.env
.env.*
!.env.example
```

### 6.3 Input Validation

- All request bodies validated via Pydantic models — invalid input returns 422 automatically
- SQL injection: SQLAlchemy ORM parameterizes all queries — never use raw string interpolation
- XSS: Backend returns JSON only (no HTML rendering); frontend uses React which escapes by default
- URL validation: Spotify URLs validated with regex before any API call

### 6.4 CORS

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

In production: replace with actual deployed frontend URL.

### 6.5 Rate Limiting (Self-protection)

```python
# Prevent accidental Claude API overuse
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/opportunities/generate")
@limiter.limit("10/hour")  # max 10 AI calls per hour
async def generate_opportunities(...):
    ...

@router.post("/campaigns/{id}/budget-recommendation")
@limiter.limit("20/day")
async def budget_recommendation(...):
    ...
```

---

## 7. Performance Requirements

### 7.1 Response Time Targets

| Endpoint type | Target (p95) |
|---------------|-------------|
| Simple CRUD reads | < 100ms |
| List endpoints with filters | < 200ms |
| Dashboard aggregate | < 300ms |
| Spotify track fetch (external) | < 5s |
| Claude budget recommendation | < 15s |
| Claude opportunity generation | < 20s |
| Frontend initial page load (LCP) | < 2s |

### 7.2 Database Indexes

Key indexes defined in schema section. Additional notes:
- `pitch_submissions`: index on `(song_id, status)` for per-song pitch tracking
- `campaign_performance`: index on `(campaign_id, metric_date DESC)` for time-series queries
- `post_opportunities`: index on `(user_id, status)` for dashboard feed

### 7.3 N+1 Prevention

Use SQLAlchemy eager loading for related objects:
```python
# Example: load pitches with their playlist + radio info in one query
pitches = (
    db.query(PitchSubmission)
    .options(
        joinedload(PitchSubmission.target_playlist),
        joinedload(PitchSubmission.target_radio),
        joinedload(PitchSubmission.song)
    )
    .filter(PitchSubmission.song_id == song_id)
    .all()
)
```

### 7.4 Frontend Caching

TanStack Query cache configuration:
```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,   // 5 minutes — data is fresh, no refetch
      gcTime: 1000 * 60 * 30,     // 30 minutes — keep in memory
      retry: 2,
    },
  },
})
```

Longer cache for slow-changing data:
```typescript
// Playlists database — changes rarely
useQuery({ queryKey: ['playlists'], staleTime: 1000 * 60 * 60 }) // 1 hour
```

---

## 8. Infrastructure & Development Setup

### 8.1 Environment Variables

```bash
# backend/.env
DATABASE_URL=postgresql://music_user:password@localhost:5432/music_promo_dev
SECRET_KEY=replace-with-64-random-chars
ANTHROPIC_API_KEY=sk-ant-api03-...
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
SPOTIFY_REDIRECT_URI=http://localhost:8000/api/v1/spotify/callback
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# frontend/.env.local
VITE_API_URL=http://localhost:8000/api/v1
```

### 8.2 Development Setup (Windows / PowerShell)

```powershell
# 1. Clone and enter project
cd music_manager

# 2. Start PostgreSQL (via Docker)
docker run -d `
  --name music-promo-db `
  -e POSTGRES_USER=music_user `
  -e POSTGRES_PASSWORD=password `
  -e POSTGRES_DB=music_promo_dev `
  -p 5432:5432 `
  postgres:15

# 3. Backend setup
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 4. Run migrations + seed data
alembic upgrade head

# 5. Start backend dev server
uvicorn app.main:app --reload --port 8000

# 6. Frontend setup (new terminal)
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

### 8.3 Backend requirements.txt

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.35
alembic==1.13.2
psycopg2-binary==2.9.9
pydantic==2.9.2
pydantic-settings==2.5.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
httpx==0.27.2
spotipy==2.24.0
anthropic==0.34.2
slowapi==0.1.9
python-dotenv==1.0.1
```

### 8.4 Frontend package.json (key dependencies)

```json
{
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.26.0",
    "@tanstack/react-query": "^5.56.0",
    "axios": "^1.7.7",
    "react-hook-form": "^7.53.0",
    "zod": "^3.23.8",
    "@hookform/resolvers": "^3.9.0"
  },
  "devDependencies": {
    "typescript": "^5.5.3",
    "vite": "^5.4.0",
    "@vitejs/plugin-react": "^4.3.0",
    "tailwindcss": "^3.4.11",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.45"
  }
}
```

### 8.5 Deployment (TBD — Railway recommended)

Railway is recommended for its simplicity with FastAPI + PostgreSQL:

```
Option A: Railway (recommended for personal tool)
  - Backend: Deploy from GitHub, auto-detect Python
  - Database: Railway managed PostgreSQL addon
  - Frontend: Deploy to Railway or Vercel (static)
  - Cost: ~$5-10/month

Option B: Render
  - Similar to Railway, free tier available (with limitations)
  - PostgreSQL: Render managed DB

Option C: Local only (valid for personal tool)
  - Run docker-compose locally
  - No external hosting cost
  - Accessible only from your machine
```

`docker-compose.yml` for local full-stack run:
```yaml
version: '3.9'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: music_user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: music_promo_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file: ./backend/.env
    depends_on:
      - db
    volumes:
      - ./backend:/app
      - ./logs:/app/logs

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000/api/v1

volumes:
  postgres_data:
```

---

## 9. Testing Strategy

### 9.1 TDD Workflow (mandatory for every User Story)

This project uses **Test-Driven Development**. No feature code is written before its tests exist.

The cycle for each User Story:

```
1. READ   — understand the US acceptance criteria
2. WRITE  — create the test file with input/output tuples covering all cases
3. RUN    — pytest → all new tests must FAIL (red) before implementation starts
4. BUILD  — implement the feature
5. RUN    — pytest → all tests must PASS (green)
6. COMMIT — tests + implementation committed together
```

If a test passes before implementation, the test is wrong — fix it first.

---

### 9.2 Test File Naming Convention

```
backend/tests/
├── conftest.py                       # shared fixtures (db, client, sample data)
│
├── unit/                             # pure logic, no DB or HTTP
│   ├── test_us001_health_score.py
│   ├── test_us001_playlist_match.py
│   ├── test_us008_budget_pacing.py
│   └── test_us004_spotify_url_parse.py
│
└── integration/                      # DB + HTTP, uses TestClient
    ├── test_us001_song_crud.py
    ├── test_us002_spotify_fetch.py
    ├── test_us004_playlist_filter.py
    ├── test_us006_pitch_tracking.py
    ├── test_us007_campaign_create.py
    ├── test_us008_budget_recommendation.py
    ├── test_us009_expense_tracking.py
    ├── test_us010_campaign_roi.py
    ├── test_us011_dashboard_sync.py
    ├── test_us014_opportunities.py
    └── test_us015_opportunity_history.py
```

File naming: `test_us{number}_{short_description}.py` — maps 1:1 to User Stories in the PRD.

---

### 9.3 Test Infrastructure

**Test database:** Separate PostgreSQL database, created/destroyed per test session.

```python
# backend/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "postgresql://music_user:password@localhost:5432/music_promo_test"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(engine):
    """Each test gets a clean, rolled-back DB transaction."""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# --- Shared sample data fixtures ---

@pytest.fixture
def sample_user(db):
    from app.models.user import User
    from app.utils.auth import hash_password
    user = User(email="artist@test.com", password_hash=hash_password("test1234"), full_name="Test Artist")
    db.add(user)
    db.commit()
    return user

@pytest.fixture
def auth_headers(client, sample_user):
    resp = client.post("/api/v1/auth/login", json={"email": "artist@test.com", "password": "test1234"})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_song(db, sample_user):
    from app.models.song import Song
    song = Song(
        user_id=sample_user.id,
        title="שיר בדיקה",
        title_english="Test Song",
        primary_genre="pop",
        language_primary="hebrew",
        mood_tags=["uplifting", "energetic"],
        story_behind_song="This is a test story " * 15,  # 200+ words minimum
    )
    db.add(song)
    db.commit()
    return song

@pytest.fixture
def sample_campaign(db, sample_user, sample_song):
    from app.models.campaign import Campaign, CampaignSong
    from datetime import date, timedelta
    campaign = Campaign(
        user_id=sample_user.id,
        name="Test Campaign",
        release_type="single",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=30),
        budget_total=300.00,
        primary_goal="awareness",
    )
    db.add(campaign)
    db.flush()
    db.add(CampaignSong(campaign_id=campaign.id, song_id=sample_song.id))
    db.commit()
    return campaign
```

**Running tests:**
```powershell
# From backend/ directory
pytest tests/ -v                          # all tests
pytest tests/unit/ -v                     # unit tests only
pytest tests/integration/ -v              # integration tests only
pytest tests/ -k "us008" -v               # one user story
pytest tests/ --tb=short                  # compact failure output
```

---

### 9.4 Input/Output Tuple Pattern

Every test file defines cases as a list of tuples before writing any test function. This makes coverage explicit and readable.

**Example — US-011: Health Score (unit test)**

```python
# backend/tests/unit/test_us011_health_score.py
"""
US-011: Health Score Calculation
Acceptance: 0-100 score; correct color bands; weighted formula
"""
import pytest
from app.services.health_score_service import calculate_health_score, get_health_label

# (streams_delta_pct, save_rate, follower_conv_rate, playlist_adds, cost_per_stream,
#  expected_min, expected_max, expected_label)
HEALTH_SCORE_CASES = [
    # Strong across all metrics → Excellent
    (30, 12.0, 9.0, 5, 0.03,   85, 100, "Excellent"),
    # Good but not great → Healthy
    (15,  8.0, 6.0, 2, 0.05,   70,  84, "Healthy"),
    # Mediocre — streams flat, save rate low → Needs Work
    ( 2,  4.0, 3.5, 1, 0.08,   50,  69, "Needs Work"),
    # Everything poor → Critical
    (-25, 1.5, 1.0, 0, 0.20,    0,  49, "Critical"),
    # Good streams but terrible save rate → pulled down
    (35,  2.0, 8.0, 3, 0.04,   55,  75, "Needs Work"),
    # No campaign ROI data (None) → treated as neutral
    (20,  9.0, 7.0, 3, None,   75,  95, "Healthy"),
]

@pytest.mark.parametrize(
    "streams_delta, save_rate, follower_conv, playlist_adds, cost_per_stream, exp_min, exp_max, exp_label",
    HEALTH_SCORE_CASES
)
def test_health_score_range(
    streams_delta, save_rate, follower_conv, playlist_adds,
    cost_per_stream, exp_min, exp_max, exp_label
):
    score = calculate_health_score(
        streams_delta_pct=streams_delta,
        save_rate=save_rate,
        follower_conversion_rate=follower_conv,
        playlist_adds_28d=playlist_adds,
        cost_per_stream=cost_per_stream,
    )
    assert exp_min <= score <= exp_max, (
        f"Expected score in [{exp_min}, {exp_max}] for inputs "
        f"(streams_delta={streams_delta}, save_rate={save_rate}...), got {score}"
    )
    assert get_health_label(score) == exp_label
```

**Example — US-001: Song creation via API (integration test)**

```python
# backend/tests/integration/test_us001_song_crud.py
"""
US-001 / US-002: Add and manage songs
Acceptance: create, read, update, delete; Spotify fields stored; story required
"""
import pytest

# (payload, expected_status, expected_field_checks)
CREATE_SONG_CASES = [
    # Happy path — full profile
    (
        {
            "title": "שיר חדש",
            "title_english": "New Song",
            "primary_genre": "pop",
            "language_primary": "hebrew",
            "mood_tags": ["uplifting", "energetic"],
            "story_behind_song": "This is a long enough story " * 12,
        },
        201,
        {"title": "שיר חדש", "primary_genre": "pop", "is_draft": False}
    ),
    # Draft — story not required when is_draft=True
    (
        {
            "title": "טיוטא",
            "primary_genre": "pop",
            "language_primary": "hebrew",
            "is_draft": True,
        },
        201,
        {"is_draft": True}
    ),
    # Missing required field: title
    (
        {"primary_genre": "pop", "language_primary": "hebrew"},
        422,
        {}
    ),
    # story_behind_song too short when not draft
    (
        {
            "title": "Short Story Song",
            "primary_genre": "pop",
            "language_primary": "hebrew",
            "story_behind_song": "Too short",
            "is_draft": False,
        },
        422,
        {}
    ),
]

@pytest.mark.parametrize("payload, expected_status, field_checks", CREATE_SONG_CASES)
def test_create_song(client, auth_headers, payload, expected_status, field_checks):
    resp = client.post("/api/v1/songs", json=payload, headers=auth_headers)
    assert resp.status_code == expected_status
    if field_checks:
        data = resp.json()
        for key, value in field_checks.items():
            assert data[key] == value, f"Expected {key}={value}, got {data[key]}"

def test_get_song_not_found(client, auth_headers):
    resp = client.get("/api/v1/songs/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert resp.status_code == 404

def test_delete_song(client, auth_headers, sample_song):
    resp = client.delete(f"/api/v1/songs/{sample_song.id}", headers=auth_headers)
    assert resp.status_code == 204
    resp = client.get(f"/api/v1/songs/{sample_song.id}", headers=auth_headers)
    assert resp.status_code == 404
```

**Example — US-008: Budget pacing alert (unit test)**

```python
# backend/tests/unit/test_us008_budget_pacing.py
"""
US-008 / US-009: Budget pacing alerts
Acceptance: alert at 80% consumed; alert if 20%+ ahead of pace
"""
import pytest
from datetime import date, timedelta
from app.services.budget_recommendation_service import check_budget_pacing
from unittest.mock import MagicMock

def make_campaign(budget_total, start_days_ago, duration_days):
    campaign = MagicMock()
    campaign.budget_total = budget_total
    campaign.start_date = date.today() - timedelta(days=start_days_ago)
    campaign.end_date = campaign.start_date + timedelta(days=duration_days)
    return campaign

# (budget_total, start_days_ago, campaign_duration, spent, expected_alert_type)
PACING_CASES = [
    # 80% of budget spent, campaign only half done → budget_80pct alert
    (300, 15, 30, 245.00, "budget_80pct"),
    # Spending 30% ahead of pace → ahead_of_pace alert
    (300, 10, 30, 140.00, "ahead_of_pace"),   # 10/30 days = 33% time, but 47% spent
    # On pace — no alert
    (300, 15, 30, 145.00, None),
    # Under-spending — no alert
    (300, 20, 30,  50.00, None),
    # Campaign not started yet — no alert
    (300,  0, 30,   0.00, None),
    # 80% alert takes priority over pacing alert
    (300,  5, 30, 250.00, "budget_80pct"),
]

@pytest.mark.parametrize(
    "budget_total, start_days_ago, duration, spent, expected_type",
    PACING_CASES
)
def test_budget_pacing(budget_total, start_days_ago, duration, spent, expected_type):
    campaign = make_campaign(budget_total, start_days_ago, duration)
    result = check_budget_pacing(campaign, spent)
    if expected_type is None:
        assert result is None, f"Expected no alert but got: {result}"
    else:
        assert result is not None, "Expected an alert but got None"
        assert result["type"] == expected_type
```

---

### 9.5 Tests for Claude-Dependent Features

Budget recommendation and opportunity generation call the Anthropic API. Tests mock the Claude client to avoid real API calls and costs.

```python
# backend/tests/integration/test_us008_budget_recommendation.py
"""
US-008: AI Budget Recommendation
Acceptance: returns valid allocation; sums to 100%; rationale present; saved to DB
"""
import pytest
import json
from unittest.mock import AsyncMock, MagicMock

RECOMMENDATION_CASES = [
    # Small budget emerging artist → concentrated split
    (
        {"budget_total": 150.00, "release_type": "single", "monthly_listeners": 3000},
        # Claude mock returns this
        {
            "allocations": {
                "playlist_pitching": {"pct": 60, "amt": 90.00, "rationale": "Best ROI"},
                "submithub":         {"pct": 30, "amt": 45.00, "rationale": "Guaranteed responses"},
                "social_ads":        {"pct": 10, "amt": 15.00, "rationale": "Supplement"},
                "content_creation":  {"pct": 0,  "amt": 0,     "rationale": ""},
                "pr_blogs":          {"pct": 0,  "amt": 0,     "rationale": ""},
                "other":             {"pct": 0,  "amt": 0,     "rationale": ""},
            },
            "overall_rationale": "Concentrate on playlists at this budget size."
        },
        200,
        100.0,   # expected total pct
    ),
    # Album campaign, larger budget → more channels
    (
        {"budget_total": 600.00, "release_type": "album", "monthly_listeners": 25000},
        {
            "allocations": {
                "playlist_pitching": {"pct": 40, "amt": 240.00, "rationale": "Core"},
                "submithub":         {"pct": 20, "amt": 120.00, "rationale": "Coverage"},
                "social_ads":        {"pct": 20, "amt": 120.00, "rationale": "Reach"},
                "content_creation":  {"pct": 10, "amt": 60.00,  "rationale": "Assets"},
                "pr_blogs":          {"pct": 10, "amt": 60.00,  "rationale": "Credibility"},
                "other":             {"pct": 0,  "amt": 0,      "rationale": ""},
            },
            "overall_rationale": "Album warrants PR and content investment."
        },
        200,
        100.0,
    ),
]

@pytest.mark.parametrize(
    "campaign_context, claude_mock_response, expected_status, expected_total_pct",
    RECOMMENDATION_CASES
)
def test_budget_recommendation(
    client, auth_headers, sample_campaign, db,
    campaign_context, claude_mock_response, expected_status, expected_total_pct,
    monkeypatch
):
    # Patch the Anthropic client so no real API call is made
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=json.dumps(claude_mock_response))]
    mock_client = AsyncMock()
    mock_client.messages.create = AsyncMock(return_value=mock_message)
    monkeypatch.setattr("app.api.campaigns.get_anthropic_client", lambda: mock_client)

    # Update campaign budget to match test case
    client.put(
        f"/api/v1/campaigns/{sample_campaign.id}",
        json={"budget_total": campaign_context["budget_total"]},
        headers=auth_headers
    )

    resp = client.post(
        f"/api/v1/campaigns/{sample_campaign.id}/budget-recommendation",
        json={"monthly_listeners": campaign_context["monthly_listeners"]},
        headers=auth_headers
    )

    assert resp.status_code == expected_status
    data = resp.json()

    # Allocations must sum to 100%
    total_pct = sum(v["pct"] for v in data["allocations"].values())
    assert abs(total_pct - expected_total_pct) < 0.5, f"Allocations sum to {total_pct}%, expected 100%"

    # Rationale must be present
    assert data["overall_rationale"]
    for channel, alloc in data["allocations"].items():
        if alloc["pct"] > 0:
            assert alloc["rationale"], f"Missing rationale for channel: {channel}"
```

---

### 9.6 What Is NOT Unit Tested

To avoid over-engineering for a personal tool:
- **Claude prompt content** — not tested; prompts are iterated manually
- **React UI components** — Playwright MCP covers end-to-end flows
- **Spotify API responses** — mocked in integration tests; real data verified manually
- **Database migrations** — verified by running `alembic upgrade head` against test DB

Phase 2 will add Vitest component tests and full Playwright E2E automation as the codebase stabilizes.

---

## 10. Monitoring & Observability

### 10.1 Logging

```python
# backend/utils/logging.py
import logging
import json
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(f"logs/{name}.log")
    handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    ))
    logger.addHandler(handler)
    return logger
```

**What gets logged:**
- All API calls to Spotify (request + response status)
- All calls to Anthropic (prompt summary + token count + response time)
- All database write operations
- All errors with full stack traces
- Budget recommendation inputs/outputs (for debugging and review)

**Log files:**
```
logs/
├── app.log           # General application logs
├── spotify.log       # All Spotify API interactions
├── anthropic.log     # All Claude API calls
└── errors.log        # Errors only
```

Log rotation: daily, keep 30 days (handled by Python's `RotatingFileHandler`).

### 10.2 Error Monitoring

MVP: Log to files + FastAPI exception handlers return structured errors.

Phase 2: Add Sentry for automatic error capture and alerting.

### 10.3 Health Check Endpoint

```python
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

## 11. Feasibility Review

### 11.1 Technical Feasibility Assessment

| Feature | Complexity | Risk | Notes |
|---------|-----------|------|-------|
| Spotify track fetch | Low | Low | Spotipy is mature; client credentials flow is simple |
| Song profile CRUD | Low | Low | Standard FastAPI + SQLAlchemy |
| Playlist matching algorithm | Low | Low | Simple scoring, no ML needed |
| Manual pitch tracking | Low | Low | CRUD with status machine |
| Campaign + expense tracking | Low | Low | Standard data management |
| Budget recommendation (Claude) | Medium | Low | Claude handles complex reasoning; JSON validation needed |
| Post opportunity engine (Claude) | Medium | Medium | Signal collection logic needs careful design; Claude output may vary |
| Health score calculation | Low | Low | Pure math, deterministic |
| Dashboard sync (manual) | Low | Low | Just a form that saves numbers |
| Hebrew RTL display | Low | Low | CSS `dir="rtl"` + Heebo font; React handles it |
| SubmitHub brief generation | Low | Low | Template + song profile data |

### 11.2 PRD Requirements Coverage Check

| PRD Requirement | Covered in Tech Spec? |
|----------------|----------------------|
| Song profile with Spotify fetch | ✅ Section 3.3, 5.1 |
| "Duplicate from last song" | ✅ `POST /songs/{id}/duplicate` |
| Curated Israeli playlist database | ✅ Schema + seed migrations |
| Playlist match scoring | ✅ Section 4.2 |
| Radio station contacts | ✅ `radio_stations` table + endpoints |
| Pitch tracking per song | ✅ `pitch_submissions` table + endpoints |
| SubmitHub campaign planner | ✅ `submithub_campaigns` + `submithub_submissions` |
| Campaign creation (single/EP/album) | ✅ `release_type` field + campaign endpoints |
| AI budget recommendation | ✅ Section 4.3 + budget_recommendations table |
| Actual vs planned spend comparison | ✅ Expenses endpoint + ROI endpoint |
| "Apply learnings" to next campaign | ✅ `POST /campaigns/{id}/apply-learnings` |
| Health score (0-100) | ✅ Section 4.1 |
| Dashboard insights | ✅ `insights` table + endpoints |
| Manual Spotify data sync | ✅ `POST /dashboard/sync` |
| Post opportunity engine | ✅ Section 4.4 + `post_opportunities` table |
| Hebrew RTL content display | ✅ Section 8.1, frontend utils/hebrew.ts |
| English UI throughout | ✅ All interface text in English |
| Phase 2 AI audio analysis ready | ✅ AI fields in `songs` table (nullable) |

### 11.3 Identified Technical Gaps / Decisions Needed

1. **Milestone deduplication:** The opportunity engine needs to track which stream milestones have already been surfaced to prevent repeating the same "you hit 5K streams!" suggestion. The `collect_signals()` function calls `milestone_already_posted()` — this needs a simple tracking table or a flag on `post_opportunities`. **Decision: add `milestone_surfaced_json JSONB` to `songs` table to store which milestones have been surfaced.**

2. **Israeli holiday calendar:** The opportunity engine references `get_upcoming_israeli_holidays()` — this needs an implementation. Options: hardcode the next 12 months of holidays; use the `jewish-holidays` Python library; or use an external API. **Decision: hardcode a static list for MVP, refresh annually.**

3. **`streams_attributed` per channel in ROI:** The ROI endpoint claims to show streams per channel. But there's no causal attribution between an expense category and streams. The actual implementation must be transparent about this: streams are *total* from Spotify, not causally split. ROI will show *cost per channel* alongside *total streams* — not "Instagram ads drove X streams." This should be clearly labeled in the UI.

4. **Spotify OAuth scope:** For MVP (track fetch only), Client Credentials flow is sufficient — no user OAuth needed. The `/api/v1/spotify/auth` and `/api/v1/spotify/callback` endpoints can be deferred to Phase 2 (when we do Spotify for Artists auto-sync).

---

## 12. Open Technical Questions

| Question | Options | Recommended |
|----------|---------|-------------|
| Deployment target | Railway / Render / Local-only | **Local-only for MVP** — simplest; personal tool doesn't need public hosting |
| Frontend hosting | Same server / Vercel / Served by FastAPI | **FastAPI serves built frontend** — single process, simpler deployment |
| Spotify OAuth (Phase 2) | Authorization Code / PKCE | PKCE (more secure, no backend secret needed for frontend flow) |
| Israeli holiday data | Hardcoded / library (`pyluach`) / API | **`pyluach` library** — handles Hebrew calendar including moveable feasts |
| Background jobs | None / Celery / APScheduler | **None in MVP** — all Claude calls are on-demand, synchronous |
| File storage (receipts) | Not in MVP | Skip — expense receipts are optional and noted as such in PRD |
| Log aggregation | Local files / Sentry | **Local files for MVP** — Sentry in Phase 2 |

---

## Approval Sign-Off

- [ ] Architecture reviewed — system design is sound
- [ ] Database schema reviewed — all entities and relationships correct
- [ ] API endpoints reviewed — all PRD features covered
- [ ] Business logic reviewed — algorithms are correct
- [ ] Security reviewed — auth, input validation, API key protection adequate
- [ ] Infrastructure reviewed — development setup is clear and reproducible

**Created by:** Claude Code
**Reviewed by:** [Your name]
**Date reviewed:** [Date]
**Approved:** [ ]

---

## Next Steps After Approval

1. Install dependencies: `pip install -r requirements.txt` + `npm install`
2. Run initial migration: `alembic upgrade head` (creates all tables + seeds playlists/radio)
3. Begin Week 1: project structure, DB connection, auth, Spotify fetch endpoint
4. Reference this document throughout implementation — update it when technical decisions change
