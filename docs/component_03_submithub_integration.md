# Component Design: SubmitHub Integration

## Document Version: 1.0
## Date: February 7, 2026  
## Status: Ready for Review

---

## Executive Summary

**Purpose:** Integrate with SubmitHub (leading playlist pitching platform) to streamline playlist submissions and track results.

**What is SubmitHub:**
- Platform connecting artists with playlist curators, bloggers, radio stations
- ~$1-3 per submission (curator gets paid to review)
- Response within 48 hours guaranteed
- Higher acceptance rates than cold emailing

**MVP Approach:**
- **Manual workflow** - generate submission data, you submit via SubmitHub website
- Track SubmitHub campaigns in our tool
- Import results manually

**Phase 2 Enhancement:**
- SubmitHub API integration (if available)
- Automated submission
- Auto-import results

**MVP Deliverable:** SubmitHub campaign planner + manual result tracking

---

## Research: SubmitHub Best Practices

### Finding #1: SubmitHub Dramatically Improves Response Rates
**Source:** Indie artist case studies

**Data:**
- Cold email to curators: ~5-10% response rate
- SubmitHub: ~70% response rate (curators paid to respond)
- Acceptance rate: 15-25% depending on song quality and targeting

**Why it works:**
- Curators are incentivized to listen ($1-2 per review)
- 48-hour response guarantee
- Feedback provided even for rejections
- Artist only pays for curator time, not placement

### Finding #2: Genre Targeting is Critical
**Source:** SubmitHub success patterns

**Key Insights:**
- Submitting to wrong genre = waste of money (instant rejection)
- "Shotgun approach" (submit to everyone) = expensive and ineffective
- Targeted approach (10-15 relevant curators) = better ROI
- Check curator's recent adds before submitting

**Implementation:**
- Tool suggests relevant SubmitHub curators based on song profile
- Show curator's genre focus and recent adds
- Budget calculator based on submission count

### Finding #3: Cost Management
**Source:** Indie artist budgets

**Costs:**
- Standard credits: $3 per submission
- Premium credits: $1 per submission (bulk purchase)
- Average campaign: 10-20 submissions = $10-60
- Fit within your $100-300/month campaign budget

**Implementation:**
- Track SubmitHub spend as part of campaign budget
- Recommend 10-15 curators per song (not 50+)
- Show expected cost before campaign launch

---

## Feature Specifications - MVP

### Core Features

**1. SubmitHub Campaign Planner**

```
┌─────────────────────────────────────────────────────┐
│ Plan SubmitHub Campaign for "Lev Kavu'a"            │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Based on your song profile:                         │
│ ├─ Genre: Indie Rock, Alternative, Acoustic         │
│ ├─ Mood: Melancholic, Introspective                │
│ └─ Language: Hebrew                                 │
│                                                      │
│ Recommended Approach:                                │
│ Submit to 10-15 curators for optimal ROI            │
│                                                      │
│ Estimated Cost:                                      │
│ ├─ 10 curators @ $3 each = $30                      │
│ ├─ 15 curators @ $3 each = $45                      │
│ └─ 20 curators @ $3 each = $60                      │
│                                                      │
│ 💡 Tip: Premium credits ($1 each) available         │
│    if you buy bulk. 30 credits for $30.             │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ RECOMMENDED CURATORS                                 │
├─────────────────────────────────────────────────────┤
│                                                      │
│ ✅ IndieRockPlaylist                                │
│ 🎵 Focus: Indie Rock, Alternative                   │
│ 👥 Audience: 12K followers                          │
│ 📊 Approval Rate: ~20%                              │
│ 🇮🇱 Israeli Artists: Sometimes                      │
│                                                      │
│ Recent Adds: Similar melancholic indie songs        │
│                                                      │
│ [View on SubmitHub] [Add to Campaign]              │
│                                                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│ ✅ AcousticVibesPlaylist                            │
│ 🎵 Focus: Acoustic, Singer-Songwriter              │
│ 👥 Audience: 8K followers                           │
│ 📊 Approval Rate: ~25%                              │
│                                                      │
│ [View on SubmitHub] [Add to Campaign]              │
│                                                      │
└─────────────────────────────────────────────────────┘

Selected Curators: 12
Estimated Cost: $36

[Cancel] [Generate Submission Brief] [Track Campaign]
```

**2. Submission Brief Generator**

Since we can't auto-submit via API in MVP, generate a document you can use:

```
SUBMITHUB CAMPAIGN BRIEF
Song: "Lev Kavu'a" (Frozen Heart)
Date: Feb 7, 2026

SONG DETAILS FOR SUBMISSION:
├─ Spotify Link: [auto-filled from song profile]
├─ Genre: Indie Rock
├─ Language: Hebrew
├─ Release Date: Dec 1, 2024

SHORT PITCH (use this in SubmitHub):
"Melancholic indie rock song about emotional numbness 
after heartbreak. Acoustic guitar-driven with vulnerable 
Hebrew vocals. Fans of Radiohead and Bon Iver."

CURATORS TO SUBMIT TO (12 selected):
1. IndieRockPlaylist - $3
2. AcousticVibesPlaylist - $3
3. [... 10 more]

TOTAL COST: $36

NEXT STEPS:
1. Go to submithub.com
2. Upload your song if not already there
3. Submit to these 12 curators
4. Copy this campaign ID: CAMP-20260207-001
5. Return here to track results

[Copy Brief] [Download PDF]
```

**3. Campaign Result Tracker**

```
┌─────────────────────────────────────────────────────┐
│ SubmitHub Campaign: CAMP-20260207-001               │
│ Song: "Lev Kavu'a"                                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Status: In Progress                                  │
│                                                      │
│ Results (update manually as you receive):            │
│ ├─ Submitted: 12 curators                           │
│ ├─ Responses: 8                                      │
│ ├─ Approved: 2 🎉                                    │
│ ├─ Declined: 6                                      │
│ └─ Pending: 4                                       │
│                                                      │
│ Spend: $36 / $50 budgeted                           │
│                                                      │
│ [Add Result] [View Feedback] [Close Campaign]      │
│                                                      │
└─────────────────────────────────────────────────────┘

ADD RESULT:
┌─────────────────────────────────────────────────────┐
│ Curator: IndieRockPlaylist                          │
│ Status: ○ Approved  ● Declined  ○ Still Pending    │
│                                                      │
│ Feedback (copy from SubmitHub):                     │
│ ┌──────────────────────────────────────────────┐   │
│ │ "Great song, but doesn't fit our current    │   │
│ │  playlist direction. Looking for more        │   │
│ │  upbeat indie this month."                   │   │
│ └──────────────────────────────────────────────┘   │
│                                                      │
│ [Save Result]                                       │
└─────────────────────────────────────────────────────┘
```

---

## Data Model

```sql
-- SubmitHub Campaigns
CREATE TABLE submithub_campaigns (
    id UUID PRIMARY KEY,
    campaign_code VARCHAR(50) UNIQUE, -- CAMP-20260207-001
    song_id UUID REFERENCES songs(id),
    campaign_id UUID REFERENCES campaigns(id),
    
    created_date DATE NOT NULL,
    budget_allocated DECIMAL(10,2),
    budget_spent DECIMAL(10,2) DEFAULT 0,
    
    curator_count INTEGER, -- How many curators submitted to
    
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'completed'
    
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Individual Submissions
CREATE TABLE submithub_submissions (
    id UUID PRIMARY KEY,
    submithub_campaign_id UUID REFERENCES submithub_campaigns(id),
    
    curator_name VARCHAR(255) NOT NULL,
    curator_genre_focus TEXT[],
    curator_approval_rate DECIMAL(5,2), -- e.g., 20.5 = 20.5%
    
    submission_date DATE,
    cost DECIMAL(5,2), -- $1 or $3
    
    response_status VARCHAR(50), -- 'pending', 'approved', 'declined'
    response_date DATE,
    curator_feedback TEXT,
    
    playlist_added BOOLEAN DEFAULT false,
    playlist_url VARCHAR(255),
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Technical Implementation

### MVP (Weeks 1-2)

**Week 1: Campaign Planner**
- UI for selecting curators
- Brief generator
- Cost calculator

**Week 2: Result Tracker**
- Manual result entry form
- Campaign dashboard
- Integration with budget tracking

### Phase 2: API Integration (Future)

**SubmitHub API Research:**
- Check if SubmitHub offers API access
- If yes: automate submission and result import
- If no: keep manual workflow

**Potential API Features:**
```python
# Hypothetical SubmitHub API
def search_curators(genres, moods):
    # Find matching curators
    pass

def submit_to_curator(song_url, curator_id, pitch_text):
    # Submit song
    pass

def get_campaign_results(campaign_id):
    # Fetch results
    pass
```

---

## Integration with Other Components

**Links to Component 1 (Song Profile):**
- Pull genre, mood, language for curator matching
- Use "story behind song" for pitch text

**Links to Component 4 (Budget Management):**
- Track SubmitHub spend as expense
- Include in campaign budget calculations
- Show ROI (cost per playlist add)

**Links to Component 5 (Dashboard):**
- Display SubmitHub results in unified view
- Compare SubmitHub ROI vs other channels

---

## Success Metrics

**Metric 1: Campaign ROI**
- Target: $2-5 per playlist add
- Measurement: Total SubmitHub spend / playlist adds
- Success: Competitive with other promotion methods

**Metric 2: Approval Rate**
- Target: 15-25% of submissions approved
- Measurement: Track approved/declined ratio
- Success: Indicates good curator targeting

**Metric 3: Feedback Quality**
- Target: 80%+ of declines include feedback
- Measurement: Track feedback presence
- Success: Helps improve future submissions

---

## Cost Analysis

**For Your Budget ($100-300/campaign):**

**Conservative Approach:**
- 10 curators @ $3 each = $30
- ~2-3 playlist adds expected (20% rate)
- Cost per add: $10-15

**Aggressive Approach:**
- 20 curators @ $3 each = $60  
- ~4-5 playlist adds expected
- Cost per add: $12-15

**Recommendation:**
Start with 10-15 curators per song, learn what works, then scale.

---

## Questions for Review

1. ✅ **Manual workflow acceptable for MVP?** Or need API from day 1?
2. ✅ **Budget allocation:** $30-60 per song reasonable?
3. ✅ **Should we include curator rating system?** (your own notes on which curators worked)
4. ✅ **Track detailed feedback?** Or just approved/declined?

Ready for Component 4: Campaign & Budget Management! 🎸
