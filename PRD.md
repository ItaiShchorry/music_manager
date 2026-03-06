# Product Requirements Document (PRD)
## Israeli Music Promotion Tool — Creative Companion Edition

**Version:** 2.0
**Date:** March 6, 2026
**Status:** Active — Week 7 Implementation Complete
**Author:** Claude Code (based on 6 component design docs + user interviews + Week 7 vision session)

---

## 1. Executive Summary

### 1.1 Problem Statement

As an independent Israeli artist releasing mainstream Hebrew pop at a high cadence (singles, EPs, and albums) with a growing catalog, the core challenges are:

- **Discovery gap:** The Israeli music landscape has hundreds of Spotify playlists, curators, and radio shows. No single place to find which ones are right for a specific song.
- **Strategy gap:** Even when targets are found, it's unclear *how* to approach each one — what angle to pitch, what the optimal budget split is, which channels give the best ROI.
- **Promotion chaos:** Tracking pitches, follow-ups, and results is currently scattered across notes apps and memory.
- **Content opportunity blindness:** Knowing *what to post about*, *when* — missing timely hooks like milestones, release anniversaries, and cultural moments.
- **Creative inertia:** The hardest part of music-making is often starting. There's no system to surface specific, personalized creative challenges that make creation feel like a game rather than a task.
- **YouTube gap:** YouTube is the primary long-form platform for artist discovery, but no structured workflow exists for planning, producing, and publishing video content.
- **Motivation loss:** Solo creation is isolating. Without structure, streaks, or feedback, it's easy to go weeks without creating anything new.

### 1.2 Solution Overview

A **personal web application** that serves as a full-stack music promotion command center AND a gamified creative companion — purpose-built for one artist releasing mainstream Hebrew pop in Israel.

**The tool does for music promotion what a DAW does for recording:** it doesn't replace the artist's judgment, but provides the structure, data, and smart suggestions that make every decision faster and better.

**In Week 7, the vision expanded to a second dimension:** the tool is now a *creative companion* as much as a promotion tool. The opportunity engine is redesigned as a personal manager and coach — surfacing creative challenges, not just promotional angles.

**The core gamified loop (added in Week 7):**
1. Open app → Manager homepage shows 3 opportunity cards (quests)
2. Accept one → full-screen Challenge Mode opens (text editor, audio/video recorder)
3. Create → submit
4. Celebration screen (level-up + badge award)
5. Share button → caption auto-prepared for social

### 1.3 Target User

**Primary (and only) user:** The artist who built this tool.

- Israeli artist releasing mainstream Hebrew pop/pop-rock
- Active catalog: 10-30 songs, with ongoing high-cadence releases
- Release cadence: variable — singles, EPs, albums
- Primary promotion targets: Galei Tzahal, large Hebrew Spotify playlists, SubmitHub curators
- **Also needs:** structured creative challenges, YouTube content planning, motivation through gamification
- Uses Spotify for Artists for analytics; promotes primarily on Instagram, Facebook, and YouTube

### 1.4 Success Criteria

The tool is a success if the artist:
1. Uses it actively for every new release (not abandoned after 2 songs)
2. Has all catalog songs profiled with Spotify data + creative metadata
3. Consistently finds new, relevant Israeli promotion targets they hadn't discovered before
4. Receives and acts on specific budget allocation recommendations per release
5. **Completes at least 1 creative challenge per week** (new in v2.0)
6. **Has YouTube video briefs planned for major songs** (new in v2.0)
7. **Maintains a creative streak of 3+ days per month** (new in v2.0)
8. Has a clear record of every pitch submitted — no more guessing "did I already contact them?"

---

## 2. Background

### 2.1 The Israeli Music Landscape

**Mainstream Hebrew Pop Context:**
- **Primary radio targets:** Galei Tzahal (גלי צה"ל) — largest radio audience in Israel; mainstream pop/rock.
- **Secondary radio:** Kan Gimel (כאן גימל) — mainstream pop focus; Reshet Gimmel — classic/pop crossover.
- **Spotify playlists:** "Top 50 Israel" (76.8K followers), "Israeli Hits 2025" (14.6K followers), and dozens of Hebrew-language mainstream curator playlists.
- **SubmitHub:** Active ecosystem of curators covering mainstream Hebrew pop; $1-3 per submission, 70% response rate.
- **YouTube:** Primary long-form discovery platform for Israeli audiences. Behind-the-scenes, acoustic sessions, and song explainers drive sustained engagement beyond the initial release window.

### 2.2 The Creative Companion Vision (Added v2.0)

Beyond promotion, the tool is redesigned as a **personal music manager and coach**. The key insight:

> Creative challenges should feel like quests, not chores. The tool should know your catalog — its themes, moods, influences, gaps — and serve you personalized challenges that are *specific, surprising, and fun*.

**Three pillars replace the old dashboard-centric model:**

| Pillar | Purpose | Primary Audience Benefit |
|--------|---------|--------------------------|
| **CREATE** | Daily creative challenges + YouTube planning | Stay creatively active between releases |
| **SHARE** | Promotional opportunities + campaigns | Make the most of every release window |
| **TRACK** | Health score + insights + performance | Understand what's working |

### 2.3 Current Workflow (Without This Tool)

**Promotion workflow:**
1. Release song on Spotify
2. Search for playlists → inconsistent results
3. Cold email/DM curators → no template, no tracking
4. Submit to SubmitHub manually → no record
5. Post social content → written from scratch each time
6. Check Spotify for Artists weekly → no context for what numbers mean

**Creative workflow:**
1. Open DAW when inspired → often nothing comes
2. No record of experiments or sketches
3. YouTube video ideas exist but never get structured
4. No external accountability or motivation system

**Time cost estimate:** 4-8 hours per song release in promotion admin + creative output drops between major releases.
**Target with this tool:** <1.5 hours per song release in admin + consistent creative output through challenge system.

---

## 3. Product Vision

### 3.1 Core Philosophy (v2.0)

**"Create. Share. Track."**

Every feature answers one of six questions:
1. **What should I create today?** (Creative challenges — US-019, US-021)
2. **What YouTube video should I plan?** (YouTube briefs — US-016, US-017)
3. **Where should I promote this song?** (Components 1, 2, 3)
4. **How should I promote it — and how much should I spend?** (Component 4)
5. **How is my promotion performing?** (Component 5)
6. **What social opportunities am I missing right now?** (Component 6 + US-019)

The tool is a **strategic advisor AND creative companion**, not an executor. The artist makes all final calls — the tool provides structure, suggestions, and motivation.

### 3.2 The Manager Homepage (US-020 — New in v2.0)

The homepage (`/manager`) is redesigned around the three-pillar structure:

**CREATE section (top — primary focus):**
- 3 active creative/YouTube challenge cards (quests)
- Each card: "Accept Challenge" → opens Challenge Mode overlay
- YouTube Queue widget (briefs in progress)
- User progress widget (level badge + streak counter)

**SHARE section (middle):**
- Promotion opportunity cards
- Active campaigns with budget bars
- Next pitch reminders

**TRACK section (bottom):**
- Health score card
- Up to 3 latest AI insights
- Quick links to full dashboard

### 3.3 The Gamified Creative Loop (US-021, US-022 — New in v2.0)

**Challenge Mode (full-screen overlay):**
- Text editor for lyric/verse/caption challenges
- Audio recorder (MediaRecorder API) for instrumental challenges
- "Submit Challenge ✓" → saves creation, marks opportunity used, updates progress

**Celebration Screen:**
- Level-up notification if threshold crossed
- Badge notification if earned
- Auto-generated caption for sharing
- "Next Challenge" → returns to Manager

**User Progress (streak + level + badges):**
- Levels: Newcomer (0-4) → Emerging (5-14) → Pro (15-29) → Expert (30+)
- Badges: First Spark, Three-Day Streak, Week on Fire, Ten Creations, Publisher, YouTube Debut
- Streak resets if no challenge completed in 24h+

### 3.4 Non-Goals (v2.0)

- No multi-user support — single-user tool
- No mobile app — responsive web only
- No automated ad spend execution — advisory only
- No Meta/Google Ads API — expenses logged manually
- No email/notification system — in-app only
- No public-facing pages — purely internal tool
- No real-time audio analysis — upload only (in future)

---

## 4. User Stories

### Priority 1 — Core Promotion (US-001 through US-015) — COMPLETE

#### Song Management

**US-001: Add a song via Spotify link** ✅
```
As an artist,
I want to paste a Spotify track URL and have the app auto-fill song metadata,
So that I don't have to manually enter title, duration, release date, and artwork.

Acceptance Criteria: ✅ All implemented
- Paste Spotify URL → fetch title, duration, release date, album artwork
- Fallback manual entry if Spotify link not available
- Duplicate detection prevents re-adding same track
```

**US-002: Complete a song's creative profile** ✅
```
As an artist,
I want to fill in the creative details about my song (mood, story, comparable artists),
So that the tool can make accurate promotion recommendations.

Acceptance Criteria: ✅ All implemented
- Fields: genre, language (hebrew/english/both), mood tags, themes, comparable artists
- Story behind the song (free text)
- "Copy profile from [song]" to pre-fill from most recent other song
```

**US-003: View my full song library** ✅
```
As an artist,
I want to see all my songs in a list,
So that I can manage my catalog efficiently.
```

#### Promotion Discovery

**US-004: Find relevant playlists for a song** ✅
**US-005: Find radio contacts** ✅
**US-006: Track all pitches for a song** ✅

#### Campaign & Budget

**US-007: Create a promotion campaign** ✅
**US-008: Get AI budget allocation recommendation** ✅
**US-009: Log and track actual expenses** ✅
**US-010: View campaign ROI and apply learnings** ✅

#### Dashboard & Insights

**US-011: View my music health at a glance** ✅
**US-012: Receive actionable AI insights** ✅
**US-013: Sync Spotify data** ✅

#### Social Content Opportunity Engine

**US-014: Get post opportunity suggestions** ✅
**US-015: See opportunity history** ✅

#### Post-MVP Polish ✅
- SubmitHub pitch brief generator (Claude-generated pitch text per campaign)
- Duplicate song profile helper (one-click copy from previous song)
- Campaign Apply Learnings (Claude analyzes planned vs actual channel spend)

---

### Priority 1 — Creative Companion (US-016 through US-022) — COMPLETE (Week 7)

#### YouTube Content

**US-016: YouTube Video Brief Generator** ✅
```
As an artist,
I want to generate an SEO-optimized YouTube video brief for any song,
So that I have a structured plan before I film — not a blank page.

Acceptance Criteria: ✅ All implemented
- Select concept_type: making_of | acoustic_session | production_breakdown | song_explained | live_performance
- Optional: key_message (max 200 chars), context (max 300 chars)
- Claude returns:
  - seo_title: eye-catching, ≤70 characters
  - hook_paragraph: 100-150 words
  - chapters: 3-5 with {timestamp, title, what_to_cover}
  - video_description: 300-500 chars, uses search_keywords naturally
  - tags: 8-12, mix Hebrew + English
- Saved with status="draft"; multiple briefs per song allowed
- Falls back to structured placeholder if Claude fails
- Lives in dedicated "YouTube Briefs" section in SongDetailPage
```

**US-017: YouTube Brief Lifecycle Management** ✅
```
As an artist,
I want to move my video brief through a draft → filmed → published workflow,
So that I always know what stage each video is at.

Acceptance Criteria: ✅ All implemented
- PATCH /youtube-briefs/{id} — update status
- filmed_at auto-set when status → filmed
- published_at auto-set + youtube_url required when status → published
- youtube_url validated (must be youtube.com or youtu.be)
- 422 if trying to publish without youtube_url
- POST /youtube-briefs/{id}/stats — log views/likes/comments/subscribers_gained (upsert on duplicate date)
- GET /youtube-briefs — list all user's briefs (?status= filter)
- DELETE — hard delete, 204
```

#### Song Enhancement

**US-018: SEO Search Keywords on Song** ✅
```
As an artist,
I want to tag my songs with search keywords,
So that generated YouTube descriptions are optimized for how people actually search.

Acceptance Criteria: ✅ All implemented
- New search_keywords: list[str] | null field on Song model
- Edited via TagInput chip input in SongDetailPage (same UX as mood_tags)
- Empty list normalized to null
- Included in SongUpdate PATCH, SongResponse, YouTube brief prompts
- Displayed below the Comparable Artists field with explanatory label
```

#### Creative Opportunity Engine

**US-019: Creative Opportunity Engine (major expansion)** ✅
```
As an artist,
I want my opportunity engine to act as a personal creative coach —
not just a social media reminder, but a catalog-aware creative challenger,
So that I always have a specific, fun, actionable creative challenge waiting for me.

Acceptance Criteria: ✅ All implemented
- New `category` field on PostOpportunity: 'creative' | 'youtube' | 'promotion'
- 6 new creative signal types (all category='creative'):
  - lyric_prompt: verse/hook challenge based on existing mood/themes
  - catalog_gap: catalog has emotional/genre imbalance → fill the gap
  - song_experiment: try something new with an existing song
  - style_exploration: try a technique from a comparable artist
  - instrumental_challenge: specific time-boxed task (e.g., 45-second build)
  - cover_idea: cover suggestion based on comparable_artists
- 4 YouTube signal types (category='youtube'):
  - story_ready: song.story > 100 chars AND no brief exists
  - no_video: song > 60 days old AND no filmed/published brief
  - brief_filmed_unpublished: filmed brief > 7 days old → nudge to publish
  - youtube_milestone: stream milestone AND no brief in last 30 days
- Redesigned Claude prompt:
  - Role: "You are this artist's personal creative manager and music coach"
  - Full catalog context: titles, genres, moods, themes, comparable_artists, stories
  - Diversity axes: genre cross-pollination, tempo, goofiness, perspective flip, language play, constraints
  - Explicit instruction: "Be specific, playful, surprising. Never give generic advice."
- OpportunityCard UI updates:
  - category='creative': amber border, "Accept Challenge" button
  - category='youtube': red badge, "Plan Video" button
  - category='promotion': unchanged indigo, "Use This" button
- collect_signals() now receives songs list directly, adds creative + YouTube signals
```

#### Challenge Completion

**US-021: Challenge Completion Flow** ✅
```
As an artist,
I want to accept a challenge, create within the app, and experience a satisfying completion moment,
So that the creative loop feels fun and self-contained — not just another to-do.

Acceptance Criteria: ✅ All implemented
- Challenge Mode (full-screen overlay):
  - Text editor for lyric/caption/note challenges
  - Signal type determines mode: lyric_prompt/catalog_gap/style_exploration → text; others → text + future audio
  - "Submit Challenge ✓" button + "Back" button
- On submit:
  - POST /challenges/{opportunity_id}/complete → 201, CreationEntry saved
  - Opportunity marked as 'used'
  - UserProgress created/updated
- Celebration Screen:
  - Level-up notification if threshold crossed
  - Badge notification for newly earned badges
  - Auto-generated shareable caption based on challenge type + content
  - "Copy Caption" button
  - "Next Challenge" → dismisses overlay
- File upload: POST /uploads (multipart) → returns file_url
  - Stored to backend/uploads/{user_id}/
  - Served via /uploads static files
- GET /challenges — list user's creation entries (?status= filter)
```

#### Gamification

**US-022: User Progress & Gamification** ✅
```
As an artist,
I want to see my creative streak, level, and earned badges,
So that I have a persistent motivation system that makes creation feel like a game.

Acceptance Criteria: ✅ All implemented
- UserProgress model (one per user):
  - streak_current, streak_best, last_challenge_date
  - total_completed
  - level: newcomer | emerging | pro | expert
  - badges: [{badge_type, earned_at}]
- Level thresholds:
  - newcomer: 0-4 completed
  - emerging: 5-14 completed
  - pro: 15-29 completed
  - expert: 30+ completed
- Streak logic:
  - last_challenge_date = yesterday → streak_current + 1
  - last_challenge_date = today → no change
  - else → streak_current = 1
  - streak_best updated if current > best
- Badges:
  - first_spark: first challenge completed
  - three_day_streak: 3 consecutive days
  - week_on_fire: 7 consecutive days
  - ten_creations: 10 total completions
  - publisher: first Share used
  - youtube_debut: first YouTube brief published
- GET /me/progress — returns full UserProgress for current user
- ProgressWidget displays: level badge, streak counter, progress bar to next level, recent badge emojis
```

#### Manager Homepage

**US-020: Manager Homepage** ✅
```
As an artist,
I want a homepage that leads with creative challenges rather than analytics,
So that opening the app feels energizing, not administrative.

Acceptance Criteria: ✅ All implemented
- / redirects to /manager
- Nav: "Manager" link added, "Dashboard" kept for legacy access
- Three sections:
  CREATE (top):
    - 3 active creative/youtube opportunity cards
    - "Generate Ideas ✨" button
    - YouTube Queue widget
    - Progress widget
  SHARE (middle):
    - Promotion opportunity cards
    - Active campaigns
  TRACK (bottom):
    - Health score card
    - Up to 3 AI insights
    - Quick links (Songs, Discover, Campaigns, Dashboard)
```

---

### Priority 2 — Future Features

**US-023: Creative Review System (design stub)**
```
Three options under consideration:
A) AI Feedback on text entries: Claude reads lyrics and gives structured feedback
B) Self-reflection prompts: 2 questions after celebration screen
C) Weekly Manager Report: Claude generates weekly creative coaching summary
D) Social feedback: public preview link + emoji reactions

Recommended phasing: B in US-021 as small addition → A for text → C as standalone
```

**US-101: AI audio analysis integration** (SONOTELLER/Cyanite)
**US-102: Spotify for Artists API auto-sync**
**US-103: Automated budget execution** (Meta/Google Ads API)
**US-104: Geographic insights map**
**US-105: Weekly narrative recap**
**US-106: SubmitHub API integration**
**US-107: Israeli current events feed**
**US-108: Hebrew transliteration helper**
**US-109: EP/album-specific campaign templates**

---

## 5. Feature Requirements

### 5.1 Component 1: Smart Song Profile

**Functional Requirements:**
- Spotify API integration: fetch metadata from track URL
- Manual creative entry: mood tags, themes, story, comparable artists, genre, language
- **New (v2.0):** `search_keywords` field for YouTube SEO
- "Copy profile from last song" button
- Save as draft

**Data stored per song (v2.0 additions):**
- `search_keywords`: list of SEO search phrases for YouTube descriptions

---

### 5.2 Component 2: Israeli Playlist & Radio Discovery

**Functional Requirements:**
- Curated database: 25 Israeli Spotify playlists + 6 radio stations seeded at launch
- Auto-filter by song profile (genre, language, mood)
- Match score display with reasoning
- Pitch tracking: "Mark Pitched" per playlist/station
- "Pitch →" redirect links: email (mailto:), Spotify for Artists, Instagram DM, SubmitHub

---

### 5.3 Component 3: SubmitHub Integration

**Functional Requirements:**
- Campaign planner: select relevant curators, track per-curator status
- **AI brief generator:** Claude generates 2-3 sentence pitch text from song profile
- "Generate with AI ✨" button in each SubmitHub campaign
- Budget integration: SubmitHub spend tracked as campaign expense

---

### 5.4 Component 4: Campaign & Budget Management

**Functional Requirements:**
- Campaign CRUD: name, dates, budget, release type, attached songs, primary goal
- AI budget recommendation per campaign (Claude)
- Expense tracking: actual vs planned per channel
- **Apply Learnings:** Claude analyzes planned vs actual channel spend → per-channel verdict + next suggestions
- Channel verdicts: on_track / over_budget / under_budget / not_used / unplanned

---

### 5.5 Component 5: Dashboard & Insights Engine

**Health Score Formula:**
```
health_score = (
  streams_trend × 0.30 +
  save_rate      × 0.25 +
  follower_conv  × 0.20 +
  playlist_adds  × 0.15 +
  campaign_roi   × 0.10
)
```
Labels: ≥85 Excellent | ≥70 Healthy | ≥50 Needs Work | <50 Critical

**Insight types:** momentum | warning | opportunity | tip | milestone

**Endpoints:** POST /dashboard/snapshots, GET /dashboard/health-score, POST /dashboard/insights/generate, GET /dashboard/insights, PATCH /dashboard/insights/{id}

---

### 5.6 Component 6: Social Content Opportunity Engine (v2.0)

**Enhanced in v2.0 — now a creative manager, not just a social reminder.**

**Three opportunity categories:**

| Category | Signal Types | Card Style | Button |
|----------|-------------|-----------|--------|
| `promotion` | milestone, playlist_add, inactivity, calendar, recent_release | Indigo border | "Use This" |
| `creative` | lyric_prompt, catalog_gap, song_experiment, style_exploration, instrumental_challenge, cover_idea | Amber border | "Accept Challenge" |
| `youtube` | story_ready, no_video, brief_filmed_unpublished, youtube_milestone | Red border | "Plan Video" |

**Redesigned Claude prompt (v2.0):**
- Role: "You are this artist's personal creative manager and music coach"
- Full catalog context passed (titles, genres, moods, themes, comparable_artists, story excerpts)
- ~60% creative challenges, ~40% promotional ideas
- Diversity axes: genre cross-pollination, tempo, goofiness, perspective flip, language play, constraints
- Instruction: "Be specific, playful, surprising. Never give generic advice."

---

### 5.7 Component 7: YouTube Video Briefs (New in v2.0)

**Purpose:** Plan YouTube content before filming. Gives the artist a structured brief with SEO-optimized title, hook, chapters, and description — so filming has a clear goal.

**Brief lifecycle:** draft → planned → filmed → published

**Concept types:** making_of | acoustic_session | production_breakdown | song_explained | live_performance

**Generated fields:** seo_title (≤70 chars), hook_paragraph (100-150 words), chapters (3-5), video_description (300-500 chars, uses search_keywords), tags (8-12, Hebrew + English)

**Stats tracking:** POST /youtube-briefs/{id}/stats — log views, likes, comments, subscribers_gained per date (upsert on duplicate)

**YouTube Queue Widget:** Shown on Manager homepage — lists briefs in progress with status indicators.

---

### 5.8 Component 8: Challenge Completion & Creation (New in v2.0)

**Purpose:** Close the loop between challenge surfacing and actual creative output. The artist creates *inside* the tool, not in a separate app.

**Creation modes by signal type:**
- Text editor: lyric_prompt, catalog_gap, style_exploration, milestone, playlist_add, inactivity, story_ready
- Future audio: instrumental_challenge, song_experiment, cover_idea (scaffolded)

**File upload:** POST /uploads (multipart) → `/uploads/{user_id}/{uuid}_{filename}` → served as static files

**Creation entry:** Stores content_type, text_content, file_url, external_url, caption_draft, status (draft | published)

---

### 5.9 Component 9: User Progress & Gamification (New in v2.0)

**Purpose:** Persistent motivation that makes creation habit-forming. Levels, streaks, and badges create extrinsic motivation while the creative challenges provide intrinsic value.

**Level progression:**

| Level | Challenges Completed | Unlock |
|-------|---------------------|--------|
| Newcomer | 0-4 | Starting out |
| Emerging | 5-14 | Blue level badge |
| Pro | 15-29 | Indigo level badge |
| Expert | 30+ | Amber level badge |

**Badges:**

| Badge | Trigger | Emoji |
|-------|---------|-------|
| first_spark | First challenge completed | ✨ |
| three_day_streak | 3 consecutive days | 🔥 |
| week_on_fire | 7 consecutive days | 🚀 |
| ten_creations | 10 total completions | 🎯 |
| publisher | First share used | 📢 |
| youtube_debut | First YouTube brief published | 🎬 |

---

## 6. User Experience Requirements

### 6.1 Design Principles (v2.0 Updated)

1. **Create first:** The homepage leads with creative challenges, not analytics. The artist should feel energized when they open the app, not burdened.
2. **Efficiency above all:** Every promotion workflow completable in <5 minutes. Every challenge completable in <20 minutes.
3. **Familiar patterns:** Standard web app UI. No learning curve.
4. **Hebrew content, English UI:** Interface in English. Generated content properly formatted for Hebrew (RTL, `dir="rtl" lang="he"`).
5. **Progressive disclosure:** Most important thing first. Advanced options available but not in the way.
6. **Celebration moments:** Level-ups, badges, and confetti make creation feel rewarding — not just productive.

### 6.2 Key User Flows (v2.0)

**Flow 1: Daily Creative Check-in (2-5 min)**
1. Open Manager (`/`) → see CREATE section
2. Review 3 creative challenge cards
3. Accept one → Challenge Mode opens
4. Write verse / note / caption
5. Submit → Celebration screen → copy caption → close

**Flow 2: YouTube Brief Planning (5-10 min)**
1. Go to Song Detail page → YouTube Briefs section
2. Click "Generate Brief" → select concept type
3. Review generated seo_title, chapters, tags
4. Save as draft → advance to planned when ready to film
5. After filming: mark filmed → add youtube_url → publish

**Flow 3: New Release Setup (15-20 min)**
1. Dashboard → "Add New Song"
2. Paste Spotify URL → auto-fetch metadata
3. Fill creative profile (mood tags, story, comparable artists, search_keywords)
4. Create campaign → enter budget → review AI recommendation → approve
5. Discover playlists → log pitches
6. Generate SubmitHub campaign brief → submit manually → track results
7. Check Manager → creative challenges will reference the new song

**Flow 4: Weekly Promotion Check-in (5-10 min)**
1. Open Manager → SHARE section
2. Act on any promotion opportunity cards
3. Open Dashboard → sync Spotify data → review insights
4. Update pitch statuses (any new responses?)
5. Log any expenses spent this week

**Flow 5: Post-Campaign Review (10 min)**
1. Open completed campaign → click "Analyze Campaign ✨"
2. Review per-channel verdicts (on_track / over_budget etc.)
3. Read next-campaign suggestions
4. Use findings when creating next campaign's budget recommendation

### 6.3 Navigation Structure (v2.0)

```
Top Navigation:
├── Manager        (home — CREATE / SHARE / TRACK pillars)
├── Songs          (library + add new + song detail/profile)
├── Discover       (playlists + radio stations + match scores)
├── Campaigns      (create + manage + budget + learnings)
└── Dashboard      (health score + insights + Spotify sync)

Song Detail Page Sections:
├── Spotify metadata (read-only)
├── Song Profile (genre, language, story, mood tags, themes, comparable artists, search_keywords)
├── Social Content Generation (Hebrew captions + hashtags)
├── YouTube Briefs (generate + lifecycle management)
├── SubmitHub Campaigns
└── Pitch History
```

### 6.4 Hebrew & RTL Requirements

- Generated Hebrew text displayed with `dir="rtl" lang="he"`
- Font: Heebo or Rubik for Hebrew characters
- Mixed Hebrew-English text: `unicode-bidi: plaintext`
- Hashtags and URLs display correctly in mixed RTL/LTR context
- Copy-to-clipboard preserves RTL formatting for WhatsApp/Instagram paste

---

## 7. Technical Requirements

### 7.1 Performance
- Page load: <2 seconds (Manager, song list, dashboard)
- Spotify API fetch: <5 seconds
- Claude brief/opportunity generation: <15 seconds
- Database queries: <200ms for all standard views

### 7.2 Security
- JWT authentication (single user, but protect data and API keys)
- API keys stored in environment variables, never in code
- OWASP Top 10 awareness
- File uploads: user-scoped directories, UUID-prefixed filenames

### 7.3 Reliability
- SQLite for development/testing; PostgreSQL-ready
- Error logging to `/logs` directory
- Graceful fallbacks: Spotify API down → manual entry; Claude API down → structured placeholder

### 7.4 Stack
- **Backend:** Python 3.11+, FastAPI, PostgreSQL/SQLite, SQLAlchemy, Alembic
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, TanStack Query
- **AI:** Anthropic Python SDK, Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- **External APIs:** Spotify Web API (track metadata)
- **File Storage:** Local filesystem (`backend/uploads/`) with StaticFiles serving
- **Deployment:** TBD (Railway or Render)

---

## 8. Data Model Summary

### Core Tables (v1.0 — Complete)

| Table | Purpose |
|-------|---------|
| `users` | Single user authentication |
| `songs` | Song catalog with Spotify + creative metadata (incl. `search_keywords` v2.0) |
| `playlists` | Curated Israeli playlist database |
| `radio_stations` | Radio station contacts + submission info |
| `pitch_submissions` | Every pitch made, with status + response |
| `generated_content` | Hebrew social captions (Claude-generated) |
| `campaigns` | Promotion campaigns with budget |
| `campaign_songs` | Many-to-many: campaigns ↔ songs |
| `expenses` | All promotion expenses, categorized |
| `submithub_campaigns` | SubmitHub-specific campaign tracking |
| `submithub_submissions` | Per-curator results |
| `dashboard_snapshots` | Aggregated daily metrics + health score |
| `insights` | AI-generated insight cards |
| `post_opportunities` | Opportunity cards; `category` field added v2.0 |

### New Tables (v2.0 — Complete)

| Table | Purpose |
|-------|---------|
| `youtube_briefs` | AI-generated video briefs per song, with full lifecycle |
| `youtube_brief_stats` | Performance snapshots per brief (views, likes, etc.) |
| `creation_entries` | Records of completed challenges (text, file_url, caption_draft) |
| `user_progress` | Gamification state: streak, level, badges per user |

Full schema in `TECH_SPEC.md`.

---

## 9. API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /register` — single-user lock enforced ✅
- `POST /login` — returns JWT ✅
- `GET /me` — requires auth ✅

### Songs (`/api/v1/songs`)
- `POST /` — create (fetches Spotify metadata) ✅
- `GET /` — list all for user ✅
- `GET /{id}` — get one ✅
- `PATCH /{id}` — update manual fields incl. genre, language, **search_keywords** ✅
- `DELETE /{id}` — delete ✅
- `GET /{id}/matches` — ranked playlist + radio station matches ✅
- `GET /{id}/pitches` — pitch history for song ✅
- `POST /{id}/content` — generate Hebrew social content (Claude) ✅
- `GET /{id}/content` — list previously generated content ✅
- `POST /{id}/youtube-briefs` — generate + save YouTube brief ✅ (v2.0)
- `GET /{id}/youtube-briefs` — list briefs for song ✅ (v2.0)

### YouTube Briefs (`/api/v1/youtube-briefs`)
- `GET /` — list all user briefs (?status= filter) ✅ (v2.0)
- `GET /{id}` — get single brief ✅ (v2.0)
- `PATCH /{id}` — update status/url (filmed_at auto-set, youtube_url validated on publish) ✅ (v2.0)
- `DELETE /{id}` — hard delete 204 ✅ (v2.0)
- `POST /{id}/stats` — log performance snapshot (upsert on duplicate date) ✅ (v2.0)
- `GET /{id}/stats` — list snapshots ✅ (v2.0)

### Challenges (`/api/v1/`)
- `POST /challenges/{opportunity_id}/complete` — save CreationEntry + mark opportunity used + update progress ✅ (v2.0)
- `GET /challenges` — list user's creation entries (?status_filter=) ✅ (v2.0)
- `POST /uploads` — multipart file upload → returns file_url ✅ (v2.0)

### Progress (`/api/v1/me/progress`)
- `GET /me/progress` — returns UserProgress for current user ✅ (v2.0)

### Opportunities (`/api/v1/opportunities`)
- `GET /opportunities` — list active (incl. `category` field) ✅
- `POST /opportunities/generate` — generate via Claude (creative + YouTube + promotion) ✅
- `PATCH /opportunities/{id}` — mark used / dismissed / remind_later ✅

### All other existing endpoints: Playlists, Radio Stations, Pitches, Campaigns, SubmitHub, Dashboard — ✅

---

## 10. Success Metrics (v2.0)

### Promotion KPIs (Unchanged)

| Metric | Target |
|--------|--------|
| Songs profiled | 80%+ of catalog |
| Pitches logged | Every submission recorded (100%) |
| Time per new release admin | <1.5 hours |
| Budget recommendations used | Every campaign reviewed before launch |
| Campaign budget adherence | Within 10% of planned total |
| Health score | Maintained above 70 |

### Creative Companion KPIs (New in v2.0)

| Metric | Target |
|--------|--------|
| Creative challenges completed per month | 4+ (1 per week minimum) |
| Streak best | 3+ days at least once per month |
| YouTube briefs created | At least 1 per major song |
| YouTube briefs published | At least 1 per quarter |
| User level | Reach "Emerging" within first month of consistent use |
| Creative categories used | Mix of lyric, instrumental, and style challenges |

---

## 11. Roadmap

### MVP 1 (Weeks 1-6): Foundation + All 6 Core Components ✅ COMPLETE

| Week | Focus |
|------|-------|
| 1 | Project setup, DB, auth, Spotify API |
| 2 | Component 1: Song profile builder |
| 3 | Component 2: Playlist discovery + pitch tracking |
| 4 | Component 3: SubmitHub planner + Component 6: Hebrew content generation |
| 5 | Component 4: Campaign/budget + AI recommendation engine |
| 6 | Component 5: Dashboard + insights + opportunity engine + polish |

### Week 7: Creative Companion ✅ COMPLETE

- US-016: YouTube Video Brief Generator
- US-017: Brief lifecycle management
- US-018: SEO search keywords on Song
- US-019: Creative Opportunity Engine (3 categories, 10 new signal types, redesigned Claude prompt)
- US-020: Manager homepage (CREATE / SHARE / TRACK pillars)
- US-021: Challenge Completion Flow (ChallengeMode overlay, CelebrationScreen, file uploads)
- US-022: User Progress & Gamification (streaks, levels, badges)

### Phase 2 (Weeks 8-12): AI Enhancement + Automation

- **US-023:** Creative Review System — AI feedback on lyrics/verses + weekly coaching report
- **US-101:** Spotify for Artists API auto-sync (replace manual data entry)
- **US-102:** AI audio analysis (SONOTELLER integration for song profiling)
- **US-103:** Automated budget execution: Meta/Google Ads API
- **US-104:** Israeli current events feed → richer signals
- **US-105:** Geographic insights map
- **US-106:** Weekly narrative recap (auto-generated "your week in music")
- **US-107:** In-browser audio recorder for instrumental challenges (MediaRecorder API)
- **US-108:** YouTube API sync for brief stats (replace manual entry)

### Phase 3 (Months 4-6): Depth & Polish

- Mobile-responsive refinements
- Export features (PDF pitch history, CSV expenses)
- Reminder system for follow-up pitches
- Advanced analytics (song comparison, cross-campaign ROI)
- Public preview link for sharing creation entries

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Spotify API rate limits | Medium | Medium | Cache all fetched data; don't re-fetch unnecessarily |
| Claude API cost spikes | Low | Low | Rate limit generation; cache outputs |
| Playlist database goes stale | High | Medium | Manual update process; "last verified" date per entry |
| Tool abandoned after 2 songs | **Low (v2.0)** | High | Creative challenges + gamification create daily return habit |
| Creative challenges feel generic | Medium | High | Catalog-specific prompts in Claude; diversity axes in prompt design |
| Upload storage grows large | Low | Medium | User-scoped directories; future: S3 integration |
| YouTube brief data goes stale | Medium | Low | Manual stats entry; future: YouTube API auto-sync |

---

## 13. Open Questions

| Question | Options | Decision |
|----------|---------|---------|
| Deployment target | Railway / Render / local-only | TBD — local-only acceptable for MVP |
| File upload storage for production | Local filesystem / S3 / Cloudinary | Local for now; S3 in Phase 2 |
| Audio recorder for challenges | MediaRecorder API / third-party | MediaRecorder scaffolded; full implementation in Phase 2 |
| Hebrew font hosting | Google Fonts (Heebo) / self-hosted | Google Fonts |
| Content generation rate limit | Per session / per day | 20 generations/day limit |
| Backup strategy | Automated cron / manual | Manual pg_dump acceptable for personal use |

---

## 14. Appendix

### A. Opportunity Categories at a Glance

| Category | Signal Types | Card Color | Button Label |
|----------|-------------|-----------|-------------|
| `promotion` | milestone, playlist_add, inactivity, calendar, recent_release | Indigo | "Use This" |
| `creative` | lyric_prompt, catalog_gap, song_experiment, style_exploration, instrumental_challenge, cover_idea | Amber | "Accept Challenge" |
| `youtube` | story_ready, no_video, brief_filmed_unpublished, youtube_milestone | Red | "Plan Video" |

### B. Level & Badge Reference

**Levels:** Newcomer (0-4) → Emerging (5-14) → Pro (15-29) → Expert (30+)

**Badges:**
- ✨ first_spark — complete first challenge
- 🔥 three_day_streak — 3 consecutive days
- 🚀 week_on_fire — 7 consecutive days
- 🎯 ten_creations — 10 total completions
- 📢 publisher — first Share used
- 🎬 youtube_debut — first YouTube brief published

### C. YouTube Brief Concept Types

| Concept | Description |
|---------|-------------|
| making_of | Behind-the-scenes of how the song was made |
| acoustic_session | Stripped-down acoustic performance |
| production_breakdown | Technical deep-dive into beats and production |
| song_explained | Songwriter explains meaning and inspiration |
| live_performance | Live performance video |

### D. AI Content Generation Cost Estimate

Using Claude Sonnet 4 (`claude-sonnet-4-20250514`):
- Content generation: ~$0.006 per generation (3 tone variants)
- YouTube brief: ~$0.004 per brief
- Opportunity generation: ~$0.003 per batch
- Total at 100 generations/month: ~$0.60/month — negligible

### E. Israeli Playlist Seed Data
25 Israeli playlists + 6 radio stations seeded in database. Full list in `backend/app/services/seed.py`.

---

**Document Status:** Active — v2.0 reflects Week 7 completion
**Last Updated:** March 6, 2026
**Next Review:** After Phase 2 implementation begins
