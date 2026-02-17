# Component Design: Dashboard + Insights Engine

## Document Version: 1.0
## Date: February 7, 2026
## Status: Ready for Review

---

## Executive Summary

**Purpose:** Unified command center showing all key metrics, campaign performance, and AI-powered insights to guide decision-making.

**Core Philosophy:** **"Data → Insight → Action"** - Don't just show numbers. Interpret them, explain what they mean, and suggest specific next steps.

**MVP Approach:**
- Real-time dashboard with key metrics (streams, followers, playlist adds)
- Campaign performance cards
- Manual data sync from Spotify for Artists
- Basic trend visualization
- Simple AI-powered insights ("Your streams are up 40% this week!")

**Phase 2 Enhancement:**
- Spotify API auto-sync (real-time)
- Advanced predictive insights
- Anomaly detection
- Competitive benchmarking

**MVP Deliverable:** Clean, actionable dashboard with essential metrics and intelligent recommendations.

---

## Research: Best Practices

### Finding #1: Segment-Based Thinking
**Source:** Spotify for Artists best practices

**Key Insight:**
Not all listeners are equal. Spotify tracks 4 key audience segments:

1. **Programmed Listeners** (28-day): Discovered you through algorithmic playlists
2. **Organic Listeners** (28-day): Found you via search, artist profile, their own library
3. **Listeners** (past 28 days): Total unique listeners
4. **Followers**: Your most engaged fans

**Why it matters:**
- **Programmed spike?** → Algorithm is working, double down on engagement
- **Organic growth?** → Marketing/playlists working, maintain momentum  
- **Follower conversion low?** → Listeners aren't committing, need stronger call-to-action

**Implementation:**
- Show all 4 segments prominently
- Explain what each means in plain language
- Alert when ratios are unhealthy (e.g., "Only 2% of listeners are following. Target: 5-10%")

### Finding #2: Save Rate is King
**Source:** Streaming algorithm research

**Key Insight:**
> "Saves are weighted more heavily than passive streams in Spotify's algorithm"

**Save Rate Benchmarks:**
- **5-10%:** Healthy (song resonates)
- **10-15%:** Excellent (strong engagement)
- **15%+:** Exceptional (potential viral hit)
- **<3%:** Problem (listeners aren't connecting)

**Why it matters:**
Save rate is the #1 predictor of:
- Discover Weekly placement
- Release Radar inclusion
- Long-term streaming success

**Implementation:**
- Calculate save rate: (Saves / Streams) × 100
- Show benchmark comparison
- Alert if save rate drops below 5%
- Suggest actions: "Low save rate. Try: Add call-to-action in posts, create Spotify Canvas, improve song ending"

### Finding #3: First 24-48 Hours Are Critical
**Source:** Release strategy research

**Key Insight:**
Spotify's algorithm heavily weights initial performance. Strong launch = algorithmic boost for weeks.

**Launch Success Indicators:**
- **Streams in first 24h:** 1,000+ (emerging), 5,000+ (developing), 20,000+ (established)
- **Save rate:** 8%+ in first week
- **Playlist adds:** 3+ within 48 hours

**Implementation:**
- "Launch Performance Score" dashboard (Day 1, Day 2, Week 1)
- Real-time alerts during launch window
- Comparison to previous releases

### Finding #4: Geographic Insights Drive Touring
**Source:** Artist marketing case studies

**Key Insight:**
Top listening cities = best tour markets. Artists who use geo data for tour planning see 30% higher ticket sales.

**How to use:**
- Identify top 10 cities by streams
- Look for unexpected hotspots (small cities with disproportionate engagement)
- Track growth by city over time (emerging markets)

**Implementation:**
- Interactive map showing listening heatmap
- City leaderboard with growth trends
- "Suggested tour markets" based on listener density

---

## My Original Ideas 💡

### Claude Suggestion #1: "Health Score" - Simplified Status Indicator

**Problem:** Too many metrics. Artists don't know if they're doing well or not.

**Solution:** Single "Health Score" (0-100) that synthesizes all metrics.

**How it's calculated:**
```
Health Score = Weighted average of:
- Streams trend (30%): Growing, stable, or declining?
- Save rate (25%): Above or below 5%?
- Follower conversion (20%): Listeners becoming fans?
- Playlist momentum (15%): New adds or removals?
- Campaign ROI (10%): Spending effectively?
```

**Visual:**
```
┌─────────────────────────────────────────────────────┐
│ YOUR MUSIC HEALTH SCORE                              │
├─────────────────────────────────────────────────────┤
│                                                      │
│           ╔════════════════╗                        │
│           ║                ║                        │
│           ║      78        ║                        │
│           ║   ⭐⭐⭐⭐      ║                        │
│           ║    Healthy     ║                        │
│           ║                ║                        │
│           ╚════════════════╝                        │
│                                                      │
│ What this means:                                     │
│ Your music is performing well. Streams are growing  │
│ steadily, and listeners are engaged. Focus on       │
│ converting more listeners to followers.              │
│                                                      │
│ What's Working:                                      │
│ ✓ Streams up 35% this week                          │
│ ✓ Save rate: 8.2% (above target)                    │
│ ✓ 2 new playlist adds                               │
│                                                      │
│ Needs Attention:                                     │
│ ⚠️ Follower conversion: 3.1% (target: 5-10%)        │
│ 💡 Action: Add "Follow" CTA to social posts         │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Color Coding:**
- **85-100:** Excellent 🟢 (keep doing what you're doing!)
- **70-84:** Healthy 🟡 (good, with room for improvement)
- **50-69:** Needs Work 🟠 (take action soon)
- **0-49:** Critical 🔴 (urgent attention needed)

### Claude Suggestion #2: "Insight Cards" - Actionable Intelligence

**Problem:** Data without context is useless. Artists see numbers but don't know what to do.

**Solution:** AI-powered insight cards that explain trends and suggest actions.

**Examples:**

```
┌─────────────────────────────────────────────────────┐
│ 🎉 MOMENTUM ALERT                                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│ "Lev Kavu'a" added to "Israeli Indie Gems"         │
│ 1,240 followers • Added 2 hours ago                │
│                                                      │
│ Impact Projection:                                   │
│ • +150-300 streams in next 7 days                   │
│ • +10-20 new monthly listeners                      │
│                                                      │
│ 💡 Action: Thank the curator on Instagram          │
│    @israeliindiegems (builds relationship)          │
│                                                      │
│ [View Playlist] [Draft Thank You Message]          │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ ⚠️ PERFORMANCE WARNING                              │
├─────────────────────────────────────────────────────┤
│                                                      │
│ "Galgalei Zman" streams dropped 60% in 48h         │
│                                                      │
│ Diagnosis:                                           │
│ Removed from "Evening Chill" playlist               │
│ (2,100 followers)                                   │
│                                                      │
│ This is normal — playlists refresh regularly.       │
│                                                      │
│ 💡 Action: Submit to 3-5 similar playlists to      │
│    replace lost exposure.                           │
│                                                      │
│ [Find Similar Playlists] [Create Pitch]            │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 🔥 OPPORTUNITY DETECTED                             │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Tel Aviv showing 3x higher listener density         │
│ than expected for your audience size.               │
│                                                      │
│ • 280 monthly listeners in Tel Aviv                 │
│ • Growing 12% week over week                        │
│ • Strong save rate: 11.2%                           │
│                                                      │
│ This suggests a engaged local fanbase!              │
│                                                      │
│ 💡 Actions to consider:                             │
│    • Plan a show in Tel Aviv                        │
│    • Target Tel Aviv in social ads                  │
│    • Reach out to local venues/blogs               │
│                                                      │
│ [View Tel Aviv Listeners] [Find Venues]            │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Types of Insights:**
- **Momentum Alerts:** New playlist adds, viral moments
- **Performance Warnings:** Drops, playlist removals
- **Opportunities:** Geographic hotspots, trending songs
- **Optimization Tips:** Improve save rate, follower conversion
- **Milestone Celebrations:** Hit 10K streams, 1K followers

### Claude Suggestion #3: "Week-Over-Week Storytelling"

**Problem:** Raw numbers are boring. Stories are memorable.

**Solution:** Narrative-style weekly recap that tells your music's story.

**Example:**

```
┌─────────────────────────────────────────────────────┐
│ YOUR WEEK IN MUSIC                                   │
│ Jan 28 - Feb 4, 2026                                │
├─────────────────────────────────────────────────────┤
│                                                      │
│ This was a STRONG week. Here's your story:          │
│                                                      │
│ 📈 Growth Snapshot                                  │
│ • 4,280 streams (+42% vs last week) ⭐             │
│ • 310 new monthly listeners (+28%)                  │
│ • 18 new followers (+15%)                           │
│                                                      │
│ 🎵 Top Performers                                   │
│ 1. "Lev Kavu'a" - 2,140 streams                    │
│    • Save rate: 9.1% (excellent!)                   │
│    • Added to 2 new playlists                       │
│    • Your best performer this week                  │
│                                                      │
│ 2. "Sheket Rishon" - 1,520 streams                 │
│    • Growing steadily (+18% WoW)                    │
│    • Strong in Jerusalem (240 listeners)            │
│                                                      │
│ 🎯 Campaign Impact                                  │
│ Your "Winter EP" campaign is working:               │
│ • Spent: $147 / $300                                │
│ • Cost per stream: $0.063 (acceptable)              │
│ • Best channel: Playlist pitching ($0.041/stream)  │
│                                                      │
│ 🌍 Where You're Growing                             │
│ • Tel Aviv: +35 listeners (now #1 city)            │
│ • Haifa: +22 listeners                              │
│ • Jerusalem: +19 listeners                          │
│                                                      │
│ 💡 This Week's Recommendation                       │
│ "Lev Kavu'a" is on fire. Double down:              │
│ • Submit to 5 more playlists (momentum is real)    │
│ • Create Instagram Reels using the chorus          │
│ • Thank playlist curators who added you            │
│                                                      │
│ Keep it up! 🚀                                      │
│                                                      │
│ [View Full Report] [Share on Social]               │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Claude Suggestion #4: "Comparison Mode" - Benchmark Against Self

**Problem:** Hard to know if current performance is good or bad without context.

**Solution:** Smart comparisons that provide perspective.

**Types of Comparisons:**

```
┌─────────────────────────────────────────────────────┐
│ HOW YOU'RE DOING                                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│ This Week vs Last Week:                              │
│ Streams:        4,280 (+42%) ⭐⭐⭐⭐                │
│ Followers:      18 (+15%)    ⭐⭐⭐                  │
│ Save Rate:      8.1% (+0.4%) ⭐⭐⭐                  │
│                                                      │
│ This Release vs Your Average:                        │
│ "Lev Kavu'a" is performing 60% BETTER than         │
│ your typical release at this stage.                 │
│                                                      │
│ First Week Performance:                              │
│ "Lev Kavu'a": 2,140 streams                        │
│ Your Average: 1,330 streams                         │
│ Your Best: 3,800 streams ("Sheket Rishon")         │
│                                                      │
│ 💡 You're on track for a strong release!           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Claude Suggestion #5: "Next Best Actions" Panel

**Problem:** Artists feel overwhelmed. "I see the data, but what should I DO?"

**Solution:** Prioritized action list based on current state.

**Example:**

```
┌─────────────────────────────────────────────────────┐
│ YOUR TOP 3 ACTIONS THIS WEEK                         │
├─────────────────────────────────────────────────────┤
│                                                      │
│ 1. 🎯 HIGH PRIORITY                                 │
│    Submit to 5 new playlists                        │
│                                                      │
│    Why: "Lev Kavu'a" has momentum. Strike while    │
│    iron is hot. High save rate (9.1%) makes it     │
│    attractive to curators.                          │
│                                                      │
│    Time: 30 min | Impact: High                      │
│    [Start Submissions →]                            │
│                                                      │
│ 2. 💬 MEDIUM PRIORITY                               │
│    Thank 2 playlist curators                        │
│                                                      │
│    Why: You were added to "Israeli Indie Gems"     │
│    and "Acoustic Vibes" this week. Build           │
│    relationships for future releases.               │
│                                                      │
│    Time: 10 min | Impact: Medium                    │
│    [View Curators →]                                │
│                                                      │
│ 3. 📊 LOW PRIORITY                                  │
│    Review campaign budget                           │
│                                                      │
│    Why: You're 35% ahead of spending pace. Might   │
│    want to slow down to preserve budget for launch. │
│                                                      │
│    Time: 5 min | Impact: Low                        │
│    [View Budget →]                                  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**How priorities are determined:**
1. **Time-sensitive opportunities** (new playlist add, viral moment)
2. **Underperforming metrics** (low save rate, follower conversion)
3. **Campaign milestones** (launch week, budget alerts)
4. **Routine tasks** (weekly check-ins, thank-yous)

---

## Feature Specifications - MVP

### Main Dashboard View

```
╔═══════════════════════════════════════════════════════╗
║ DASHBOARD                                             ║
╚═══════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────┐
│ YOUR MUSIC HEALTH SCORE: 78 ⭐⭐⭐⭐                │
│ Healthy - Keep up the good work!                    │
│                                                      │
│ [View Details] [What This Means]                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ KEY METRICS (Last 28 Days)                           │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Streams              Monthly Listeners              │
│ 12,450               892                            │
│ +35% ⬆️             +28% ⬆️                        │
│                                                      │
│ Followers            Save Rate                       │
│ 348                  8.1%                           │
│ +12% ⬆️             +0.4% ⬆️                        │
│                                                      │
│ Playlist Adds        Cost Per Stream                │
│ 5 new                $0.063                         │
│ +2 this week ✓      (acceptable)                    │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ INSIGHT CARDS                                        │
├─────────────────────────────────────────────────────┤
│                                                      │
│ 🎉 MOMENTUM ALERT                                   │
│ "Lev Kavu'a" added to "Israeli Indie Gems"         │
│ [View Details]                                      │
│                                                      │
│ 🔥 OPPORTUNITY                                      │
│ Tel Aviv showing 3x listener density                │
│ [Explore]                                           │
│                                                      │
│ [View All Insights (3)]                             │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ ACTIVE CAMPAIGNS                                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│ "Winter EP Release"                                  │
│ Day 15 of 45 | Budget: $147 / $300 (49%)           │
│ Performance: 2,340 streams | $0.063/stream          │
│ Status: On Track ✓                                  │
│                                                      │
│ [View Campaign] [View ROI]                          │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ TOP 3 ACTIONS THIS WEEK                              │
├─────────────────────────────────────────────────────┤
│                                                      │
│ 1. 🎯 Submit to 5 new playlists                     │
│    [Start →]                                        │
│                                                      │
│ 2. 💬 Thank 2 playlist curators                     │
│    [View →]                                         │
│                                                      │
│ 3. 📊 Review campaign budget                        │
│    [Check →]                                        │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ QUICK LINKS                                          │
├─────────────────────────────────────────────────────┤
│                                                      │
│ [Add New Song] [Start Campaign]                     │
│ [Find Playlists] [View Analytics]                   │
│ [Sync Spotify Data]                                 │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Geographic Insights View

```
┌─────────────────────────────────────────────────────┐
│ WHERE YOUR LISTENERS ARE                             │
├─────────────────────────────────────────────────────┤
│                                                      │
│ [Interactive Map - Heatmap of listeners]            │
│                                                      │
│ Top Cities:                                          │
│ 1. Tel Aviv      280 listeners (+35 this week)      │
│ 2. Jerusalem     185 listeners (+19 this week)      │
│ 3. Haifa         142 listeners (+22 this week)      │
│ 4. New York      89 listeners (+8 this week)        │
│ 5. London        67 listeners (+12 this week)       │
│                                                      │
│ 🔥 Hotspot Alert: Tel Aviv                          │
│ 3x higher density than expected. Consider:          │
│ • Booking a show                                    │
│ • Targeting in social ads                           │
│ • Local media outreach                              │
│                                                      │
│ [View Full List] [Export Data]                      │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Data Model

```sql
-- Dashboard Snapshots (daily aggregates for performance)
CREATE TABLE dashboard_snapshots (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    snapshot_date DATE NOT NULL,
    
    -- Aggregate metrics
    total_streams INTEGER DEFAULT 0,
    total_monthly_listeners INTEGER DEFAULT 0,
    total_followers INTEGER DEFAULT 0,
    total_saves INTEGER DEFAULT 0,
    total_playlist_adds INTEGER DEFAULT 0,
    
    -- Calculated metrics
    save_rate DECIMAL(5,2), -- (saves / streams) * 100
    follower_conversion_rate DECIMAL(5,2), -- (followers / monthly_listeners) * 100
    
    -- Health score
    health_score INTEGER, -- 0-100
    
    -- Trends
    streams_vs_last_week_pct DECIMAL(6,2),
    listeners_vs_last_week_pct DECIMAL(6,2),
    followers_vs_last_week_pct DECIMAL(6,2),
    
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, snapshot_date)
);

-- Insights (AI-generated)
CREATE TABLE insights (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    
    insight_type VARCHAR(50) NOT NULL, -- 'momentum', 'warning', 'opportunity', 'tip', 'milestone'
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high'
    
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    action_text VARCHAR(255), -- "Submit to 5 playlists"
    action_link VARCHAR(500), -- Internal link to relevant page
    
    -- Context
    related_song_id UUID REFERENCES songs(id),
    related_campaign_id UUID REFERENCES campaigns(id),
    
    -- Lifecycle
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'dismissed', 'actioned'
    expires_at TIMESTAMP, -- Some insights are time-sensitive
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Weekly Recaps
CREATE TABLE weekly_recaps (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    
    week_start_date DATE NOT NULL,
    week_end_date DATE NOT NULL,
    
    -- Narrative content
    summary_text TEXT NOT NULL,
    
    -- Key stats
    streams_total INTEGER,
    streams_vs_last_week_pct DECIMAL(6,2),
    
    top_performing_song_id UUID REFERENCES songs(id),
    top_performing_song_streams INTEGER,
    
    -- Recommendation
    recommended_action TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Geographic data
CREATE TABLE listener_geography (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    snapshot_date DATE NOT NULL,
    
    city VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    
    listener_count INTEGER DEFAULT 0,
    streams_count INTEGER DEFAULT 0,
    
    -- Growth
    vs_last_week_pct DECIMAL(6,2),
    
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, city, snapshot_date)
);
```

---

## Technical Implementation

### Health Score Calculation

```python
def calculate_health_score(user_data: Dict) -> int:
    """
    Calculate health score (0-100) based on multiple factors
    """
    scores = []
    
    # 1. Streams trend (30% weight)
    streams_trend = user_data['streams_vs_last_week_pct']
    if streams_trend > 20:
        streams_score = 100
    elif streams_trend > 10:
        streams_score = 80
    elif streams_trend > 0:
        streams_score = 60
    elif streams_trend > -10:
        streams_score = 40
    else:
        streams_score = 20
    scores.append(('streams', streams_score, 0.30))
    
    # 2. Save rate (25% weight)
    save_rate = user_data['save_rate']
    if save_rate >= 15:
        save_score = 100
    elif save_rate >= 10:
        save_score = 85
    elif save_rate >= 5:
        save_score = 70
    elif save_rate >= 3:
        save_score = 50
    else:
        save_score = 30
    scores.append(('save_rate', save_score, 0.25))
    
    # 3. Follower conversion (20% weight)
    conversion = user_data['follower_conversion_rate']
    if conversion >= 10:
        conv_score = 100
    elif conversion >= 7:
        conv_score = 85
    elif conversion >= 5:
        conv_score = 70
    elif conversion >= 3:
        conv_score = 50
    else:
        conv_score = 30
    scores.append(('follower_conv', conv_score, 0.20))
    
    # 4. Playlist momentum (15% weight)
    new_playlists = user_data['playlist_adds_last_week']
    if new_playlists >= 5:
        playlist_score = 100
    elif new_playlists >= 3:
        playlist_score = 80
    elif new_playlists >= 1:
        playlist_score = 60
    else:
        playlist_score = 40
    scores.append(('playlists', playlist_score, 0.15))
    
    # 5. Campaign ROI (10% weight)
    cost_per_stream = user_data['cost_per_stream']
    if cost_per_stream <= 0.03:
        roi_score = 100
    elif cost_per_stream <= 0.05:
        roi_score = 80
    elif cost_per_stream <= 0.10:
        roi_score = 60
    else:
        roi_score = 40
    scores.append(('roi', roi_score, 0.10))
    
    # Calculate weighted average
    health_score = sum(score * weight for _, score, weight in scores)
    
    return int(health_score)
```

### Insight Generation Engine

```python
class InsightEngine:
    """
    Generate AI-powered insights based on user data
    """
    
    def generate_insights(self, user_id: str) -> List[Dict]:
        insights = []
        
        data = self.get_user_data(user_id)
        
        # Check for momentum alerts
        new_playlists = self.check_new_playlists(user_id)
        if new_playlists:
            for playlist in new_playlists:
                insights.append({
                    'type': 'momentum',
                    'priority': 'high',
                    'title': f'🎉 Added to "{playlist.name}"',
                    'description': f'{playlist.followers} followers • Added {playlist.hours_ago}h ago',
                    'action': 'Thank curator on Instagram',
                    'link': f'/playlists/{playlist.id}'
                })
        
        # Check for warnings
        if data['streams_vs_yesterday'] < -50:
            playlist_removal = self.check_playlist_removals(user_id)
            if playlist_removal:
                insights.append({
                    'type': 'warning',
                    'priority': 'medium',
                    'title': '⚠️ Stream drop detected',
                    'description': f'Removed from "{playlist_removal.name}" playlist',
                    'action': 'Submit to similar playlists',
                    'link': '/playlists/search'
                })
        
        # Check for opportunities
        hotspot_city = self.detect_geographic_hotspot(user_id)
        if hotspot_city:
            insights.append({
                'type': 'opportunity',
                'priority': 'medium',
                'title': f'🔥 Hotspot: {hotspot_city.name}',
                'description': f'{hotspot_city.listeners} listeners, {hotspot_city.density_multiplier}x expected density',
                'action': 'Explore tour opportunities',
                'link': f'/geography?city={hotspot_city.id}'
            })
        
        # Check for optimization tips
        if data['save_rate'] < 5:
            insights.append({
                'type': 'tip',
                'priority': 'low',
                'title': '💡 Low save rate detected',
                'description': f'Current: {data["save_rate"]}% (Target: 5-10%)',
                'action': 'Learn how to improve',
                'link': '/help/save-rate'
            })
        
        return insights
```

---

## Success Metrics

**Metric 1: Dashboard Engagement**
- Target: 80%+ of users visit dashboard at least weekly
- Measurement: Track daily active users
- Success: Dashboard becomes habit

**Metric 2: Insight Action Rate**
- Target: 40%+ of high-priority insights are actioned
- Measurement: Track "dismissed" vs "actioned" status
- Success: Insights lead to behavior change

**Metric 3: Data Freshness**
- Target: 90%+ of users sync Spotify data at least weekly
- Measurement: Track last_sync timestamp
- Success: Data stays current

**Metric 4: Health Score Improvement**
- Target: 60%+ of users improve health score over 30 days
- Measurement: Compare scores month-over-month
- Success: Tool drives measurable improvement

---

## Questions for Review

1. ✅ **Health Score useful?** Or too abstract?
2. ✅ **Insight cards priorities correct?** Momentum > Warning > Opportunity > Tip?
3. ✅ **Weekly recap valuable?** Or just more noise?
4. ✅ **Geographic insights needed in MVP?** Or Phase 2?
5. ✅ **"Next Best Actions" helpful?** Or overwhelming?

Final component next: Component 6 - Hebrew Social Content Generation! 🎸
