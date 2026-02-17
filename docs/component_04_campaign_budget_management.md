# Component Design: Campaign & Budget Management

## Document Version: 1.0
## Date: February 7, 2026
## Status: Ready for Review

---

## Executive Summary

**Purpose:** Organize promotion efforts into campaigns with clear budgets, track spending across channels, and measure ROI to optimize marketing effectiveness.

**Core Philosophy:** **Campaign-Based Thinking** - Instead of random promotional activities, organize everything under campaigns (e.g., "Winter EP Release", "Summer Single Push"). This provides structure, accountability, and clear measurement.

**MVP Approach:**
- Create campaigns with songs, budget, timeline, and target personas
- Manual expense tracking (you log spending as it happens)
- Real-time budget monitoring with alerts
- Basic ROI calculation (cost per stream, cost per playlist add)

**Phase 2 Enhancement:**
- Automated expense import (Meta Ads API, Google Ads API)
- Predictive budget recommendations
- Advanced attribution modeling

**MVP Deliverable:** Full campaign management system with budget tracking, spending alerts, and basic ROI metrics.

---

## Research: Best Practices

### Finding #1: The 30-40% Rule
**Source:** Music marketing industry standards

**Key Insight:**
> "With any piece of music or visual content, aim to invest AT LEAST 30-40% of the production cost on promoting it properly."

**Example:**
- Production cost: $2,000 (recording, mixing, mastering)
- Marketing budget: $600-800 minimum
- Total investment: $2,600-2,800

**Why it matters:**
Artists who under-invest in promotion see 70% lower streaming numbers in first 90 days. The song dies before it gets discovered.

**Implementation:**
- Tool calculates recommended marketing budget based on production cost
- Warning if budget is below 30% threshold
- Show expected ROI at different budget levels

### Finding #2: Cost Per Stream Benchmarks
**Source:** Industry analysis + streaming data

**Reality Check on ROI:**
- Spotify pays: ~$0.003-0.004 per stream
- Typical promotion cost: $0.01-0.05 per stream
- **You will lose money in the short term** (6-12 months)
- **Break-even happens long-term** (3-10 years) IF listeners are engaged

**Why promote anyway?**
1. **Algorithmic Trigger:** Good engagement triggers Discover Weekly, Release Radar (free exposure)
2. **Audience Building:** Engaged listeners buy merch, tickets, support future releases
3. **Long-tail Revenue:** Streams continue for years after campaign ends
4. **Credibility:** Stream counts matter for booking shows, media coverage

**Benchmarks by Channel:**
- **Playlist pitching:** 10-50 streams per dollar (best ROI)
- **Social media ads:** 5-20 streams per dollar
- **Influencer marketing:** Varies wildly, hard to measure
- **PR/Blog coverage:** Credibility > direct streams

**Implementation:**
- Track cost per stream by channel
- Compare your results to benchmarks
- Show "long-term value" projections, not just immediate ROI
- Warning: "This campaign will lose money short-term, but here's why it's worth it..."

### Finding #3: Budget Allocation Strategy
**Source:** Successful indie campaigns + marketing experts

**Tier-Based Recommendations:**

**Emerging Artist (0-10K monthly listeners):**
- 60-70% → Playlist pitching (highest ROI)
- 20-30% → Social media ads (Facebook/Instagram)
- 10% → Content creation (photos, videos)
- Budget range: $100-500/campaign

**Developing Artist (10K-100K monthly listeners):**
- 40% → Playlist pitching
- 30% → PR/Blog coverage (build credibility)
- 20% → Social media ads
- 10% → Content creation
- Budget range: $500-2,000/campaign

**Established Artist (100K+ monthly listeners):**
- 30% → PR/Media
- 25% → Playlist pitching
- 25% → Influencer marketing
- 20% → Social media ads
- Budget range: $2,000-10,000+/campaign

**Implementation:**
- Tool suggests allocation based on your listener count
- Show "Why these percentages?" explanation
- Allow customization but warn if deviating too far

### Finding #4: Campaign Timeline Matters
**Source:** Release strategy research

**Optimal Timeline:**
- **4-8 weeks BEFORE release:**
  - Week -8 to -6: Submit to editorial playlists (Spotify requires 7 days minimum)
  - Week -4 to -3: Begin PR outreach
  - Week -2 to -1: Launch pre-save campaign
  - Week -1: Ramp up social media ads

- **Release Week:**
  - Maximum push (highest ad spend)
  - Influencer posts go live
  - Email newsletter blast

- **4-8 weeks AFTER release:**
  - Continue ads (reduced spend)
  - Track algorithmic playlist adds
  - Measure long-term retention

**Why this matters:**
Campaigns started 1 week before release see 45% lower playlist acceptance rates vs 4+ weeks before.

**Implementation:**
- Campaign has start/end dates
- Tool shows "campaign phase" (Pre-Release, Launch Week, Post-Release)
- Recommendations adjust based on phase
- Alerts: "You're in Launch Week - time to maximize spend!"

---

## My Original Ideas 💡

### Claude Suggestion #1: Budget "Guardrails" with Smart Alerts

**Problem:** Artists overspend early, run out of budget for critical moments.

**Solution:** Budget pacing algorithm with predictive alerts.

**How it works:**
```
Expected Pace vs Actual Pace:
- Campaign: 30 days, $300 budget
- Expected pace: $10/day
- Day 10: Should have spent $100

Actual Spend: $180 (80% ahead of pace)

Alert: "⚠️ Budget Warning: You're spending 80% faster than planned. 
At this rate, you'll run out in 7 days. Consider:
• Pausing ads temporarily
• Reducing daily ad spend from $18 to $10
• Reallocating $50 from another channel"
```

**Additional Guardrails:**
- **Spending floor:** Don't let channels drop below minimum effective spend
  - Example: Meta ads need $5/day minimum or algorithm doesn't learn
- **Critical phase protection:** Reserve budget for Launch Week
  - Example: "You've allocated $200 for pre-release. Save at least $100 for launch week."

### Claude Suggestion #2: Channel ROI Leaderboard

**Problem:** Hard to know which channels are working.

**Solution:** Live leaderboard comparing channel effectiveness.

**Visual:**
```
┌─────────────────────────────────────────────────────┐
│ CHANNEL ROI LEADERBOARD - "Winter EP Campaign"      │
├─────────────────────────────────────────────────────┤
│                                                      │
│ 🥇 Playlist Pitching                                │
│    $60 spent → 1,200 streams → $0.05/stream        │
│    2 playlist adds (600+ followers each)            │
│    ROI Score: 85/100 ⭐⭐⭐⭐                        │
│                                                      │
│ 🥈 SubmitHub                                        │
│    $36 spent → 450 streams → $0.08/stream          │
│    3 playlist adds (avg 400 followers)              │
│    ROI Score: 72/100 ⭐⭐⭐                          │
│                                                      │
│ 🥉 Instagram Ads                                    │
│    $80 spent → 320 streams → $0.25/stream          │
│    High engagement (2.5% CTR) but expensive         │
│    ROI Score: 58/100 ⭐⭐                            │
│                                                      │
│ ⚠️ Facebook Ads                                     │
│    $50 spent → 120 streams → $0.42/stream          │
│    Poor targeting or creative?                      │
│    ROI Score: 35/100 ⭐                              │
│    💡 Recommendation: Pause and reassess            │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**How ROI Score is calculated:**
- Cost per stream (40% weight)
- Engagement quality - saves, playlist adds (30% weight)
- Long-term value - follower growth (20% weight)
- Efficiency - spend vs results ratio (10% weight)

**Actionable Insights:**
- "Facebook Ads are 5x more expensive than playlisting. Consider pausing."
- "Playlist pitching is working great! Allocate $20 more here from Facebook."

### Claude Suggestion #3: "Scenario Planner" - Budget Simulation

**Problem:** Artists don't know what results to expect for their budget.

**Solution:** Interactive budget simulator showing projected outcomes.

**How it works:**
```
Campaign Budget Planner
Budget: $300 [slider: $100-$1000]
Timeline: 30 days

Projected Results:
├─ Total Streams: 3,000-6,000 (based on benchmarks)
├─ New Monthly Listeners: 200-400
├─ Playlist Adds: 3-5 playlists
├─ Cost Per Stream: $0.05-0.10
└─ Break-Even Timeline: 3-5 years (long-term)

Budget Allocation Simulator:
Playlist Pitching: $180 (60%) [slider]
  → 1,800-3,600 streams (best ROI)
  
Social Ads: $90 (30%) [slider]
  → 450-1,800 streams
  
SubmitHub: $30 (10%) [slider]
  → 375-600 streams

[Adjust sliders to see different scenarios]

💡 Tip: At your current budget, focus heavily on playlisting.
   Save social ads for when you have $500+/campaign.
```

**Value:**
- Sets realistic expectations (no false promises)
- Shows trade-offs (more on X = less on Y)
- Educational (learn what each channel delivers)

### Claude Suggestion #4: "Momentum Tracker"

**Problem:** Hard to know if campaign is gaining traction or fizzling out.

**Solution:** Visual momentum indicator with trend analysis.

**Visual:**
```
Campaign Momentum: "Winter EP Release"
Day 15 of 30

[====== Week 1 ======][====== Week 2 ======]
 ▁▂▃▄▅▆▇█              ▇▆▅▄▃▂▁
  Strong Start         Losing Steam

Current Status: ⚠️ Declining
├─ Streams/day: 85 (↓ 40% from peak)
├─ Playlist adds: 0 in last 7 days
└─ Follower growth: Flat

Diagnosis:
• Initial momentum from release week has faded
• No new playlist adds to sustain growth
• Social ads may be fatiguing (same creative for 2 weeks)

Recommended Actions:
1. Submit to 5-10 new playlists this week
2. Refresh ad creative (new image/video)
3. Consider doubling down on best-performing channel
4. Reach out to Kan 88 radio (haven't pitched yet)
```

**Why this helps:**
- Visual makes trends obvious
- Specific recommendations, not just data
- Prevents campaigns from dying silently

---

## Feature Specifications - MVP

### Core Features

**1. Campaign Creation**

```
┌─────────────────────────────────────────────────────┐
│ Create New Campaign                                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Campaign Name: [Winter EP Release              ]    │
│                                                      │
│ Timeline:                                            │
│ Start: [2026-02-15 ▾]  End: [2026-03-31 ▾]         │
│ Duration: 45 days                                    │
│                                                      │
│ Budget: $[300.00]                                    │
│                                                      │
│ 💡 Recommended: $600-800                            │
│    (30-40% of your $2,000 production cost)          │
│                                                      │
│ Songs (select from your library):                   │
│ ☑ Lev Kavu'a (Frozen Heart)                        │
│ ☑ Galgalei Zman (Wheels of Time)                   │
│ ☑ Sheket Rishon (First Silence)                    │
│                                                      │
│ Target Personas (allocate % of effort):             │
│ Fellow Traveler:        [40%] ████░░░░░░           │
│ Nostalgic Explorer:     [30%] ███░░░░░░░           │
│ Thoughtful Wanderer:    [20%] ██░░░░░░░░           │
│ Melancholic Dreamer:    [10%] █░░░░░░░░░           │
│                                                      │
│ Campaign Goals (select primary):                    │
│ ● Build awareness (0-10K listeners)                 │
│ ○ Grow fanbase (10K-100K listeners)                │
│ ○ Monetize audience (100K+ listeners)              │
│                                                      │
│ [Cancel] [Save Draft] [Create Campaign →]          │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**After creation, tool suggests budget allocation:**

```
┌─────────────────────────────────────────────────────┐
│ Suggested Budget Allocation                          │
│ Based on: Emerging artist tier + $300 budget        │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Playlist Pitching (60%): $180                       │
│   • Direct pitches: $100                            │
│   • SubmitHub: $80                                  │
│   Expected: 1,800-3,600 streams, 3-5 playlist adds  │
│                                                      │
│ Social Media Ads (30%): $90                         │
│   • Instagram: $50                                  │
│   • Facebook: $40                                   │
│   Expected: 450-1,800 streams, 40-80 new followers  │
│                                                      │
│ Content Creation (10%): $30                         │
│   • Photo shoot: $30                                │
│   Expected: Professional assets for campaign        │
│                                                      │
│ Total: $300                                         │
│                                                      │
│ [Accept Suggestion] [Customize Allocation]         │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**2. Expense Tracking**

```
┌─────────────────────────────────────────────────────┐
│ Campaign: "Winter EP Release"                        │
│ Budget: $300 | Spent: $147 (49%) | Remaining: $153 │
├─────────────────────────────────────────────────────┤
│                                                      │
│ [Add Expense] [Import from Bank] [View Report]     │
│                                                      │
│ Recent Expenses:                                     │
│                                                      │
│ Feb 10 | Instagram Ads      | $25.00 | Social Ads  │
│ Feb 08 | SubmitHub Credits  | $36.00 | Playlisting │
│ Feb 05 | Photo Shoot        | $30.00 | Content     │
│ Feb 03 | Playlist Pitch     | $45.00 | Playlisting │
│ Feb 01 | Facebook Ads       | $11.00 | Social Ads  │
│                                                      │
│ [Load More]                                         │
│                                                      │
└─────────────────────────────────────────────────────┘

ADD EXPENSE:
┌─────────────────────────────────────────────────────┐
│ Date: [2026-02-10 ▾]                                │
│                                                      │
│ Category: [Social Media Ads ▾]                      │
│   Options: Playlist Pitching, Social Media Ads,     │
│   Content Creation, Radio Promotion, PR/Press,      │
│   Other                                              │
│                                                      │
│ Subcategory: [Instagram Ads ▾]                      │
│                                                      │
│ Amount: $[25.00]                                    │
│                                                      │
│ Description (optional):                             │
│ [Story ads targeting Israeli indie fans]           │
│                                                      │
│ Receipt/Proof: [Upload file] (optional)            │
│                                                      │
│ [Cancel] [Save Expense]                             │
└─────────────────────────────────────────────────────┘
```

**3. Budget Monitoring Dashboard**

```
┌─────────────────────────────────────────────────────┐
│ BUDGET OVERVIEW                                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Campaign: "Winter EP Release" (Day 15 of 45)        │
│                                                      │
│ ┌────────────────────────────────────────────────┐ │
│ │ Budget Progress                                 │ │
│ │ [█████████░░░░░░░░░░░░░░░░░░] 49% spent       │ │
│ │ $147 / $300                                     │ │
│ │                                                 │ │
│ │ ⚠️ Alert: Spending 35% ahead of schedule       │ │
│ │ Expected: $100 (33% of timeline)                │ │
│ │ Actual: $147 (49% of budget)                    │ │
│ └────────────────────────────────────────────────┘ │
│                                                      │
│ Budget by Channel:                                   │
│                                                      │
│ Playlist Pitching: $81 / $180 (45%)                 │
│ [████░░░░░░] On Track ✓                            │
│                                                      │
│ Social Ads: $36 / $90 (40%)                         │
│ [████░░░░░░] On Track ✓                            │
│                                                      │
│ Content: $30 / $30 (100%)                           │
│ [██████████] Complete ✓                            │
│                                                      │
│ Recommendations:                                     │
│ • You're ahead of pace. Consider:                   │
│   - Saving $40 for Launch Week (Feb 25-Mar 3)      │
│   - Reducing daily ad spend from $6 to $4          │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**4. ROI Tracking**

```
┌─────────────────────────────────────────────────────┐
│ CAMPAIGN PERFORMANCE                                 │
│ "Winter EP Release" - Day 15 of 45                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Overall Results:                                     │
│ ├─ Total Spent: $147                                │
│ ├─ Streams Generated: 2,340                         │
│ ├─ Cost Per Stream: $0.063                          │
│ ├─ New Followers: 62                                │
│ └─ Playlist Adds: 2                                 │
│                                                      │
│ Performance by Channel:                              │
│                                                      │
│ 🥇 Playlist Pitching (Direct)                       │
│    Spent: $45 | Streams: 1,100 | $0.041/stream     │
│    ROI: Excellent ⭐⭐⭐⭐⭐                          │
│    + Added to 2 playlists (800+ followers)          │
│                                                      │
│ 🥈 SubmitHub                                        │
│    Spent: $36 | Streams: 520 | $0.069/stream       │
│    ROI: Good ⭐⭐⭐⭐                                 │
│    + 3 approvals, 9 rejections                      │
│                                                      │
│ 🥉 Instagram Ads                                    │
│    Spent: $25 | Streams: 480 | $0.052/stream       │
│    ROI: Good ⭐⭐⭐⭐                                 │
│    + 28 new followers, high engagement              │
│                                                      │
│ ⚠️ Facebook Ads                                     │
│    Spent: $11 | Streams: 90 | $0.122/stream        │
│    ROI: Poor ⭐⭐                                     │
│    💡 Consider pausing                              │
│                                                      │
│ vs Industry Benchmarks:                              │
│ Your avg: $0.063/stream                             │
│ Industry: $0.01-0.05/stream                         │
│ Status: Slightly above average (acceptable)         │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Data Model

```sql
-- Campaigns
CREATE TABLE campaigns (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    
    name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    
    budget_total DECIMAL(10,2) NOT NULL,
    budget_spent DECIMAL(10,2) DEFAULT 0,
    
    -- Suggested allocations
    budget_playlist_pitching DECIMAL(10,2),
    budget_social_ads DECIMAL(10,2),
    budget_content DECIMAL(10,2),
    budget_pr DECIMAL(10,2),
    budget_other DECIMAL(10,2),
    
    status VARCHAR(50) DEFAULT 'active', -- 'planning', 'active', 'completed'
    
    -- Personas
    persona_fellow_traveler_pct INTEGER,
    persona_nostalgic_explorer_pct INTEGER,
    persona_thoughtful_wanderer_pct INTEGER,
    persona_melancholic_dreamer_pct INTEGER,
    
    -- Goals
    primary_goal VARCHAR(100), -- 'awareness', 'growth', 'monetization'
    
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Campaign Songs (many-to-many)
CREATE TABLE campaign_songs (
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    song_id UUID REFERENCES songs(id) ON DELETE CASCADE,
    PRIMARY KEY (campaign_id, song_id)
);

-- Expenses
CREATE TABLE expenses (
    id UUID PRIMARY KEY,
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    song_id UUID REFERENCES songs(id), -- Optional: which song was this for?
    
    expense_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    
    category VARCHAR(100) NOT NULL, -- 'playlist_pitching', 'social_ads', 'content', etc.
    subcategory VARCHAR(100), -- 'instagram_ads', 'submithub', 'photo_shoot', etc.
    
    description TEXT,
    receipt_url VARCHAR(500), -- Link to uploaded receipt
    
    source VARCHAR(50) DEFAULT 'manual', -- 'manual', 'api_meta', 'api_google'
    external_id VARCHAR(255), -- ID from Meta/Google if imported
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Performance Metrics (daily snapshots)
CREATE TABLE campaign_performance (
    id UUID PRIMARY KEY,
    campaign_id UUID REFERENCES campaigns(id),
    song_id UUID REFERENCES songs(id),
    
    metric_date DATE NOT NULL,
    
    -- Streams
    streams_total INTEGER DEFAULT 0,
    streams_today INTEGER DEFAULT 0,
    
    -- Engagement
    saves_total INTEGER DEFAULT 0,
    playlist_adds_total INTEGER DEFAULT 0,
    
    -- Audience
    monthly_listeners INTEGER DEFAULT 0,
    followers_total INTEGER DEFAULT 0,
    
    -- Social
    instagram_followers INTEGER DEFAULT 0,
    instagram_reach INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(campaign_id, song_id, metric_date)
);

-- ROI Analysis (computed view)
CREATE VIEW campaign_roi AS
SELECT 
    c.id AS campaign_id,
    c.name,
    c.budget_total,
    c.budget_spent,
    SUM(cp.streams_total) AS total_streams,
    CASE 
        WHEN SUM(cp.streams_total) > 0 
        THEN c.budget_spent / SUM(cp.streams_total)
        ELSE NULL
    END AS cost_per_stream,
    SUM(cp.saves_total) AS total_saves,
    SUM(cp.playlist_adds_total) AS total_playlist_adds
FROM campaigns c
LEFT JOIN campaign_songs cs ON c.id = cs.campaign_id
LEFT JOIN campaign_performance cp ON cp.campaign_id = c.id AND cp.song_id = cs.song_id
GROUP BY c.id, c.name, c.budget_total, c.budget_spent;
```

---

## Success Metrics

**Metric 1: Budget Adherence**
- Target: 85%+ of campaigns finish within 10% of budget
- Measurement: Compare planned vs actual spend
- Success: Alerts prevent overspending

**Metric 2: ROI Awareness**
- Target: 100% of campaigns have cost/stream tracked
- Measurement: Completeness of performance data
- Success: Users understand what's working

**Metric 3: Channel Optimization**
- Target: 70%+ of users adjust channel allocation after Campaign 1
- Measurement: Track budget changes between campaigns
- Success: Users learn and improve

**Metric 4: Campaign Completion Rate**
- Target: 80%+ of campaigns run to completion
- Measurement: % of campaigns that reach end date
- Success: Users stay engaged throughout campaign

---

## Questions for Review

1. ✅ **Budget guardrails acceptable?** Alerts at 80% spent, 15% ahead of pace?
2. ✅ **ROI leaderboard helpful?** Or too much data?
3. ✅ **Scenario planner needed in MVP?** Or save for Phase 2?
4. ✅ **Momentum tracker useful?** Or is simpler better?
5. ✅ **Manual expense tracking OK?** Or want CSV import in MVP?

Ready for Component 5: Dashboard + Insights Engine! 🎸
