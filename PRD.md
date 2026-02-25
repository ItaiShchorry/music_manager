# Product Requirements Document (PRD)
## Israeli Music Promotion Tool — Personal Edition

**Version:** 1.1
**Date:** February 24, 2026
**Status:** Draft — Awaiting Review
**Author:** Claude Code (based on 6 component design docs + user interviews)

---

## 1. Executive Summary

### 1.1 Problem Statement

As an independent Israeli artist releasing mainstream Hebrew pop at a high cadence (singles, EPs, and albums) with a growing catalog (10-30 songs), the core challenge is **not** producing music — it's knowing *where*, *how*, and *when* to promote it. Specifically:

- **Discovery gap:** The Israeli music landscape has hundreds of Spotify playlists, curators, radio shows, and submission channels. There's no single place to find which ones are right for a specific song.
- **Strategy gap:** Even when targets are found, it's unclear *how* to approach each one — what angle to pitch, what the optimal budget split is, which channels give the best ROI for this type of release, and in what order to act.
- **Targeting mismatch:** Mainstream Hebrew pop has different targets than indie/alternative. Galei Tzahal, large Hebrew-language playlists, and mainstream playlist curators require different approaches and contacts than indie channels.
- **Promotion chaos:** Keeping track of what was pitched, to whom, when, what resulted — currently managed in notes apps or memory. Easy to miss follow-ups, repeat pitches, or fail to spot patterns.
- **Content opportunity blindness:** Knowing *what* to post about at the right moment is hard — missing timely hooks like milestone achievements, current events, or release anniversaries that would resonate with an Israeli audience.
- **Budget uncertainty:** With a limited promotion budget, it's unclear how to divide spend across channels (playlists, SubmitHub, social ads) to maximize ROI for each specific song and release type.
- **Insight blindness:** Spotify for Artists provides raw data but no interpretation. Hard to know if a campaign is actually working or what to do next.

### 1.2 Solution Overview

A **personal web application** that serves as a full-stack music promotion command center — purpose-built for one artist releasing mainstream Hebrew pop in Israel. It centralizes song profiles, promotion targeting, campaign strategy, budget recommendations, and AI-powered content opportunity suggestions in one place.

**The tool does for music promotion what a DAW does for recording:** it doesn't replace the artist's judgment, but provides the structure, data, and smart suggestions that make every decision faster and better. The artist still makes all final calls — the tool is a strategic advisor, not an autopilot.

### 1.3 Target User

**Primary (and only) user:** The artist who built this tool.

- Israeli artist releasing mainstream Hebrew pop/pop-rock
- Active catalog: 10-30 songs, with ongoing high-cadence releases (singles, EPs, albums)
- Release cadence: variable — could be a single every few weeks, an EP with multiple songs, or a full album campaign
- Primary promotion targets: Galei Tzahal, large Hebrew Spotify playlists, SubmitHub curators
- Primary pains: Not knowing which channels to target, how to divide budget, or what to post about
- Uses Spotify for Artists for analytics; promotes primarily on Instagram and Facebook

### 1.4 Success Criteria (6 months post-launch)

The tool is a success if the artist:
1. Uses it actively for every new release (not abandoned after 2 songs)
2. Has all 10-30 catalog songs profiled with Spotify data + creative metadata
3. Consistently finds new, relevant Israeli promotion targets they hadn't discovered before
4. Receives and acts on specific budget allocation recommendations per release
5. Uses post opportunity suggestions to catch timely, relevant social moments
6. Has a clear record of every pitch submitted — no more guessing "did I already contact them?"
7. Can review past campaign performance to make smarter decisions on the next release

---

## 2. Background

### 2.1 The Israeli Music Landscape

**Mainstream Hebrew Pop Context:**
- **Primary radio targets:** Galei Tzahal (גלי צה"ל) — largest radio audience in Israel; mainstream pop/rock. More selective than indie stations but highest reach.
- **Secondary radio:** Kan Gimel (כאן גימל) — mainstream pop focus; Reshet Gimmel (רשת גימל) — classic/pop crossover.
- **Spotify playlists:** "Top 50 Israel" (76.8K followers), "Israeli Hits 2025" (14.6K followers), and dozens of Hebrew-language mainstream and pop-specific curator playlists.
- **SubmitHub:** Active ecosystem of playlist curators covering mainstream Hebrew pop; $1-3 per submission, 70% response rate vs ~5-10% for cold outreach.
- **Language dynamic:** Mainstream Hebrew pop primarily targets Hebrew-language playlists and Israeli radio. English-language crossover is secondary for this genre.
- **Festival exposure:** Jacubob Festival, Piano Festival, and mainstream Israeli live venues.

**Key artist insight from research:**
> Artists who submit to genre-matched playlists (not mass-submit) see 3-5x higher acceptance rates and better algorithmic placement.

### 2.2 Current Promotion Workflow (Without This Tool)

Today's manual process:
1. Release song on Spotify
2. Search Google / Instagram / friends for relevant playlists → inconsistent results
3. Cold email or DM curators → no template, no tracking
4. Submit to SubmitHub manually → no record of which curators were targeted
5. Post social content → written from scratch each time
6. Check Spotify for Artists weekly → no context for what the numbers mean
7. Campaign budget tracked in phone notes → no ROI awareness

**Time cost estimate:** 4-8 hours per song release in promotion-related admin work.
**Target with this tool:** <1.5 hours per song release.

### 2.3 Competitive Landscape

| Tool | Strength | Gap for This Use Case |
|------|----------|----------------------|
| Spotify for Artists | Official streaming data | No promotion targeting; no Israeli-specific guidance |
| SubmitHub.com | Curator submissions | No song profiling; no Hebrew content; no budget tracking |
| Groover | Playlist pitching | Not Israel-focused; expensive |
| Notion/Spreadsheet | Custom tracking | No automation; no AI; no Spotify integration |
| **This tool** | **All of the above, Israeli-focused, personal** | — |

---

## 3. Product Vision

### 3.1 Core Philosophy

**"From Data to Strategy to Action"**

Every feature must answer one of four questions:
1. **Where should I promote this song?** (Components 1, 2, 3)
2. **How should I promote it — and how should I spend my budget?** (Component 4)
3. **How is my promotion performing?** (Component 5)
4. **What social opportunities am I missing right now?** (Component 6)

The tool is a **strategic advisor**, not an executor. In MVP, the artist approves every recommendation and acts manually. Automation is the Phase 2+ direction.

### 3.2 Business Goals

This is a personal tool with no monetization goals. The "business" objective is:
- Reduce time spent on promotion admin by 70%+
- Increase promotion coverage (more relevant targets reached per song)
- Build institutional knowledge (past campaigns inform future ones)
- Make promotion feel systematic, not chaotic

### 3.3 User Goals

| Goal | Current State | Target State |
|------|--------------|--------------|
| Find promotion targets | Google + guesswork, 1-2 hours/song | Curated matches in <10 minutes |
| Know *how* to promote | Gut feeling, inconsistent | AI-generated strategy: channel priority, approach, timing per release type |
| Decide budget split | Arbitrary or skipped | AI recommendation per song + release type with rationale |
| Track pitches | Memory or scattered notes | Full log with status per submission |
| Spot social opportunities | Miss timely moments, write from scratch | AI surfaces 3-5 relevant post angles per week based on release + events |
| Understand analytics | Raw numbers, no context | Insights with recommended actions |
| Manage campaign spend | Phone notes, no ROI | AI-recommended split → manual execution → performance review |

### 3.4 Technical Goals

- **Reliability:** Works every day without babysitting. No crashes during release week.
- **Speed:** Dashboard and song list load in <2 seconds.
- **Hebrew accuracy:** Generated content reads like authentic Israeli social posts, not translated English.
- **Data integrity:** No lost pitch records, no duplicate entries.
- **Maintainability:** Personal tool that can be modified without major refactoring.

### 3.5 Non-Goals (MVP 1)

The following are explicitly out of scope:

- **No multi-user support** — authentication exists for security but no teams/sharing
- **No mobile app** — responsive web only
- **No AI audio analysis** — song profiling is manual + Spotify API (Phase 2)
- **No SubmitHub API** — campaign workflow is manual entry + tracking (Phase 2 if API available)
- **No automated ad spend** — budget recommendations are advisory; execution is manual (Phase 2+)
- **No Meta/Google Ads API import** — expenses logged manually
- **No social post caption writing** — the tool suggests *what to post about*, not the post text itself
- **No image/video generation** — text-based suggestions only
- **No i18n / Hebrew UI** — English interface throughout
- **No email/notification system** — in-app only
- **No public-facing pages** — purely internal tool

---

## 4. User Stories

### Priority 1 — Must Have (MVP 1)

#### Song Management

**US-001: Add a song via Spotify link**
```
As an artist,
I want to paste a Spotify track URL and have the app auto-fill song metadata,
So that I don't have to manually enter tempo, key, energy, and other technical data.

Acceptance Criteria:
- [ ] Paste Spotify URL → fetch title, duration, release date, audio features (tempo, key, energy, valence, danceability, acousticness)
- [ ] Album artwork displayed
- [ ] ISRC stored if available
- [ ] Fallback manual entry if Spotify link not provided
- [ ] Load time < 5 seconds
```

**US-002: Complete a song's creative profile**
```
As an artist,
I want to fill in the creative details about my song (mood, story, comparable artists),
So that the tool can make accurate promotion recommendations.

Acceptance Criteria:
- [ ] Fields: primary genre, secondary genres, language, mood tags (3-5), lyrical themes, vocal style, production style
- [ ] Story behind the song (200+ words, with word count indicator)
- [ ] Comparable artists field (3-5 names)
- [ ] "Golden minute" timestamp (optional)
- [ ] Radio targets: Galei Tzahal, Kan 88, others (checkboxes)
- [ ] Festival tags
- [ ] Save as draft
- [ ] "Duplicate from last song" to copy previous profile
```

**US-003: View my full song library**
```
As an artist,
I want to see all my songs in a list with quick stats,
So that I can manage my catalog efficiently.

Acceptance Criteria:
- [ ] List view with song title, release date, stream count, health indicator
- [ ] Sort by release date, streams, or health score
- [ ] Quick filter by genre, language, campaign status
- [ ] Click to open full song profile
```

#### Promotion Discovery

**US-004: Find relevant playlists for a song**
```
As an artist,
I want to see a list of Israeli Spotify playlists that match my song's genre, mood, and language,
So that I know exactly where to pitch instead of guessing.

Acceptance Criteria:
- [ ] Auto-filter playlists based on song's genre, mood tags, and language
- [ ] Show: playlist name, follower count, curator, submission method (email/Spotify for Artists/SubmitHub)
- [ ] Match score shown (why this playlist fits)
- [ ] Include mainstream Hebrew pop playlists prominently (not just indie)
- [ ] Filter by follower count range (500-10K, 10K-50K, 50K+)
- [ ] "Mark as Pitched" button per playlist
- [ ] "Already pitched" badge if previously submitted
```

**US-005: Find radio contacts**
```
As an artist,
I want to see Israeli radio stations that fit my genre with submission instructions,
So that I can pitch to the right stations without researching contact info each time.

Acceptance Criteria:
- [ ] Galei Tzahal listed with submission guidelines and contact
- [ ] Kan Gimel / other mainstream stations included
- [ ] Submission tips per station (what they look for, response time)
- [ ] "Mark as Contacted" per station
```

**US-006: Track all pitches for a song**
```
As an artist,
I want to log every pitch I make (playlist, radio, SubmitHub) and track results,
So that I never forget who I contacted or whether they responded.

Acceptance Criteria:
- [ ] Log a pitch: target name, date, method (email/DM/Spotify/SubmitHub), status
- [ ] Status options: Sent, Responded, Added, Rejected, No Response
- [ ] Add response notes (copy curator feedback)
- [ ] See pitch history per song with timeline
- [ ] Summary stats: X pitched, Y responded, Z added
```

#### Campaign & Budget

**US-007: Create a promotion campaign**
```
As an artist,
I want to create a campaign for a song, EP, or album with a timeline and budget,
So that my promotion efforts are organized under a single structure I can track.

Acceptance Criteria:
- [ ] Campaign name, start/end dates, total budget
- [ ] Release type: single / EP / album (affects strategy suggestions)
- [ ] Attach one or more songs (for EP/album: multiple songs, ordered)
- [ ] Campaign phases auto-calculated: Pre-Release, Launch Week, Post-Release
- [ ] Primary goal selectable: build awareness / grow fanbase / monetize
```

**US-008: Get AI budget allocation recommendation**
```
As an artist,
I want the tool to recommend how to split my campaign budget across channels,
So that I have a clear, justified spending plan before I start promoting.

Acceptance Criteria:
- [ ] After entering total budget and release type, tool generates recommended split:
      e.g., "Playlist pitching 55% ($110), SubmitHub 25% ($50), Social ads 15% ($30), Content 5% ($10)"
- [ ] Each allocation includes rationale: "Playlist pitching gives best ROI at your listener tier"
- [ ] Recommendation adjusts by: release type (single vs EP), artist listener tier, primary goal
- [ ] Artist can accept or manually adjust the split
- [ ] Recommended split stored as the campaign's "planned allocation"
- [ ] Phase 2+: tool can execute on this allocation automatically
```

**US-009: Log and track actual expenses**
```
As an artist,
I want to manually log each promotion expense after I spend it,
So that I can compare actual spend to the AI-recommended plan and stay on budget.

Acceptance Criteria:
- [ ] Add expense: date, amount, category, subcategory, optional description
- [ ] Actual vs planned spend shown per channel (e.g., "Playlist: $80 actual vs $110 planned")
- [ ] Budget remaining shown prominently
- [ ] Alert at 80% budget consumed
- [ ] Alert if a channel is significantly over or under its planned allocation
- [ ] Expense history list per campaign
```

**US-010: View campaign ROI and channel performance**
```
As an artist,
I want to see cost-per-stream and channel performance breakdowns,
So that I know which channels worked and can make smarter budget decisions next time.

Acceptance Criteria:
- [ ] Cost per stream by channel
- [ ] Channel leaderboard (best to worst ROI)
- [ ] Actual allocation vs AI-recommended allocation side-by-side
- [ ] Comparison to industry benchmarks ($0.01-0.05/stream)
- [ ] "Apply learnings to next campaign" button pre-fills future recommendation with adjusted weights
```

#### Dashboard & Insights

**US-011: View my music health at a glance**
```
As an artist,
I want a single dashboard showing all key metrics with a simple health score,
So that I can understand my overall performance in under 60 seconds.

Acceptance Criteria:
- [ ] Health score (0-100) prominently displayed with color coding
- [ ] Key metrics: streams (28-day), monthly listeners, followers, save rate, playlist adds
- [ ] Week-over-week trends (↑/↓ with percentage)
- [ ] Active campaign status
- [ ] Top 3 recommended actions
```

**US-012: Receive actionable insights**
```
As an artist,
I want to see AI-generated insight cards that explain what my data means and what to do,
So that I act on data instead of just staring at numbers.

Acceptance Criteria:
- [ ] Insight types: Momentum Alert (new playlist add), Performance Warning (stream drop), Opportunity (geo hotspot), Optimization Tip (low save rate)
- [ ] Each insight has: title, explanation, specific recommended action
- [ ] Dismiss or mark as actioned
- [ ] High-priority insights surfaced first
```

**US-013: Sync Spotify data**
```
As an artist,
I want to manually sync my Spotify analytics data,
So that my dashboard reflects current performance.

Acceptance Criteria:
- [ ] "Sync Spotify Data" button on dashboard
- [ ] Manual input form for: streams, monthly listeners, followers, saves (copy from Spotify for Artists)
- [ ] Data stored with timestamp
- [ ] Historical data preserved for trend analysis
```

#### Social Content Opportunity Engine

**US-014: Get post opportunity suggestions based on my release and current events**
```
As an artist,
I want the tool to surface 3-5 timely, relevant angles I could post about right now,
So that I never miss a good social moment and always have a clear starting point.

Acceptance Criteria:
- [ ] Tool generates a list of post opportunity cards, each containing:
      - Post angle / hook (what to write about, in 1-2 sentences)
      - Why it's relevant now (release milestone, current event, date, audience insight)
      - Suggested platform (Instagram / Facebook / TikTok)
      - Relevant hashtag suggestions (Hebrew + English mix)
      - Optional: suggested timing ("post before Friday evening")
- [ ] Opportunities sourced from multiple signal types:
      - Release milestones: "Your song hit 5K streams — thank your fans"
      - Campaign events: "You were added to a playlist — share the news"
      - Date-based: Israeli holidays, music awareness days, anniversary of release
      - Dashboard trends: "Your save rate jumped 3% this week — mention it"
      - Artist actions: "You haven't posted in 10 days — here are 3 ideas"
- [ ] Each opportunity has a "Use This" button that opens a blank draft with the angle pre-filled as a note (artist writes the actual post)
- [ ] Dismiss individual suggestions
- [ ] Refresh to generate new set
```

**US-015: See opportunity history and what worked**
```
As an artist,
I want to track which post opportunities I used,
So that I can see which types of content hooks I tend to act on.

Acceptance Criteria:
- [ ] Log of past opportunities: shown, dismissed, or used
- [ ] No engagement tracking (that's Instagram's job) — just capture what was actioned
- [ ] Simple tally: X opportunities generated, Y used this month
```

### Priority 2 — Should Have (Phase 2)

- **US-101:** AI audio analysis integration (SONOTELLER/Cyanite) to pre-fill mood/genre/story
- **US-102:** Spotify for Artists API auto-sync (instead of manual input)
- **US-103:** Automated budget execution: connect Meta/Google Ads API to deploy approved budget split automatically
- **US-104:** Geographic insights map (heatmap of top listening cities)
- **US-105:** Weekly narrative recap (auto-generated "your week in music" summary)
- **US-106:** SubmitHub API integration (if/when available) for automated submission
- **US-107:** Israeli current events feed integration to make opportunity suggestions more timely and culturally specific
- **US-108:** Hebrew transliteration helper for song titles
- **US-109:** EP/album-specific campaign templates (pre-built multi-week rollout strategies)

### Priority 3 — Nice to Have (Future)

- **US-201:** Export pitch history to PDF or CSV
- **US-202:** Reminder system for follow-up pitches (email to self)
- **US-203:** Duplicate detection for playlists (flag if same curator submitted twice)
- **US-204:** "Best time to post" guidance based on Israeli social media patterns
- **US-205:** Shabbat-aware content scheduling warnings

---

## 5. Feature Requirements

### 5.1 Component 1: Smart Song Profile

**Functional Requirements:**
- Spotify API integration: fetch metadata from track URL (title, duration, release date, audio features)
- Manual creative entry: mood tags (from curated list), lyrical themes, vocal style, production style, story (200+ words), comparable artists
- Hebrew/English bilingual title support (`title_hebrew`, `title_english`)
- "Golden minute" timestamp entry (optional)
- Radio-ready flags: Galei Tzahal, Kan Gimel, Kan 88 (checkboxes)
- "Duplicate from last song" to carry over genre, production style, comparable artists
- Save as draft before completing profile

**Data stored per song:**
- Spotify metadata: tempo, key, mode, energy, valence, acousticness, danceability, instrumentalness, liveness, loudness, speechiness
- Creative metadata: all manual fields listed above
- AI fields: schema supports Phase 2 AI suggestions (stored but null in MVP)

**Success Metrics:**
- 85%+ of songs have complete profiles (story field populated)
- Profile completion time: <20 minutes per song
- 50%+ of second+ songs use "Duplicate from last song"

---

### 5.2 Component 2: Israeli Playlist & Radio Discovery

**Functional Requirements:**
- Curated database: 50-100 Israeli Spotify playlists seeded at launch
  - Emphasis on mainstream Hebrew pop playlists (not just indie)
  - Include: Top 50 Israel (76.8K), Israeli Hits (14.6K), plus curator playlists 500-50K followers
- Radio station database: Galei Tzahal (primary), Kan Gimel, Kan 88, online/university stations
- Auto-filter by song profile (genre, language, mood)
- Match score display with reason ("Why this fits")
- Submission method shown: email, Spotify for Artists, Instagram DM, SubmitHub
- Pitch tracking: "Mark Pitched" → logs submission date + method
- Status tracking: Pitched → Responded → Added / Rejected / No Response
- "Already pitched" badge prevents duplicates

**Playlist seed data priorities for mainstream Hebrew pop:**
- Large Hebrew-language playlists (Top 50 Israel, Israeli Hits, etc.)
- Galei Tzahal-adjacent curator playlists
- Pop/R&B Hebrew crossover playlists
- SubmitHub curators who accept Hebrew pop

**Success Metrics:**
- 50+ active playlists in database at launch
- Match accuracy: 80%+ of suggestions are relevant (self-assessed)
- Industry benchmark pitch success rate: 15-20% playlist acceptance

---

### 5.3 Component 3: SubmitHub Integration

**Functional Requirements:**
- Campaign planner: select relevant curators from SubmitHub based on song profile
- Cost calculator: 10 × $3 = $30, with premium credit option ($1 each if bulk)
- Submission brief generator: auto-fills song details into a formatted document ready to copy into SubmitHub
- Short pitch text generated from song profile (1-2 sentences, genre + mood + language)
- Result tracker: per-curator status (pending/approved/declined), feedback notes
- Budget integration: SubmitHub spend tracked as expense in Campaign component

**MVP Limitation:**
Submissions are made manually on submithub.com. The tool generates the brief and tracks results — no automated API submission.

**Success Metrics:**
- ROI target: $2-5 per playlist add
- Approval rate target: 15-25% of submissions
- 80%+ of declines have feedback recorded

---

### 5.4 Component 4: Campaign & Budget Management

**Functional Requirements:**

**Campaign Creation:**
- Name, start/end dates, total budget, release type (single / EP / album), attached songs, primary goal
- EP/album: ordered song list; campaign covers multi-week rollout
- Campaign phases auto-calculated: Pre-Release, Launch Week, Post-Release

**AI Budget Recommendation Engine (core feature):**
- On campaign creation, tool generates a specific, justified budget split across channels:
  - Playlist pitching (direct + SubmitHub)
  - Social media ads (Instagram / Facebook / TikTok)
  - Content creation
  - PR / blog outreach
  - Other
- Recommendation logic considers:
  - Total budget size (small budget → concentrate, don't spread thin)
  - Release type (album warrants longer pre-release window and PR spend; single → heavier playlist focus)
  - Artist listener tier (emerging vs developing → different channel weightings)
  - Past campaign performance (if previous campaigns logged: upweight channels with better historical ROI)
  - Israeli market context (playlist pitching delivers higher ROI than social ads for Hebrew pop at emerging tier)
- Each line item includes a plain-English rationale (e.g., "SubmitHub: $50 — best guaranteed response rate for your genre")
- Artist approves or edits each line before saving as "planned allocation"
- Planned allocation stored separately from actual spend for post-campaign comparison

**Expense Tracking:**
- Manual expense logging: date, amount, category, subcategory, optional description
- Actual vs planned spend shown per channel in real time
- Budget remaining shown prominently
- Alerts: 80% consumed; significantly over/under planned channel split

**ROI Review:**
- Cost per stream by channel
- Channel leaderboard (best → worst ROI)
- Actual allocation vs AI-recommended allocation side-by-side
- Industry benchmark comparison ($0.01–0.05/stream)
- "Apply learnings" carries channel performance weights into the next campaign's recommendation

**Phase 2+:**
- Connect to Meta/Google Ads API to deploy social ad budget automatically once artist approves the split
- SubmitHub API integration for automated submissions within budget

**Success Metrics:**
- Every campaign has an AI-generated budget recommendation reviewed before launch
- 85%+ of campaigns finish within 10% of total budget
- Cost per stream tracked per channel on all campaigns

---

### 5.5 Component 5: Dashboard & Insights Engine

**Functional Requirements:**

**Health Score (0-100):**
```
health_score = (
  streams_trend × 0.30 +
  save_rate      × 0.25 +
  follower_conv  × 0.20 +
  playlist_adds  × 0.15 +
  campaign_roi   × 0.10
)
```
Color-coded: 85-100 Excellent 🟢 | 70-84 Healthy 🟡 | 50-69 Needs Work 🟠 | 0-49 Critical 🔴

**Key Metrics (28-day view):**
- Total streams, monthly listeners, followers, save rate, playlist adds
- Week-over-week change for each

**Insight Cards:**
- Momentum Alert: new playlist add detected (manual or auto)
- Performance Warning: significant stream drop
- Opportunity: geographic hotspot (manually entered)
- Optimization Tip: save rate below 5%, follower conversion low
- Milestone celebration: hit 10K, 50K, 100K streams

**MVP Data Input:**
Manual sync: user copies key numbers from Spotify for Artists weekly. Form fields: streams (28-day), monthly listeners, followers, saves, playlist adds, top cities (optional).

**"Next Best Actions" panel:** Prioritized list of 3 recommended actions based on current state.

**Weekly "Your Week in Music" recap:** Auto-generated narrative summary using stored delta data.

**Success Metrics:**
- Dashboard visited at least weekly
- 40%+ of high-priority insights actioned within 7 days
- Health score improves over 30 days of active use

---

### 5.6 Component 6: Social Content Opportunity Engine

**Purpose:** The tool does *not* write posts for the artist. Instead, it surfaces timely, relevant post *angles* and *hooks* so the artist always has a clear idea of what to write about and why now is the right moment to post.

**Functional Requirements:**

**Opportunity Card Structure:**
Each suggestion is a card containing:
- **Hook:** What to write about (1-2 sentence angle/idea, not the actual post)
- **Why now:** The signal that makes this timely (release milestone, date, event, metric)
- **Suggested platform:** Instagram / Facebook / TikTok
- **Hashtag suggestions:** 4-8 relevant Hebrew + English hashtags relevant to the hook
- **Timing note:** e.g., "Post before Shabbat for higher reach" or "This week while the release is still fresh"

**Signal sources (what triggers opportunities):**
- **Release milestones:** Song hits 1K / 5K / 10K / 50K streams; added to a playlist; first week anniversary
- **Campaign events:** Playlist pitch accepted; SubmitHub approval; radio confirmation
- **Performance trends:** Save rate spike this week; sudden stream surge; new city emerging in listeners
- **Calendar & culture:** Israeli holidays (Independence Day, Memorial Day, etc.), music awareness days, day of the week patterns (avoid Shabbat)
- **Inactivity trigger:** No post in X days → "You haven't posted in 8 days. Here are 3 ideas"
- **Release proximity:** 7 days before release → teaser ideas; release day → announcement angles; 2 weeks post → follow-up hooks

**Post categories surfaced:**
1. Milestone / thank-you ("5,000 streams — here's what to say")
2. Behind the story ("your song was recorded in one take — write about that")
3. Release build-up (countdown, teaser, day-of)
4. Playlist / radio win ("you got added — your fans will want to know")
5. Engagement hook ("ask your audience something related to the song's theme")
6. Cultural moment tie-in ("Independence Day is coming — your song about [theme] fits")

**AI Model:** Claude Sonnet 4 (`claude-sonnet-4-20250514`)

**Cultural context baked into prompts:**
- Opportunities framed for Israeli mainstream audience
- Shabbat-aware timing suggestions
- Hebrew cultural calendar awareness (holidays, national events)
- Platform-appropriate suggestion style (TikTok hooks are shorter and trend-based; Facebook is more narrative)

**Interaction model:**
- Artist sees opportunity cards on dashboard and in a dedicated "Post Ideas" section
- "Use This" → opens a lightweight note with the hook pre-filled; artist writes the actual post
- "Dismiss" → removes that suggestion
- "Remind Later" → resurfaces in 3 days
- Refresh generates a new batch

**Phase 2:**
- Pull live Israeli trending topics and current events via news/social feed API
- More precise signal detection via Spotify for Artists API auto-sync

**Success Metrics:**
- 3-5 fresh opportunities shown per week
- 50%+ of weeks: artist uses at least one suggestion
- Subjective: artist feels they never miss a good posting moment

---

## 6. User Experience Requirements

### 6.1 Design Principles

1. **Efficiency above all:** This is a personal productivity tool used under time pressure (release week). Every workflow should be completable in <5 minutes.
2. **Familiar patterns:** Standard web app UI — no surprises. Forms, tables, cards. No learning curve.
3. **Hebrew content, English UI:** All interface text in English. All generated content properly formatted for Hebrew (RTL, correct fonts: Heebo/Rubik).
4. **Data-forward:** Numbers visible everywhere. Don't hide metrics behind extra clicks.
5. **Progressive disclosure:** Show the most important thing first. Advanced options available but not in the way.

### 6.2 Key User Flows

**Flow 1: New Release Setup**
1. Dashboard → "Add New Song" (or "New Campaign" for EP/album)
2. Paste Spotify URL → auto-fetch metadata
3. Fill creative profile (15-20 min first time, 5 min with "Duplicate from last song")
4. Create campaign → enter budget → review AI budget recommendation → approve/adjust
5. Go to Playlist Discovery → filter by song → find matches → log pitches
6. Generate SubmitHub campaign brief → submit manually → log in tracker
7. Check "Post Ideas" section → pick a release-week opportunity → write post

**Flow 2: Weekly Check-in (5-10 min)**
1. Open Dashboard → sync Spotify data (copy numbers from Spotify for Artists)
2. Review health score and insight cards
3. Check "Post Ideas" for timely opportunities this week
4. Update pitch statuses (any SubmitHub responses? Playlist adds?)
5. Log any expenses spent this week

**Flow 3: Post-Campaign Review**
1. Open completed campaign → view ROI leaderboard
2. Review actual spend vs AI-recommended split — what diverged?
3. Click "Apply learnings" → weights carry into next campaign
4. Note what worked in campaign notes for future reference

### 6.3 Navigation Structure

```
Top Navigation:
├── Dashboard          (home, health score, insights)
├── Songs              (library + add new)
├── Discover           (playlists + radio)
├── Campaigns          (create + manage + budget)
├── Content            (generate + library)
└── Settings           (Spotify connection, profile)
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
- Page load time: <2 seconds (dashboard, song list)
- Spotify API fetch: <5 seconds
- Claude content generation: <15 seconds (3 variants)
- Database queries: <200ms for all standard views

### 7.2 Security
- JWT authentication (single user, but protect data and API keys)
- HTTPS only (when deployed)
- API keys stored in environment variables, never in code
- Rate limiting on content generation (prevent runaway API costs)
- OWASP Top 10 awareness

### 7.3 Reliability
- Local PostgreSQL for development; cloud PostgreSQL for deployment
- Daily automated database backup
- Error logging to `/logs` directory
- Graceful error handling: Spotify API down → manual entry fallback; Claude API down → error message, don't crash

### 7.4 Scalability (Personal Tool Scope)
- Design for 1 user, up to 200 songs, 50 campaigns
- No concurrency requirements beyond single user
- Efficient AI token usage: cache generated content, don't regenerate unnecessarily

### 7.5 Stack
- **Backend:** Python 3.11+, FastAPI, PostgreSQL, SQLAlchemy, Alembic
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, TanStack Query
- **AI:** Anthropic Python SDK, Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- **External APIs:** Spotify Web API (track metadata + audio features)
- **Deployment:** TBD (Railway or Render preferred for simplicity)

---

## 8. Data Model Summary

### Core Tables

| Table | Purpose |
|-------|---------|
| `users` | Single user authentication |
| `songs` | Song catalog with Spotify + creative metadata |
| `playlists` | Curated Israeli playlist database |
| `radio_stations` | Radio station contacts + submission info |
| `pitch_submissions` | Every pitch made, with status + response |
| `campaigns` | Promotion campaigns with budget |
| `campaign_songs` | Many-to-many: campaigns ↔ songs |
| `expenses` | All promotion expenses, categorized |
| `campaign_performance` | Daily metric snapshots (manually synced) |
| `submithub_campaigns` | SubmitHub-specific campaign tracking |
| `submithub_submissions` | Per-curator results |
| `post_opportunities` | AI-generated post angles with signal source + status |
| `dashboard_snapshots` | Aggregated daily metrics + health score |
| `insights` | AI-generated insight cards |

Full schema in `TECH_SPEC.md`.

---

## 9. Success Metrics

### Personal Use KPIs (6-month targets)

| Metric | Target |
|--------|--------|
| Songs profiled | 80%+ of catalog (8-25 songs) |
| Pitches logged | Every submission recorded (100%) |
| Playlist acceptance rate | 15-20% (industry benchmark) |
| Time per new release admin | <1.5 hours (down from 4-8) |
| Budget recommendations used | Every campaign has an AI recommendation reviewed before launch |
| Post opportunities actioned | At least 1 per week used as a posting starting point |
| Dashboard visits | At least weekly |
| Campaign budget adherence | Actual spend within 10% of planned total |
| Cost per stream | At or below $0.10/stream |
| Health score | Maintained above 70 |
| "Apply learnings" usage | Used after every completed campaign |

---

## 10. Roadmap

### MVP 1 (Weeks 1-6): Foundation + All 6 Components
**Goal:** Working tool covering the full release workflow.

| Week | Focus |
|------|-------|
| 1 | Project setup, DB, auth, Spotify API |
| 2 | Component 1: Song profile builder (+ EP/album support) |
| 3 | Component 2: Playlist discovery + pitch tracking |
| 4 | Component 3: SubmitHub planner + Component 4: Campaign/budget + AI recommendation engine |
| 5 | Component 5: Dashboard + insights + Component 6: Post opportunity engine |
| 6 | Polish, error handling, testing, playlist database seeding |

### Phase 2 (Weeks 7-12): AI Enhancement + Automation
- Spotify for Artists API auto-sync (replace manual data entry)
- AI audio analysis (SONOTELLER integration for song profiling)
- Automated budget execution: Meta/Google Ads API integration
- Israeli current events feed → richer post opportunity signals
- Geographic insights map
- Weekly narrative recap (auto-generated)
- EP/album multi-week rollout campaign templates

### Phase 3 (Months 4-6): Depth & Polish
- Mobile-responsive refinements
- Export features (PDF pitch history, CSV expenses)
- Reminder system for follow-up pitches
- Advanced analytics (song comparison, cross-campaign ROI)

---

## 11. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Spotify API rate limits | Medium | Medium | Cache all fetched data; don't re-fetch unnecessarily |
| Claude API cost spikes | Low | Low | Rate limit content generation; cache outputs |
| Playlist database goes stale | High | Medium | Manual update process; flag "last verified" date per entry |
| Tool abandoned after 2 songs | Medium | High | Keep MVP simple; prioritize the most painful features first (discovery + pitch tracking) |
| SubmitHub API unavailable (no API) | High | Low | MVP is manual workflow; not a blocker |
| Spotify for Artists data mismatch | Medium | Low | Manual sync is imprecise but acceptable for personal use |

---

## 12. Open Questions (To Resolve Before or During Build)

| Question | Options | Decision |
|----------|---------|---------|
| Deployment target | Railway / Render / local-only | TBD — local-only acceptable for MVP |
| Spotify OAuth scope | Read-only track data vs full access | Read-only sufficient for MVP |
| Hebrew font hosting | Google Fonts (Heebo) / self-hosted | Google Fonts (simpler) |
| Content generation rate limit | Per session / per day | 20 generations/day limit (prevent accidental cost) |
| Playlist database format | Seeded SQL / admin UI / CSV import | Seeded SQL migration for MVP |
| Backup strategy | Automated cron / manual | Manual pg_dump acceptable for personal use |

---

## 13. Appendix

### A. Audience Personas for Campaign Targeting

The component 4 docs reference target audience personas for campaign allocation. These are *your listeners* (not the tool's users):

| Persona | Description | Platform Focus |
|---------|-------------|---------------|
| Fellow Traveler | 25-40, Israeli, emotionally connected to Hebrew music | Instagram, Facebook |
| Nostalgic Explorer | 30-50, mainstream Israeli radio listener | Facebook, Galei Tzahal |
| Thoughtful Wanderer | 20-35, discovers music on Spotify playlists | Spotify editorial, SubmitHub |
| Melancholic Dreamer | 18-30, TikTok/Instagram Reels, viral content | TikTok, Instagram Reels |

### B. Israeli Playlist Seed List (Initial 10 priorities)

| Playlist | Followers | Type |
|----------|-----------|------|
| Top 50 Israel (official Spotify) | 76,800 | Editorial — no pitch |
| Israeli Hits 2025 | 14,600 | Curator — Eddie T Malakh |
| New Jewish Music | 3,700 | Curator |
| Israeli Indie (Sounds of Spotify) | 558 | Spotify-curated |
| +40 mainstream Hebrew pop curator playlists | varies | Research needed |

### C. Radio Contacts (Initial)

| Station | Genre Focus | Contact | Notes |
|---------|------------|---------|-------|
| Galei Tzahal (גלי צה"ל) | Mainstream pop/rock | IDF Radio submission form | Selective; largest audience |
| Kan Gimel (כאן גימל) | Mainstream pop | kan.org.il | More accessible than Galei Tzahal |
| Kan 88 (כאן 88) | Indie/alternative | 88music@kan.org.il | Best for indie; not primary target |

### D. AI Content Generation Cost Estimate

Using Claude Sonnet 4:
- ~2,000 tokens per generation (3 variants across 2 platforms)
- Cost: ~$0.006 per generation
- 20 generations/month = ~$0.12/month
- Even 200 generations/month = ~$1.20/month — negligible cost

---

**Document Status:** Draft v1.0
**Next Step:** Review and refine with user → then create `TECH_SPEC.md`

**Reviewed by:** [Your name]
**Date reviewed:** [Date]
**Approved:** [ ]
