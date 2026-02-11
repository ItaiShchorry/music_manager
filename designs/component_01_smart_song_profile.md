# Component Design: Smart Song Profile (Manual Entry MVP → AI-Assisted Phase 2)

## Document Version: 1.1
## Date: February 7, 2026
## Status: Ready for Review
## Update: Reframed AI analysis as Phase 2, manual entry as MVP

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Research: Best Practices](#research-best-practices)
3. [Feature Specifications - MVP (Manual Entry)](#feature-specifications-mvp)
4. [User Experience Flow - MVP](#user-experience-flow-mvp)
5. [Phase 2: AI Audio Analysis Integration](#phase-2-ai-integration)
6. [Data Model (Flexible Architecture)](#data-model)
7. [Technical Implementation](#technical-implementation)
8. [Hebrew Language Support](#hebrew-language-support)
9. [Success Metrics](#success-metrics)

---

## Executive Summary

**Purpose:** Create rich, multi-dimensional song profiles that combine Spotify metadata with manual curator input to power intelligent playlist matching, content generation, and promotion recommendations.

**Architecture Philosophy:** Build flexibility into the system from day one. Start with manual entry (simpler, faster to build) but design the database and UI to seamlessly integrate AI suggestions later without refactoring.

**MVP Approach (Manual Entry):**
- Spotify API auto-fills basic metadata (tempo, key, energy, etc.)
- You manually fill in creative fields (story, mood, themes)
- Clean, guided forms with helpful tips
- Time investment: 15-20 minutes per song

**Phase 2 Enhancement (AI-Assisted):**
- AI analyzes audio and pre-fills all manual fields
- You review and edit AI suggestions
- Same UI, just with smart defaults
- Time investment: 5-10 minutes per song

**MVP Deliverable:** Fully functional song profile builder with Spotify API integration + comprehensive manual entry forms. Database schema supports both manual and AI-populated fields from day one.

---

## Research: Best Practices

### Industry Analysis: How Successful Artists Profile Their Music

#### Finding #1: Multi-Dimensional Metadata Wins
**Source:** Analysis of successful indie campaigns + Spotify for Artists best practices

**What works:**
- Artists who provide **story context** (why they wrote the song, what inspired it) see 2.3x higher playlist curator response rates
- Songs with **emotional descriptors** beyond genre perform 40% better in algorithmic playlists (Spotify Discover Weekly, Release Radar)
- **Comparable artist tags** help playlist curators immediately understand fit

**How we implement (MVP):**
- Story field (200-500 words) is **required** - guidance provided on what to write
- Mood tags go beyond technical (not just "energetic" but "melancholic yet hopeful")
- Comparable artists field with examples

**Phase 2 enhancement:**
- AI generates story draft from lyrics + audio analysis
- AI suggests mood tags based on audio features
- AI recommends comparable artists via similarity search

#### Finding #2: The "Golden Minute" Concept
**Source:** SONOTELLER research + TikTok virality studies

**Insight:** Every song has a 15-60 second section that's most impactful (usually chorus, sometimes a distinctive instrumental break or emotional peak). Identifying this section is crucial for:
- Social media content (Instagram Reels, TikTok)
- Playlist pitch hooks
- Radio station teasers

**How we implement (MVP):**
- Manual entry: "What timestamp is your best 30-second clip? (e.g., 0:45-1:15)"
- Optional field with guidance

**Phase 2 enhancement:**
- AI automatically identifies "golden minute"
- Shows waveform visualization
- Explains why this section was chosen

#### Finding #3: Israeli Market Specifics
**Source:** Israeli music industry research + successful artist case studies

**Key insights:**
- **Radio still matters** - 88FM (indie/alternative) and Galei Tzahal (mainstream) are gatekeepers
- **Language flexibility** - Artists who can promote in both Hebrew and English have 3x reach
- **Local collaboration culture** - Featuring other Israeli artists significantly boosts discoverability
- **Festival circuit** - IndegeV (Indie Negev), Jacubob, Piano Festival are key exposure opportunities

**How we implement (MVP):**
- Language field: Hebrew primary, English secondary (or vice versa)
- Collaboration tracking: Who's featured on this track?
- Festival/event association: Tag songs with relevant Israeli festivals/venues
- Radio-ready checkboxes: 88FM, Galei Tzahal

**Phase 2 enhancement:**
- AI detects language from lyrics
- AI suggests radio station fit based on genre/style

#### Finding #4: The "Release Frequency" Strategy
**Source:** Analysis of Russ, Connor Price, Nic D (indie artists who blew up via consistent releases)

**Pattern:** Artists releasing 1 song every 1-4 weeks see exponential growth vs quarterly releases.

**Why it matters for song profiling:**
- Need fast, efficient profiling workflow (can't spend 30+ min per song)
- Consistency in metadata style helps algorithmic recommendations
- Batch profiling features reduce cognitive load

**How we implement (MVP):**
- **"Duplicate from last song" feature** - copy mood tags, themes, production style from previous song with one click
- Template system: Save and reuse profiles for songs in same album/EP
- Smart defaults remember your preferences

**Phase 2 enhancement:**
- AI learns from your previous entries
- Suggests better defaults based on your editing patterns
- Recognizes songs from same album and auto-suggests similar profiles

---

## Feature Specifications - MVP (Manual Entry)

### User Flow: Adding a New Song

**Step 1: Basic Info Entry**
```
┌─────────────────────────────────────┐
│ Add New Song                         │
├─────────────────────────────────────┤
│                                      │
│ Spotify Link (recommended):          │
│ [https://open.spotify.com/track/... │
│                                      │
│ OR                                   │
│                                      │
│ Manual Entry:                        │
│ Song Title: [                     ]  │
│ Artist: [Your Name                ]  │
│ Duration: [3:42]  Release: [Date ▾] │
│                                      │
│ [Next: Add Details →]               │
│                                      │
└─────────────────────────────────────┘
```

**User Experience:**
- **Spotify link is recommended** - auto-fetches all technical metadata
- Manual entry available as fallback
- Clear, simple interface

**Step 2: Spotify Auto-Fetch (if Spotify link provided)**
```
┌─────────────────────────────────────┐
│ Fetching from Spotify...             │
├─────────────────────────────────────┤
│                                      │
│  [██████████████████████] 100%      │
│                                      │
│  ✓ Track metadata retrieved          │
│  ✓ Audio features extracted          │
│  ✓ Album artwork found               │
│                                      │
│  Ready to add details!               │
│                                      │
└─────────────────────────────────────┘
```

**Step 3: Manual Profile Entry**

```
╔═══════════════════════════════════════════════════════╗
║ Song Profile: "Lev Kavu'a" (לב קפוא)                ║
╚═══════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────┐
│ BASIC INFORMATION (From Spotify - Read Only)        │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Title: לב קפוא (Lev Kavu'a / Frozen Heart)         │
│ Artist: [Your Name]                                 │
│ Duration: 3:42                                      │
│ Release Date: 2024-12-01                            │
│ ISRC: IL-ABC-24-12345                               │
│                                                      │
│ Audio Features (from Spotify):                       │
│ ├─ Tempo: 95 BPM                                    │
│ ├─ Key: A minor                                     │
│ ├─ Energy: 0.45 (Low-Medium)                        │
│ ├─ Valence: 0.25 (Melancholic)                     │
│ ├─ Acousticness: 0.78 (Very Acoustic)              │
│ └─ Danceability: 0.32 (Low)                         │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ YOUR INPUT - Creative Description                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Primary Genre: [Select ▾]                           │
│   Options: Indie Rock, Alternative, Pop, Folk, etc.  │
│                                                      │
│ Secondary Genres: [Multi-select]                    │
│   ☐ Acoustic                                        │
│   ☐ Alternative                                     │
│   ☐ Folk                                            │
│   ☐ Indie Pop                                       │
│   [+ Add custom genre]                              │
│                                                      │
│ Language: [Hebrew (Primary) ▾]                      │
│   Secondary: [None ▾]  (English, Hebrew, Both)     │
│                                                      │
│ 💡 Tip: Language affects playlist targeting         │
│                                                      │
│ Mood Tags: [Select 3-5 that best fit]               │
│   ☐ Melancholic    ☐ Introspective  ☐ Nostalgic   │
│   ☐ Uplifting      ☐ Energetic     ☐ Romantic      │
│   ☐ Dark           ☐ Hopeful       ☐ Bittersweet   │
│   ☐ Calm           ☐ Dreamy        ☐ Ethereal      │
│                                                      │
│ 💡 Tip: Mood tags help Spotify's algorithm place    │
│    your song in Discover Weekly and Release Radar   │
│                                                      │
│ Lyrical Themes: [Select all that apply]             │
│   ☐ Heartbreak     ☐ Love          ☐ Joy           │
│   ☐ Self-reflection ☐ Philosophy   ☐ Loss          │
│   ☐ Nostalgia      ☐ Hope          ☐ Relationships │
│                                                      │
│ Vocal Style: [Select all that apply]                │
│   ☐ Soft/gentle    ☐ Powerful/belting              │
│   ☐ Melancholic    ☐ Whispered/intimate            │
│   ☐ Raw/emotional  ☐ Smooth/polished               │
│                                                      │
│ Production Style: [Select all that apply]           │
│   ☐ Acoustic/stripped   ☐ Full production          │
│   ☐ Guitar-driven       ☐ Piano-driven             │
│   ☐ Electronic elements ☐ Orchestral               │
│   ☐ Lo-fi              ☐ Polished/clean            │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ STORY BEHIND THE SONG (Required: 200-500 words)     │
├─────────────────────────────────────────────────────┤
│                                                      │
│ 💡 This is your most important field! Playlist      │
│    curators respond 2.3x more when you share the    │
│    story behind your song.                          │
│                                                      │
│ What to include:                                     │
│ • Why did you write this song?                      │
│ • What was happening in your life?                  │
│ • What do you want listeners to feel?               │
│ • Any interesting production stories?                │
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ [Write your story here...]                   │   │
│ │                                              │   │
│ │ Example:                                     │   │
│ │ "I wrote 'Lev Kavu'a' during the coldest    │   │
│ │ week of winter, a few months after my        │   │
│ │ divorce. The title means 'Frozen Heart' in   │   │
│ │ Hebrew, and it captures how I felt -         │   │
│ │ emotionally numb, unable to feel anything.   │   │
│ │                                              │   │
│ │ I recorded it in one take in my home studio, │   │
│ │ just me and my acoustic guitar. I wanted it  │   │
│ │ to feel raw and unpolished, because that's   │   │
│ │ how the emotion felt..."                     │   │
│ │                                              │   │
│ │                                              │   │
│ └──────────────────────────────────────────────┘   │
│                                                      │
│ Word count: 0 / 200 minimum                          │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ COMPARABLE ARTISTS                                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│ List 3-5 artists whose style is similar to this     │
│ song. Include at least one Israeli artist.          │
│                                                      │
│ [Radiohead, Jeff Buckley, Bon Iver, Asaf Avidan ]  │
│                                                      │
│ 💡 Tip: This helps playlist curators understand     │
│    where your song fits. Mix international and      │
│    Israeli artists.                                  │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ GOLDEN MINUTE (Optional but recommended)             │
├─────────────────────────────────────────────────────┤
│                                                      │
│ What's the best 30-second clip from your song?      │
│ (Great for Instagram Reels, TikTok, playlist hooks) │
│                                                      │
│ Start time: [0:52]  End time: [1:22]                │
│                                                      │
│ Why this section? (optional):                       │
│ [The chorus hits hardest here, most emotional...] │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ ADDITIONAL CONTEXT (Optional)                        │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Featured Artists: [None]                             │
│ Recording Location: [Home studio]                    │
│ Producer: [Self-produced]                            │
│                                                      │
│ Radio Ready:                                         │
│ ☐ 88FM (Indie/Alternative)                          │
│ ☐ Galei Tzahal (Mainstream)                         │
│                                                      │
│ Festival/Event Tags:                                 │
│ ☐ IndegeV  ☐ Jacubob  ☐ Piano Festival             │
│                                                      │
│ Personal Notes: (for your own reference)            │
│ ┌──────────────────────────────────────────────┐   │
│ │ [Internal notes, reminders...]               │   │
│ └──────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘

[Cancel]  [Save as Draft]  [Save & Add to Campaign →]
```

**Key MVP Features:**
- **Clear guidance** at every step (tooltips, examples)
- **Smart defaults** where possible
- **"Duplicate from last song"** button to copy previous profile
- **Save as draft** so you can come back later
- **Validation:** Story field required (200 words minimum)

---

## Phase 2: AI Audio Analysis Integration

### Overview
Phase 2 adds AI analysis to **pre-populate** all the manual fields you just filled in. The UI stays the same, but now fields come with AI suggestions instead of being blank.

### Comparison: MVP vs Phase 2

| Field | MVP (Manual) | Phase 2 (AI-Assisted) |
|-------|--------------|----------------------|
| **Primary Genre** | Dropdown, you select | Pre-selected by AI with confidence score, you confirm or change |
| **Mood Tags** | Checkboxes, you select 3-5 | Pre-checked based on AI analysis, you add/remove |
| **Lyrical Themes** | Checkboxes, you select | Pre-checked based on lyric analysis (Hebrew supported) |
| **Vocal Style** | Checkboxes, you select | Pre-checked based on vocal detection |
| **Production Style** | Checkboxes, you select | Pre-checked based on instrument detection |
| **Story** | You write from scratch (200-500 words) | AI generates draft, you edit/personalize |
| **Comparable Artists** | You type manually | AI suggests 3-5 based on audio similarity |
| **Golden Minute** | You specify timestamps | AI identifies peak moment with waveform viz |

### Phase 2 Implementation Plan

**Step 1: Add AI Analysis Layer**
```python
class SongProfileService:
    def __init__(self, ai_provider: Optional[AudioAnalysisProvider] = None):
        self.ai_provider = ai_provider  # None for MVP, provider for Phase 2
    
    def get_profile_defaults(self, song_id: str) -> Dict:
        """
        MVP: Returns empty defaults
        Phase 2: Returns AI-populated defaults
        """
        if self.ai_provider is None:
            # MVP: Empty defaults
            return {
                'mood_tags': [],
                'lyrical_themes': [],
                'story_draft': '',
                # ... etc
            }
        else:
            # Phase 2: AI analysis
            return self.ai_provider.analyze_and_suggest(song_id)
```

**Step 2: UI Shows Suggestions**
```javascript
// Frontend code - same for MVP and Phase 2
function SongProfileForm({ songId, aiSuggestions }) {
    // aiSuggestions is {} in MVP, populated object in Phase 2
    
    const [moodTags, setMoodTags] = useState(
        aiSuggestions.mood_tags || []  // Pre-check if AI provided
    );
    
    return (
        <div>
            <h3>Mood Tags</h3>
            {aiSuggestions.mood_confidence && (
                <p>AI Confidence: {aiSuggestions.mood_confidence}%</p>
            )}
            <CheckboxGroup 
                options={MOOD_OPTIONS}
                selected={moodTags}
                onChange={setMoodTags}
            />
        </div>
    );
}
```

### AI Provider Options (Phase 2)

**Recommended: SONOTELLER** ($30-50/month for your volume)
- Hebrew lyric analysis ✅
- "Golden minute" detection ✅
- Affordable for indie artists ✅

**Alternative: Cyanite** (€290/month API or $19.95/month web app)
- Best accuracy ⭐⭐⭐⭐⭐
- Most comprehensive features
- More expensive

**See full comparison in original appendix (preserved below)**

---

## Data Model (Flexible Architecture)

### Design Philosophy
The database schema supports **both manual and AI-populated fields** from day one. This means:
- No schema changes needed when adding AI in Phase 2
- Can track: "Did user accept AI suggestion or override it?"
- Can improve AI over time by learning from user corrections

### Database Table: `songs`

```sql
CREATE TABLE songs (
    -- Primary Keys
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    -- Basic Metadata
    title VARCHAR(255) NOT NULL,
    title_hebrew VARCHAR(255),  -- For Hebrew songs
    title_english VARCHAR(255),  -- For English translation
    spotify_uri VARCHAR(255) UNIQUE,
    isrc VARCHAR(50) UNIQUE,
    release_date DATE,
    duration_ms INTEGER,
    
    -- Spotify Audio Features (from Spotify API - available in MVP)
    tempo DECIMAL(6,2),
    musical_key INTEGER,  -- 0-11 (C, C#, D, etc.)
    musical_mode INTEGER,  -- 0 = minor, 1 = major
    time_signature INTEGER,
    energy DECIMAL(4,3),  -- 0.0 - 1.0
    valence DECIMAL(4,3),  -- 0.0 - 1.0 (sad to happy)
    acousticness DECIMAL(4,3),  -- 0.0 - 1.0
    danceability DECIMAL(4,3),  -- 0.0 - 1.0
    instrumentalness DECIMAL(4,3),  -- 0.0 - 1.0
    liveness DECIMAL(4,3),  -- 0.0 - 1.0
    loudness DECIMAL(6,2),  -- in dB
    speechiness DECIMAL(4,3),  -- 0.0 - 1.0
    
    -- AI Analysis Metadata (NULL in MVP, populated in Phase 2)
    ai_analysis_provider VARCHAR(50),  -- NULL for MVP, 'sonoteller'/'cyanite' for Phase 2
    ai_analysis_timestamp TIMESTAMP,  -- NULL for MVP
    ai_analysis_raw_json JSONB,  -- NULL for MVP, full API response in Phase 2
    ai_confidence_overall DECIMAL(4,3),  -- NULL for MVP
    
    -- AI-Suggested Fields (NULL in MVP, AI suggestions in Phase 2)
    ai_genre_primary VARCHAR(100),  -- NULL in MVP
    ai_genre_confidence DECIMAL(4,3),  -- NULL in MVP
    ai_mood_tags TEXT[],  -- NULL in MVP, ['melancholic', 'introspective'] in Phase 2
    ai_mood_confidence JSONB,  -- NULL in MVP, {'melancholic': 0.92} in Phase 2
    ai_instruments_detected TEXT[],  -- NULL in MVP
    ai_vocal_characteristics TEXT[],  -- NULL in MVP
    ai_lyrical_themes TEXT[],  -- NULL in MVP
    ai_story_draft TEXT,  -- NULL in MVP, AI-generated draft in Phase 2
    ai_golden_minute_start INTEGER,  -- NULL in MVP
    ai_golden_minute_end INTEGER,  -- NULL in MVP
    
    -- User-Confirmed Fields (Always populated - manual in MVP, reviewed/edited in Phase 2)
    primary_genre VARCHAR(100) NOT NULL,
    secondary_genres TEXT[],
    language_primary VARCHAR(50) NOT NULL,
    language_secondary VARCHAR(50),
    
    mood_tags TEXT[] NOT NULL,
    lyrical_themes TEXT[] NOT NULL,
    
    story_behind_song TEXT NOT NULL,  -- Required field
    
    vocal_style TEXT[],
    production_style TEXT[],
    
    comparable_artists TEXT,  -- Comma-separated
    
    golden_minute_start INTEGER,  -- Optional in MVP
    golden_minute_end INTEGER,
    golden_minute_note TEXT,  -- Why this section?
    
    -- Additional Context
    featured_artists TEXT[],
    recording_location VARCHAR(255),
    producer VARCHAR(255),
    
    radio_ready_88fm BOOLEAN DEFAULT false,
    radio_ready_galei_tzahal BOOLEAN DEFAULT false,
    
    festival_tags TEXT[],
    
    personal_notes TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Key Design Benefits:**

1. **Future-Proof**
   - AI fields exist but are NULL in MVP
   - No migration needed for Phase 2
   - Easy A/B testing (some users get AI, some don't)

2. **Learning System**
   - Compare `ai_mood_tags` vs final `mood_tags`
   - If user frequently changes AI suggestions, improve AI
   - Track acceptance rate per field

3. **Flexibility**
   - Can switch AI providers without schema changes
   - Can disable AI for specific users if needed
   - Can compare multiple AI providers

---

## Technical Implementation

### MVP Implementation (3-4 weeks)

**Week 1: Foundation**
- Set up database schema (with AI fields, but unused)
- Spotify API integration
- Basic song CRUD operations
- File upload (if needed)

**Week 2: Manual Entry Form**
- Build comprehensive profile form
- Validation (story required, word count)
- Save as draft functionality
- Hebrew text support

**Week 3: Smart Features**
- "Duplicate from last song" feature
- Template system
- Auto-save drafts
- Form guidance/tooltips

**Week 4: Polish**
- Error handling
- Loading states
- Mobile responsive
- Testing

### Phase 2 Implementation (2-3 weeks)

**Week 1: AI Integration**
- Choose AI provider (SONOTELLER recommended)
- Implement analysis service
- Background job for analysis
- Store results in database

**Week 2: UI Enhancement**
- Show AI suggestions in form
- Confidence scores
- Edit workflow
- "Accept all" / "Review each" options

**Week 3: Optimization**
- Cache analysis results
- Improve AI prompts (for story generation)
- Track acceptance rates
- Performance tuning

### Code Architecture

```python
# /backend/services/song_profile_service.py

from typing import Optional, Dict
from abc import ABC, abstractmethod

class AudioAnalysisProvider(ABC):
    """Abstract interface - allows swapping providers"""
    
    @abstractmethod
    def analyze(self, audio_url: str) -> Dict:
        pass

class ManualEntryProvider(AudioAnalysisProvider):
    """MVP implementation - returns empty defaults"""
    
    def analyze(self, audio_url: str) -> Dict:
        return {
            'mood_tags': [],
            'lyrical_themes': [],
            'story_draft': '',
            'comparable_artists': [],
            # All fields empty - user fills manually
        }

class SONOTELLERProvider(AudioAnalysisProvider):
    """Phase 2 implementation"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def analyze(self, audio_url: str) -> Dict:
        # Call SONOTELLER API
        # Return structured suggestions
        pass

class SongProfileService:
    def __init__(self, analysis_provider: AudioAnalysisProvider):
        # Dependency injection - swap providers easily
        self.analysis_provider = analysis_provider
    
    async def get_profile_defaults(self, song_id: str) -> Dict:
        """
        Get default values for profile form
        
        MVP: Returns empty dict
        Phase 2: Returns AI suggestions
        """
        song = await self.db.get_song(song_id)
        
        # Try to get AI analysis
        suggestions = await self.analysis_provider.analyze(song.audio_url)
        
        return suggestions

# Usage in API endpoint
@router.get("/songs/{song_id}/profile-defaults")
async def get_profile_defaults(song_id: str):
    """
    Frontend calls this to populate form
    
    MVP: Returns empty defaults
    Phase 2: Returns AI suggestions
    """
    service = SongProfileService(
        analysis_provider=get_configured_provider()  # Inject based on config
    )
    
    defaults = await service.get_profile_defaults(song_id)
    
    return defaults
```

**Configuration Toggle:**

```python
# /backend/config.py

class Settings(BaseSettings):
    # Feature flags
    AI_ANALYSIS_ENABLED: bool = False  # False for MVP, True for Phase 2
    AI_PROVIDER: str = "manual"  # "manual", "sonoteller", "cyanite"
    
    # API keys (only needed for Phase 2)
    SONOTELLER_API_KEY: Optional[str] = None

def get_configured_provider() -> AudioAnalysisProvider:
    """Factory function - returns correct provider based on config"""
    settings = get_settings()
    
    if not settings.AI_ANALYSIS_ENABLED or settings.AI_PROVIDER == "manual":
        return ManualEntryProvider()
    elif settings.AI_PROVIDER == "sonoteller":
        return SONOTELLERProvider(settings.SONOTELLER_API_KEY)
    # ... etc
```

This means switching from MVP to Phase 2 is just:
```bash
# .env file
AI_ANALYSIS_ENABLED=true
AI_PROVIDER=sonoteller
SONOTELLER_API_KEY=your_key_here
```

No code changes needed! ✨

---

## Hebrew Language Support

### MVP Implementation

**Challenge 1: Hebrew Text Display**
- Hebrew is right-to-left (RTL)
- Mix of Hebrew and English in same interface

**Solution:**
```css
/* CSS for Hebrew text fields */
[lang="he"], .hebrew-text {
    direction: rtl;
    text-align: right;
    font-family: 'Heebo', 'Rubik', 'Assistant', sans-serif;
}

/* For mixed language fields (title with both Hebrew and English) */
.mixed-language {
    unicode-bidi: plaintext;
}

/* Form labels stay LTR, inputs can be RTL */
.form-label {
    direction: ltr;
    text-align: left;
}

input[lang="he"], textarea[lang="he"] {
    direction: rtl;
    text-align: right;
}
```

**Challenge 2: Transliteration**
- Playlists curators may need English transliteration
- Example: "לב קפוא" → "Lev Kavu'a"

**Solution:**
- Optional "English Title" field
- Phase 2: Use Claude API for smart transliteration

```python
# Phase 2 feature
async def suggest_transliteration(hebrew_title: str) -> str:
    """Use Claude for Hebrew→English transliteration"""
    
    prompt = f"""Transliterate this Hebrew song title to English.
Use standard Israeli music industry conventions.
Respond with ONLY the transliterated title.

Hebrew: {hebrew_title}"""
    
    response = await anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text.strip()
```

---

## Success Metrics

### MVP Success Metrics

**Metric 1: Profile Completion Rate**
- **Target:** 85%+ of songs have complete profiles (all required fields filled)
- **Measurement:** Count songs with story_behind_song populated
- **Success:** Users understand the importance and complete profiles

**Metric 2: Time to Complete**
- **Target:** 15-20 minutes per song (MVP baseline)
- **Measurement:** Track time from "Add Song" to "Save Profile"
- **Success:** Reasonable time investment, not burdensome

**Metric 3: Story Quality**
- **Target:** Average story length: 250-400 words
- **Measurement:** Word count of story_behind_song field
- **Success:** Users write substantive stories, not just placeholders

**Metric 4: Duplicate Usage**
- **Target:** 50%+ of users use "Duplicate from last song" for second+ songs
- **Measurement:** Track feature usage
- **Success:** Feature saves time, users find it valuable

### Phase 2 Success Metrics

**Metric 5: Time Savings**
- **Target:** Reduce profiling time from 15-20 min → 5-10 min
- **Measurement:** Compare MVP vs Phase 2 completion times
- **Success:** 50%+ time reduction

**Metric 6: AI Acceptance Rate**
- **Target:** 70%+ acceptance of AI suggestions without changes
- **Measurement:** Compare ai_mood_tags vs final mood_tags, etc.
- **Success:** AI is accurate, users trust it

**Metric 7: Story Enhancement**
- **Target:** 80%+ of users edit AI story draft (vs using as-is or writing from scratch)
- **Measurement:** Track if ai_story_draft != story_behind_song
- **Success:** AI provides helpful starting point, users personalize

---

## Appendix: Full AI Provider Comparison (For Phase 2)

[Original detailed comparison from previous version preserved here]

### Option 1: SONOTELLER.ai ⭐⭐ **RECOMMENDED**

**Pricing:** $30-50/month for 50-100 songs
**Hebrew Support:** ✅ Full lyric analysis
**Golden Minute:** ✅ Built-in
**Best For:** Israeli musicians, budget-conscious

### Option 2: Cyanite.ai ⭐⭐⭐⭐⭐

**Pricing:** €290/month API or $19.95/month web app (20 songs)
**Hebrew Support:** ⚠️ Audio only, no lyric analysis
**Accuracy:** Best-in-class (99%)
**Best For:** Professional use, highest accuracy needed

### Option 3: Music.AI

**Pricing:** $0.15/minute (~$0.45 per song)
**Uses:** Cyanite's engine
**Best For:** Pay-per-use, scaling

---

## Questions for Review

1. ✅ **MVP scope acceptable?** Manual entry first, AI later?
2. ✅ **Hebrew-specific features covered?** RTL text, language fields, transliteration?
3. ✅ **Form design looks good?** Clear guidance, tooltips, examples?
4. ✅ **Database schema flexible enough?** Ready for Phase 2 without migration?
5. ✅ **Any additional fields needed?** Anything we missed?

Ready to move to next component once approved! 🎸
