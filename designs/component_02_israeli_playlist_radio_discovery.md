# Component Design: Israeli Playlist & Radio Discovery

## Document Version: 1.0
## Date: February 7, 2026
## Status: Ready for Review

---

## Executive Summary

**Purpose:** Help you discover and target relevant Israeli playlists (Spotify) and radio stations (88FM, Galei Tzahal) for song promotion.

**MVP Approach:**
- **Manual curated database** of Israeli playlists and radio contacts
- Search/filter based on song profile (genre, mood, language)
- Display with contact information
- Track which playlists/stations you've pitched to

**Phase 2 Enhancement:**
- Spotify API playlist search
- Automated matching algorithm
- Real-time playlist follower counts
- Contact information scraping/updates

**MVP Deliverable:** Curated database of 50-100 Israeli playlists + radio station contacts with search and filtering capabilities.

---

## Research: Best Practices

### Finding #1: Playlist Targeting is Genre-Specific
**Source:** Indie artist success stories + SubmitHub data

**Key Insights:**
- **Small-to-medium playlists (500-50K followers) have highest acceptance rates** for indie artists
- Large playlists (100K+) are Editorial or algorithm-driven (can't pitch directly)
- Israeli market has strong **curator playlists** (individuals curating by taste)
- **Language matters**: Hebrew-language playlists are separate ecosystem from English

**Implementation:**
- Focus on 500-50K follower range
- Separate Hebrew vs English/International playlists
- Tag by subgenre (indie rock, alternative, acoustic, etc.)

### Finding #2: Israeli Radio Station Landscape
**Source:** Israeli music industry research

**Key Stations for Indie/Alternative:**
- **Kan 88 (כאן 88)** - Main indie/alternative station
  - Contact: 88music@kan.org.il
  - Focus: Alternative, indie, rock, world music, jazz
  - New artist friendly
  - National reach (10.8% exposure)

- **Galei Tzahal (גלי צה"ל)** - IDF radio, mainstream
  - More selective, requires established presence
  - Mainstream pop/rock
  - Largest audience in Israel

- **Regional/Online Stations:**
  - Indie-focused web radio
  - University stations
  - Community radio

**Implementation:**
- 88FM as primary target for indie artists
- Galei Tzahal as secondary (requires more momentum)
- Include submission guidelines and contact methods

### Finding #3: Playlist Curator Communication
**Source:** Successful playlist pitching strategies

**What Works:**
- **Personal, specific emails** (not mass submissions)
- **Mention why your song fits THEIR playlist** (research their taste)
- **Keep it short** (3-4 paragraphs max)
- **Include story context** (why you wrote the song)
- **Hebrew communication** for Israeli curators (English for international)

**What Doesn't Work:**
- Generic "check out my music" emails
- Long essays about your career
- Aggressive follow-ups
- Pitching wrong genre to playlist

---

## Feature Specifications - MVP

### Core Features

**1. Curated Playlist Database**
```
Playlist Entry Structure:
{
  name: "The Sound of Israeli Indie",
  spotify_id: "0lKD2vCUwtVhp7wLhJoyWe",
  curator: "The Sounds of Spotify",
  follower_count: 558,
  last_updated: "2025-01-15",
  genres: ["indie", "alternative", "rock"],
  languages: ["hebrew", "english"],
  mood_tags: ["introspective", "melancholic", "energetic"],
  submission_method: "spotify_for_artists", // or "email", "instagram_dm"
  curator_contact: null, // If indie curator, email/IG handle
  notes: "Curated by Spotify, editorial playlist"
}
```

**Initial Seed Data (50-100 playlists):**
- Top 50 Israel (official Spotify): 76.8K followers
- Israeli Indie (Sounds of Spotify): 558 followers
- Israeli Hits 2025: 14.6K followers
- New Jewish Music: 3.7K followers
- Plus 50-80 smaller indie curator playlists

**2. Radio Station Database**
```
Station Entry:
{
  name: "Kan 88 (כאן 88)",
  type: "national_radio",
  focus: ["alternative", "indie", "rock", "world", "jazz"],
  contact_email: "88music@kan.org.il",
  phone: "076-8098000",
  website: "https://www.kan.org.il/radio/program.aspx/?progId=93",
  submission_guidelines: "Email with song link, bio, and story. They review weekly.",
  best_for: ["indie", "alternative", "acoustic"],
  reach: "National - 10.8% exposure",
  notes: "New artist friendly. Focus on quality, not fame."
}
```

**Initial Seed Data:**
- Kan 88 (main target)
- Galei Tzahal
- 5-10 regional/online stations

### User Flow

**Search & Filter Interface:**

```
┌─────────────────────────────────────────────────────┐
│ Find Playlists & Radio for "Lev Kavu'a"             │
├─────────────────────────────────────────────────────┤
│                                                      │
│ [Auto-filled based on song profile]                 │
│                                                      │
│ Filters:                                             │
│ ├─ Genre: Indie Rock, Alternative, Acoustic         │
│ ├─ Language: Hebrew                                 │
│ ├─ Mood: Melancholic, Introspective                │
│ └─ Target: ○ Playlists  ○ Radio  ● Both            │
│                                                      │
│ Playlist Size:                                       │
│ ● 500-10K  ○ 10K-50K  ○ 50K+  ○ All               │
│                                                      │
│ [Search]                                            │
│                                                      │
└─────────────────────────────────────────────────────┘

Results: 23 playlists, 2 radio stations

┌─────────────────────────────────────────────────────┐
│ PLAYLISTS                                            │
├─────────────────────────────────────────────────────┤
│                                                      │
│ ✅ Match: 95% - The Sound of Israeli Indie          │
│ 👥 558 followers | Curator: The Sounds of Spotify   │
│ 🎵 Indie, Alternative, Rock | 🇮🇱 Hebrew & English  │
│                                                      │
│ Why it fits: Your song matches the melancholic      │
│ indie rock vibe of this playlist.                   │
│                                                      │
│ 📋 Submission: Via Spotify for Artists dashboard    │
│                                                      │
│ [View on Spotify] [Generate Pitch] [Mark Pitched]  │
│                                                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│ ✅ Match: 88% - Israeli Indie Hits 2025             │
│ 👥 14.6K followers | Curator: Eddie T Malakh        │
│ 🎵 Pop, Indie, Alternative | 🇮🇱 Hebrew             │
│                                                      │
│ Why it fits: Larger Hebrew-language playlist        │
│ featuring indie artists.                            │
│                                                      │
│ 📧 Contact: [Requires research - no public email]   │
│                                                      │
│ [View on Spotify] [Research Contact] [Mark Pitched]│
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ RADIO STATIONS                                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│ ⭐ RECOMMENDED: Kan 88 (כאן 88)                     │
│ 📻 National Radio | 🎵 Alternative, Indie, Rock     │
│ 📊 Reach: 10.8% national exposure                   │
│                                                      │
│ Perfect for: New indie/alternative artists          │
│                                                      │
│ 📧 Email: 88music@kan.org.il                        │
│ 📞 Phone: 076-8098000                               │
│ 🌐 Website: kan.org.il/radio                        │
│                                                      │
│ Submission Tips:                                     │
│ • Send email with Spotify link + short bio          │
│ • Include story behind the song (Hebrew)            │
│ • They review submissions weekly                    │
│ • Response time: 1-2 weeks typically                │
│                                                      │
│ [Generate Email Pitch] [Mark as Contacted]         │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Pitch Tracking

```
┌─────────────────────────────────────────────────────┐
│ Pitch Tracker for "Lev Kavu'a"                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Status Overview:                                     │
│ ├─ Pitched: 12 playlists, 1 radio station           │
│ ├─ Responses: 3                                     │
│ ├─ Added: 1 🎉                                      │
│ └─ Rejected: 1                                      │
│                                                      │
│ Recent Activity:                                     │
│ ├─ Jan 15: Added to "The Sound of Israeli Indie" ✅ │
│ ├─ Jan 12: No response from "Israeli Hits 2025"     │
│ └─ Jan 10: Pitched to Kan 88 - awaiting response    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Data Model

```sql
-- Playlists Database
CREATE TABLE playlists (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    spotify_id VARCHAR(255) UNIQUE,
    curator_name VARCHAR(255),
    curator_contact VARCHAR(255), -- email or IG handle
    follower_count INTEGER,
    last_updated DATE,
    
    -- Matching criteria
    genres TEXT[] NOT NULL,
    languages TEXT[] NOT NULL,
    mood_tags TEXT[],
    
    -- Submission info
    submission_method VARCHAR(50), -- 'spotify_for_artists', 'email', 'instagram_dm'
    submission_guidelines TEXT,
    
    -- Metadata
    is_active BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Radio Stations
CREATE TABLE radio_stations (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    name_hebrew VARCHAR(255),
    type VARCHAR(50), -- 'national', 'regional', 'online', 'university'
    
    -- Contact
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    website VARCHAR(255),
    
    -- Focus
    genres_focus TEXT[] NOT NULL,
    best_for TEXT[],
    
    -- Submission
    submission_guidelines TEXT NOT NULL,
    response_time VARCHAR(100),
    
    -- Stats
    reach_description VARCHAR(255),
    
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Pitch Tracking
CREATE TABLE pitch_submissions (
    id UUID PRIMARY KEY,
    song_id UUID REFERENCES songs(id),
    campaign_id UUID REFERENCES campaigns(id),
    
    target_type VARCHAR(20), -- 'playlist' or 'radio'
    target_id UUID, -- References playlists(id) or radio_stations(id)
    
    pitched_date TIMESTAMP NOT NULL,
    pitch_method VARCHAR(50), -- 'email', 'spotify', 'instagram_dm'
    pitch_email_sent TEXT, -- Copy of email sent
    
    status VARCHAR(50) DEFAULT 'sent', -- 'sent', 'opened', 'responded', 'added', 'rejected', 'no_response'
    response_date TIMESTAMP,
    response_notes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Technical Implementation

### Phase 1: Manual Curated Database (Weeks 1-2)

**Week 1: Research & Data Collection**
- Manual research of Israeli Spotify playlists
- Identify curator contact information (where available)
- Compile radio station details
- Build initial seed data (CSV → Database)

**Week 2: UI Development**
- Search/filter interface
- Playlist/radio detail pages
- Pitch tracking system

### Phase 2: Automated Enhancement (Future)

**Spotify API Integration:**
```python
# Search for playlists based on song profile
def search_spotify_playlists(genres, language, mood_tags):
    # Use Spotify search API
    # Query: "genre:indie mood:melancholic language:hebrew"
    pass

# Get playlist details
def fetch_playlist_details(playlist_id):
    # Get follower count, curator, tracks
    pass
```

---

## Success Metrics

**Metric 1: Database Quality**
- Target: 50+ Israeli playlists, 5+ radio stations in MVP
- Measurement: Count active entries
- Success: Covers major indie/alternative landscape

**Metric 2: Match Accuracy**
- Target: 80%+ of suggestions are relevant
- Measurement: User feedback on matches
- Success: Users find appropriate targets

**Metric 3: Pitch Success Rate**
- Target: 15-20% playlist acceptance rate
- Measurement: Track added/rejected status
- Success: Comparable to industry benchmarks

---

## Questions for Review

1. ✅ **MVP scope reasonable?** 50-100 manually curated playlists + radio contacts?
2. ✅ **Should we include submission cost tracking?** (Some playlists use paid services)
3. ✅ **Include playlist "quality score"?** (Follower growth rate, curator engagement)
4. ✅ **Hebrew-only interface for radio contacts?** Or bilingual?

Ready for Component 3: SubmitHub Integration! 🎸
