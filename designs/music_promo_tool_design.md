# Music Promotion Tool - Complete Design Document

*A comprehensive design for an AI-powered music promotion platform*

---

## Quick Reference

**What:** Web app to help you promote your music strategically  
**Who:** You (35-year-old musician, ML engineer, limited marketing time)  
**Budget:** $100-300/month per campaign  
**Philosophy:** Semi-automated, you approve everything  
**Timeline:** MVP in 6-8 weeks

---

## The Problem You're Solving

You create beautiful music but marketing feels overwhelming:
- ❌ Currently just upload to DistroKid + post Facebook link
- ❌ Don't know which playlists to pitch to
- ❌ Don't know how to run effective ads
- ❌ Can't track what's actually working
- ❌ Limited time (you have a full-time job)

## The Solution

A tool that:
- ✅ Finds relevant playlists and writes pitch emails
- ✅ Generates social media content tailored to your brand personas
- ✅ Plans ad campaigns (you execute them)
- ✅ Tracks everything in one dashboard
- ✅ Gives you actionable insights: "do more of X, stop doing Y"

---

# Part 1: What We're Building

## Core Features (MVP)

### 1. Campaign Manager
Create campaigns around song releases. One campaign can include multiple songs.

**Example Campaign:**
- Name: "Winter EP Release"
- Budget: $250 total
- Duration: December 1-31
- Songs: "Frozen Heart", "December Blues", "New Year"
- Target Personas: Fellow Traveler (50%), Nostalgic Explorer (30%), Heartbreak Seeker (20%)

### 2. Smart Song Profiles
Combine Spotify API data + your input to create rich profiles.

**Automatic (from Spotify):**
- Audio features: tempo, key, energy, acousticness, etc.
- Metadata: title, duration, release date

**Manual (you provide):**
- Story behind the song (200-500 words)
- Mood tags (melancholic, introspective, etc.)
- Themes (heartbreak, philosophy, joy)
- Comparable artists
- Production style

**Why it matters:** This data powers playlist matching, content generation, and ad targeting.

### 3. Budget Tracker
Track where money goes across channels:
- Meta Ads
- Google Ads  
- Playlist pitch services (SubmitHub, Playlist Push)
- Content boosting

Get alerts when you're overspending or underspending relative to timeline.

### 4. Unified Dashboard
See everything in one place:
- Total streams, saves, playlist adds
- Spending by channel
- Cost per stream by channel
- Song-by-song comparison
- Actionable recommendations

### 5. Playlist Finder
Input: Your song profile  
Output: List of 20-30 relevant indie playlists with:
- Match score (how well your song fits)
- Curator contact info
- Playlist size and recent activity
- Similar artists already on the playlist

### 6. Pitch Generator
Auto-generates personalized playlist pitch emails using:
- Song story
- Curator's playlist vibe
- Your comparable artists
- Authentic, non-spammy tone

You review and edit before sending.

### 7. Content Factory
Generate 10-15 content variations per song:
- Instagram captions (short, medium, long)
- Facebook posts
- Email newsletter drafts
- Story templates with lyrics

Tailored to specific personas (Fellow Traveler vs Nostalgic Explorer content feels different).

### 8. Insights Engine
Analyzes your data and tells you:
- "Stop spending on Meta Ads for Song X - ROI is terrible"
- "Double down on playlist pitching - best cost per stream"
- "Frozen Heart is trending up - increase its budget"
- "Your acoustic content gets 2x more saves"
- "Budget pace is 20% ahead of schedule - reduce spend"

---

# Part 2: How It Works

## User Flow: New Release Campaign

**Step 1: Add Your Song**
1. Paste Spotify link
2. Tool fetches metadata automatically
3. You fill in story, mood, themes (5 minutes)

**Step 2: Create Campaign**
1. Name it ("Winter EP Release")
2. Set budget ($250) and dates (Dec 1-31)
3. Add songs to this campaign
4. Set persona allocation (Fellow Traveler 50%, etc.)

**Step 3: Find Playlists**
1. Click "Find Playlists" for your song
2. Tool analyzes song profile
3. Returns 24 curated indie playlists
4. You review match scores
5. Select 10-15 to pitch

**Step 4: Generate Pitches**
1. Click "Generate Pitch" for each playlist
2. Tool writes personalized email
3. You review/edit
4. Click "Send" (or save for later)

**Step 5: Create Content**
1. Select song + target persona
2. Tool generates Instagram posts, Stories, Facebook content, email draft
3. You pick favorites, maybe edit a caption
4. Use over next 2 weeks

**Step 6: Plan Ads (Manual execution)**
1. Tool analyzes your personas + song profile
2. Generates Meta Ads campaign plan:
   - Audience targeting recommendations
   - Ad copy variations
   - Budget allocation
   - Expected results
3. You copy the plan into Meta Ads Manager
4. Set up campaign yourself
5. Tool tracks results via API

**Step 7: Monitor Dashboard**
1. Check weekly (20 min)
2. See what's working, what's flopping
3. Read insights: "Do more X, stop Y"
4. Adjust budget allocation
5. Generate fresh content if needed

---

# Part 3: The Data Model

## Database Tables

### Users
```
id, email, artist_name, spotify_artist_id, created_at
```

### Campaigns
```
id, user_id, name, budget_total, budget_spent, 
start_date, end_date, status, created_at
```

### Campaign_Personas
```
id, campaign_id, persona_type (fellow_traveler, etc.), 
allocation_percentage (0-100)
```

### Songs
```
id, user_id, title, spotify_uri, isrc, release_date, duration_ms,

[Spotify Features]
tempo, key, mode, energy, valence, acousticness, danceability, ...

[Manual Inputs]
primary_genre, secondary_genres[], mood_tags[], lyrical_themes[],
story_behind_song (text), vocal_style[], production_style[],
comparable_artists (text), personal_notes (text)
```

### Campaign_Songs (many-to-many)
```
campaign_id, song_id
```

### Expenses
```
id, campaign_id, song_id, category (meta_ads, playlists, etc.),
amount, expense_date, description, source (manual vs API),
external_id
```

### Performance_Metrics (daily snapshots)
```
id, song_id, metric_date,
streams, saves, playlist_adds, listeners,
instagram_reach, instagram_engagement, ...
```

### Ad_Performance (daily snapshots)
```
id, campaign_id, song_id, platform (meta, google),
metric_date, spend, impressions, clicks, conversions
```

### Playlists
```
id, spotify_playlist_id, name, curator_name, curator_email,
follower_count, genres[], mood_tags[], last_updated
```

### Playlist_Pitches
```
id, song_id, playlist_id, campaign_id,
pitch_email_subject, pitch_email_body,
status (draft, sent, opened, responded, added, rejected),
sent_date, response_date, added_date
```

### Generated_Content
```
id, song_id, campaign_id, persona_type,
content_type (instagram_post, email, etc.),
content_format (text, image_template),
content_text, content_metadata (JSON),
status (generated, edited, scheduled, posted),
scheduled_date, posted_date
```

### Insights
```
id, campaign_id, song_id,
insight_type (budget_alert, performance_recommendation, etc.),
priority (high, medium, low),
title, description, recommendation,
status (active, dismissed, acted_upon)
```

---

# Part 4: APIs We'll Use

## 1. Spotify Web API
**What we get:**
- Track metadata (title, duration, ISRC)
- Audio features (tempo, key, energy, acousticness, etc.)
- Artist info

**When we use it:**
- When you add a song (paste Spotify link)
- One-time fetch per song (data is static)

**Rate limits:** Generous, no concerns

---

## 2. Meta Business API
**What we get:**
- Ad campaign performance (spend, impressions, clicks)
- Daily breakdown

**When we use it:**
- Daily automated polling (overnight)
- Stores in ad_performance table

**Setup required:**
- Meta Business Manager account
- Connect ad account to our app
- OAuth2 authentication

**Phase 1 (MVP):** Manual tracking  
**Phase 2:** Automated via API

---

## 3. Google Ads API
**What we get:**
- Campaign metrics (cost, impressions, clicks)

**When we use it:**
- Daily polling (Phase 2)

**Note:** Google Ads API is complex, likely defer to Phase 2

---

## 4. Anthropic API (Claude)
**What we use it for:**
- Generate playlist pitch emails
- Generate social media content
- Generate ad copy
- Analyze performance data → create insights

**Cost:**
- ~$0.005 per content generation
- Budget $20/month = ~4,000 generations (plenty)

**Implementation:**
```python
# Generate Instagram caption
client = anthropic.Client(api_key=key)
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{
        "role": "user",
        "content": f"Generate Instagram caption for {song_data}"
    }]
)
```

---

## 5. SendGrid (Email Service)
**What we use it for:**
- Sending playlist pitch emails
- Track open/click rates (optional)

**Free tier:** 100 emails/day (plenty for you)

---

# Part 5: The Recommendation Engine

This is the "brain" that analyzes your data and tells you what to do.

## Input Data
1. Song performance (streams, saves, playlists)
2. Ad performance (spend, clicks, conversions)
3. Budget data (what you spent where)
4. Song characteristics (genre, mood, acousticness, etc.)
5. Campaign configuration (personas, budget, timeline)

## Recommendation Types

### 1. Budget Alerts
**Triggers:**
- 80% of budget spent
- Spending 15%+ ahead of schedule
- Spending 20%+ behind schedule

**Example output:**
"⚠️ You've spent 72% of budget with 42% of campaign remaining. Reduce daily ad spend by 25% to stay on track."

### 2. Channel Performance
**Logic:**
- Calculate cost per stream for each channel
- Compare channels
- If one channel is 3x worse than best channel → recommend pausing it

**Example output:**
"🎯 STOP: Meta Ads cost $0.35/stream vs Playlist Adds at $0.12/stream. Pause Meta, reallocate $40 to playlists."

### 3. Song Comparisons
**Logic:**
- Compare songs in same campaign
- If Song A has 2x streams of Song B → recommend reallocating budget

**Example output:**
"💡 'Frozen Heart' outperforming 'New Year' by 2x. Shift $30 from 'New Year' to 'Frozen Heart' ads."

### 4. Content Recommendations
**Logic:**
- Analyze song characteristics vs performance
- If acoustic songs have higher save rates → recommend more acoustic content
- If certain persona over-performing → suggest more content for them

**Example output:**
"🎸 Songs with acousticness > 0.7 have 45% higher save rate. Create more stripped-down content."

### 5. Trend Predictions
**Logic:**
- Calculate streams trajectory (linear regression over last 7 days)
- Project to campaign end
- If gaining 50+ streams/day → recommend increasing budget

**Example output:**
"📈 'Frozen Heart' gaining 73 streams/day. Based on trajectory, you'll hit 8,500 total streams by Dec 31. Consider +$50 to capitalize on momentum."

---

# Part 6: Wireframes

## Dashboard View
```
╔════════════════════════════════════════╗
║  Dashboard              [Profile Menu] ║
╚════════════════════════════════════════╝

┌──────────────────────────────────────┐
│ ACTIVE CAMPAIGNS                      │
│                                       │
│ ┌──────────────────────────────────┐ │
│ │ Winter EP Release                │ │
│ │ $147 / $250 (59%)                │ │
│ │ 18 days remaining                │ │
│ │ [View Details]                   │ │
│ └──────────────────────────────────┘ │
│                                       │
│ [+ Create New Campaign]               │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ QUICK STATS                           │
│ Streams this month: 5,234  ↑28%      │
│ Budget spent: $147                    │
│ Cost/stream: $0.028                   │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ TOP INSIGHTS (4)                      │
│ 🎯 STOP Meta Ads for "New Year"      │
│ 💡 "Frozen Heart" trending up        │
│ [View All]                            │
└──────────────────────────────────────┘
```

## Campaign Detail View
```
╔════════════════════════════════════════╗
║  Winter EP Release         [Settings] ║
╚════════════════════════════════════════╝

[Overview] [Songs] [Expenses] [Content]
   ⎯⎯⎯

Budget: $250 | Spent: $147 | Remaining: $103
━━━━━━━━━━━━━━━━━━░░░░░░░░  59%

[Performance charts as shown in earlier design]
[Insights section]
```

---

# Part 7: Technical Stack

## Frontend
- **Framework:** Next.js 14 (React)
- **Styling:** Tailwind CSS
- **Charts:** Recharts
- **State:** React Query for server state
- **Deployment:** Vercel

## Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Auth:** NextAuth.js + JWT
- **Background Jobs:** Celery + Redis
- **Deployment:** Railway or Render

## File Structure
```
/frontend (Next.js)
├── /app
│   ├── /dashboard
│   ├── /campaigns
│   ├── /songs
│   └── /settings
├── /components
│   ├── /charts
│   ├── /forms
│   └── /ui
└── /lib
    └── api.ts

/backend (FastAPI)
├── /api
│   └── /routes
│       ├── campaigns.py
│       ├── songs.py
│       └── insights.py
├── /models
├── /services
│   ├── spotify_service.py
│   ├── anthropic_service.py
│   └── meta_service.py
├── /engine
│   └── recommendation_engine.py
└── /tasks
    └── poll_apis.py
```

---

# Part 8: Implementation Plan

## Phase 1: MVP (6-8 weeks)

**Weeks 1-2: Foundation**
- Set up Next.js + FastAPI projects
- Database schema + migrations
- Authentication (login/signup)
- Basic navigation/routing

**Weeks 3-4: Core Features**
- Song profile builder (Spotify API integration)
- Campaign creation/management
- Manual budget tracking (expense entry form)
- Basic dashboard (show budget, song list)

**Weeks 5-6: Playlist & Content**
- Playlist discovery algorithm
- Playlist pitch generator (Anthropic API)
- Content generator (Instagram/Facebook posts)
- Pitch tracking

**Weeks 7-8: Insights & Polish**
- Basic recommendation engine (budget alerts, simple insights)
- Dashboard improvements (charts, better UX)
- Testing & bug fixes
- Deploy to production

**MVP Deliverables:**
✅ You can create campaigns, add songs, track budget  
✅ Find playlists and generate pitch emails  
✅ Generate social content  
✅ See basic insights on dashboard  

---

## Phase 2: Automation (4-6 weeks after MVP)

**Auto API Polling:**
- Connect Meta Ads API
- Connect Google Ads API  
- Daily background jobs to pull data
- No more manual expense entry for ads

**Enhanced Insights:**
- All recommendation algorithms implemented
- Comparative analytics (song vs song)
- Trend predictions
- Persona performance tracking

**Content Scheduling:**
- Schedule posts for future dates
- Calendar view of planned content

**Email Automation:**
- Automated playlist pitch sending
- Track email opens/responses

---

## Phase 3: Advanced (Future)

**Direct Ad Management:**
- Tool creates Meta/Google campaigns for you
- You just approve and launch

**A/B Testing:**
- Test multiple ad creatives
- Test caption variations
- Auto-select winners

**More Integrations:**
- TikTok
- YouTube
- Influencer outreach platforms

**Mobile App:**
- React Native version
- Check dashboard on the go

---

# Part 9: Success Metrics

## For You (User Success)
- **Time saved:** 10+ hours/month on marketing
- **Cost efficiency:** 30%+ lower cost per stream vs manual approach
- **Clarity:** Always know what's working, what's not
- **Confidence:** Feel in control of your promotion

## For The Tool (Product Success)
- **User retention:** You use it every week
- **Feature adoption:** You use 5+ features regularly
- **ROI:** Tool demonstrably improves your results
- **Feedback:** Continuous improvement based on your needs

---

# Part 10: Next Steps

## Your Action Items
1. ✅ Review this design - does it solve your problem?
2. ✅ Prioritize features - anything to add/remove?
3. ✅ Get API access:
   - Spotify Developer account
   - Anthropic API key
   - Meta Business Manager (can wait for Phase 2)
4. ✅ Decide on hosting (Vercel + Railway recommended)

## My Action Items (Once Approved)
1. Set up project repos (Next.js + FastAPI)
2. Create database schema
3. Build MVP iteratively
4. You review PRs, I incorporate feedback
5. Write tests as we go

## Timeline
- **Design approval:** Now
- **Start development:** Immediately after approval
- **MVP completion:** 6-8 weeks
- **Your first campaign:** By mid-March 2025

---

# Questions for Discussion

1. **Dashboard priority:** What's the ONE metric you most want to see front and center?

2. **Content generation:** Should we start with just Instagram/Facebook, or add TikTok scripts to MVP?

3. **Playlist pitching:** Manual sending (you hit send) or fully automated with daily limits?

4. **Budget tracking:** Track by song or just by campaign overall?

5. **MVP scope:** Too much? Too little? Just right?

---

# Closing Thoughts

This tool is designed specifically for YOU:
- An ML engineer who thinks systematically
- A musician with limited marketing time
- Someone who values data-driven decisions
- A person willing to be vulnerable and authentic

It won't make you go viral overnight. It won't do your job for you.

But it WILL:
- Give you clarity on what's working
- Save you 10+ hours/month
- Help you spend your budget wisely
- Generate content that feels authentic
- Connect your music with the right people

Most importantly, it'll let you focus on what you do best: making music that matters.

Ready to build this? 🎸

