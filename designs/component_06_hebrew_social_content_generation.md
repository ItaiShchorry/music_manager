# Component Design: Hebrew Social Content Generation

## Document Version: 1.0
## Date: February 7, 2026
## Status: Ready for Review - FINAL MVP 1 COMPONENT! 🎉

---

## Executive Summary

**Purpose:** Generate professional, culturally-appropriate Hebrew social media content (Instagram, Facebook, TikTok) for song promotion with one click.

**Core Challenge:** Writing consistent, engaging Hebrew content is time-consuming and requires both language fluency and marketing expertise. Most Israeli indie artists struggle with:
- Writer's block
- Consistent posting
- Hebrew marketing language (not everyday Hebrew)
- Platform-specific best practices

**MVP Approach:**
- Claude-powered content generation
- Templates for common post types (new release, behind-the-scenes, show announcement)
- Hebrew + English bilingual support
- Instagram/Facebook/TikTok optimized
- Save/reuse successful posts

**Phase 2 Enhancement:**
- Image generation (DALL-E integration)
- Video scripts
- Story sequences
- Hashtag research
- Posting schedule AI

**MVP Deliverable:** One-click content generator producing ready-to-post Hebrew captions with hashtags, emojis, and platform-specific formatting.

---

## Research: Best Practices

### Finding #1: Hebrew Social Media Landscape
**Source:** Israeli social media statistics + influencer research

**Platform Usage in Israel:**
1. **Instagram:** Most popular for musicians (visual + music)
2. **Facebook:** Still strong, especially 25+ demographic
3. **TikTok:** Growing rapidly among younger audiences
4. **X/Twitter:** Less relevant for music promotion

**Hebrew Language Nuances:**
- **Formal vs Informal:** Israeli social media skews VERY informal
- **Slang Integration:** Natural use of "אחלה" (achla), "יופי" (yofi), "בטח" (betach) builds authenticity
- **RTL Formatting:** Proper right-to-left, but emojis/hashtags flow LTR
- **Hebrew-English Mix:** Common to include English words in Hebrew posts ("single חדש")

**Cultural Considerations:**
- **Shabbat Awareness:** Posts scheduled Friday evening through Saturday evening get lower engagement (people offline)
- **Community Focus:** Israeli culture values community, collaboration > individual achievement
- **Authenticity >> Polish:** Overly produced content feels fake. Raw, genuine posts perform better

### Finding #2: Optimal Caption Length by Platform
**Source:** Social media best practices 2024

**Instagram:**
- Sweet spot: 125-150 characters (Hebrew or English)
- Long-form acceptable but breaks needed (use .\n\n. trick)
- First 2 lines CRITICAL (before "more")

**Facebook:**
- 40-80 characters for high engagement
- Can go longer (150+) for storytelling

**TikTok:**
- VERY short: 50-100 characters
- Hook in first 5 words
- Focus on trends/challenges

**Implementation:**
Generate platform-specific versions automatically

### Finding #3: Music Promotion Post Types
**Source:** Successful indie artist social media analysis

**Essential Post Types:**
1. **New Release Announcement** (40% of content)
2. **Behind-the-Scenes** (20%) - studio, writing process
3. **Show Announcements** (10%)
4. **Personal/Storytelling** (15%) - why you wrote the song
5. **Engagement** (15%) - questions, polls, "what should I write about?"

**Posting Frequency:**
- **Growing (0-10K):** 4-5x/week minimum
- **Established (10K+):** 3-4x/week

---

## My Original Ideas 💡

### Claude Suggestion #1: "Content Variants" - Same Message, Different Styles

**Problem:** One-size-fits-all captions don't work. Different followers respond to different tones.

**Solution:** Generate 3-5 variants of each post in different tones, let user pick.

**Example:**

```
User Input:
- Song: "Lev Kavu'a"
- Post Type: New Release Announcement
- Key Message: Out now on Spotify

Generated Variants:

🎭 VARIANT 1: Emotional/Vulnerable
┌─────────────────────────────────────────────────────┐
│ HEBREW:                                              │
│ "לב קפוא" בחוץ עכשיו 💔                             │
│                                                      │
│ כתבתי את השיר הזה בתקופה הכי קשה שעברתי.            │
│ כשהרגשתי שאני לא יכול להרגיש יותר כלום.             │
│                                                      │
│ אם אתם עוברים משהו דומה - אתם לא לבד.              │
│                                                      │
│ 🎧 לינק בביו                                        │
│ #מוזיקהישראלית #אינדי #שיר_חדש #לב_קפוא            │
│                                                      │
│ ENGLISH:                                             │
│ "Frozen Heart" out now 💔                           │
│                                                      │
│ I wrote this during my darkest time.                │
│ When I felt completely numb.                        │
│                                                      │
│ If you're going through something similar -        │
│ you're not alone.                                   │
│                                                      │
│ 🎧 Link in bio                                      │
│ #IsraeliMusic #Indie #NewSong                       │
└─────────────────────────────────────────────────────┘

🎉 VARIANT 2: Excited/Energetic
┌─────────────────────────────────────────────────────┐
│ HEBREW:                                              │
│ אחלה של יום! 🔥                                     │
│                                                      │
│ "לב קפוא" החדש שלי סוף סוף בחוץ!                   │
│ פעם ראשונה שאני משתף שיר כל כך אישי.                │
│                                                      │
│ שמעתי? תגידו לי מה אתם חושבים! ⬇️                   │
│                                                      │
│ 🎧 Spotify בלינק בביו                               │
│ #מוזיקה_חדשה #אינדי_ישראלי #single_חדש            │
│                                                      │
│ ENGLISH:                                             │
│ What a day! 🔥                                      │
│                                                      │
│ My new single "Frozen Heart" is finally out!       │
│ First time sharing something this personal.         │
│                                                      │
│ Did you listen? Tell me what you think! ⬇️          │
│                                                      │
│ 🎧 Spotify link in bio                              │
│ #NewMusic #IndieIsrael #NewSingle                   │
└─────────────────────────────────────────────────────┘

💬 VARIANT 3: Conversational/Casual
┌─────────────────────────────────────────────────────┐
│ HEBREW:                                              │
│ אז זהו, "לב קפוא" בחוץ 🎵                           │
│                                                      │
│ שיר שכתבתי בחורף. על ניתוק רגשי.                   │
│ על הרגע שאתה מרגיש קפוא מבפנים.                     │
│                                                      │
│ גם אם שיר אחד אתם מתחברים אליו - די לי.            │
│                                                      │
│ יאללה, תשמעו 🎧                                     │
│ #מוזיקה_ישראלית #אינדי #לב_קפוא                    │
│                                                      │
│ ENGLISH:                                             │
│ So yeah, "Frozen Heart" is out 🎵                   │
│                                                      │
│ A song I wrote in winter. About emotional numbness. │
│ About that moment when you feel frozen inside.      │
│                                                      │
│ If even one of you connects with it - that's enough.│
│                                                      │
│ Go listen 🎧                                        │
│ #IsraeliMusic #Indie #FrozenHeart                   │
└─────────────────────────────────────────────────────┘

Select your favorite variant to post!
```

**Tone Options:**
- Emotional/Vulnerable
- Excited/Energetic
- Conversational/Casual
- Poetic/Artistic
- Humorous/Playful (when appropriate)

### Claude Suggestion #2: "Story Behind the Song" Generator

**Problem:** The most engaging posts tell stories, but artists struggle to articulate their creative process.

**Solution:** Interview-style prompts that extract compelling stories, then format them beautifully.

**Flow:**

```
┌─────────────────────────────────────────────────────┐
│ STORY BEHIND "LEV KAVU'A"                            │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Answer a few quick questions:                       │
│                                                      │
│ 1. Where were you when you wrote this?              │
│    [בסטודיו הביתי, בשעות הקטנות של הלילה]           │
│                                                      │
│ 2. What was happening in your life?                 │
│    [עברתי גירושין קשים, הייתי בתקופה אפלה]         │
│                                                      │
│ 3. What do you want listeners to feel?              │
│    [שהם לא לבד בכאב. שזה בסדר להרגיש ככה]          │
│                                                      │
│ 4. Any interesting production details?              │
│    [הקלטתי בטייק אחד, רציתי שזה ירגיש גולמי]       │
│                                                      │
│ [Generate Story Post]                               │
└─────────────────────────────────────────────────────┘

Generated Post:
┌─────────────────────────────────────────────────────┐
│ הסיפור מאחורי "לב קפוא" 💔                          │
│                                                      │
│ כתבתי את השיר הזה בסטודיו הביתי, שלוש בלילה.       │
│ כמה חודשים אחרי שהתגרשתי. התקופה הכי אפלה של החיים. │
│                                                      │
│ הקלטתי את זה בטייק אחד. רציתי שהשיר ירגיש גולמי,   │
│ ללא ליטושים. כי ככה הרגשתי - פצוע, פתוח, לא מוכן.   │
│                                                      │
│ אם אתם עוברים משהו דומה - אני רוצה שתדעו:          │
│ אתם לא לבד בכאב.                                    │
│ זה בסדר להרגיש ככה.                                 │
│                                                      │
│ 🎧 "לב קפוא" בחוץ עכשיו. לינק בביו.                │
│                                                      │
│ #מוזיקה_ישראלית #אינדי #סיפור_אישי                  │
└─────────────────────────────────────────────────────┘
```

**Value:** Transforms generic announcements into compelling narratives.

### Claude Suggestion #3: "Smart Hashtag Mix" - Hebrew + English

**Problem:** Should hashtags be Hebrew or English? Most Israeli posts use both, but finding the right mix is hard.

**Solution:** Automated hashtag strategy based on research and current trends.

**Strategy:**

```
Hashtag Mix Formula (Instagram):
- 3-5 Hebrew hashtags (local discovery)
- 3-5 English hashtags (international reach)
- 1-2 genre tags (#אינדי #indie)
- 1 song/campaign tag (#לב_קפוא)

Total: 8-12 hashtags (optimal range)

Example for "Lev Kavu'a":
HEBREW TAGS:
#מוזיקה_ישראלית (Israeli music - broad)
#אינדי_ישראלי (Israeli indie - niche)
#שיר_חדש (new song - timing)
#מוזיקה_מקורית (original music)

ENGLISH TAGS:
#IsraeliMusic
#IndieMusic
#NewMusic2026
#AlternativeRock

CAMPAIGN TAG:
#לב_קפוא

AUTO-RESEARCHED TRENDING:
#musicfromisrael (currently trending)
```

### Claude Suggestion #4: "Post Series Generator"

**Problem:** One-off posts don't build momentum. Need coordinated series.

**Solution:** Generate entire post series for a release (announcement, countdown, launch, follow-up).

**Example Series:**

```
RELEASE SERIES: "Lev Kavu'a"
Campaign Duration: 7 days

┌─────────────────────────────────────────────────────┐
│ POST 1: TEASER (Day -7)                              │
├─────────────────────────────────────────────────────┤
│ משהו חדש בדרך 👀                                    │
│ שיר שכתבתי בתקופה קשה. יוצא בשבוע הבא.              │
│ תהיו מוכנים 🎵                                      │
│ #בקרוב #מוזיקה_חדשה                                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ POST 2: BEHIND-THE-SCENES (Day -5)                   │
├─────────────────────────────────────────────────────┤
│ [תמונה: באולפן]                                     │
│ בסטודיו, לילה 3.                                    │
│ הקלטנו את "לב קפוא" בטייק אחד.                     │
│ לפעמים הכאב הכי גולמי הוא הכי אמיתי.                │
│ יוצא בעוד שלושה ימים 💔                             │
│ #מאחורי_הקלעים #באולפן                              │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ POST 3: STORY BEHIND (Day -2)                        │
├─────────────────────────────────────────────────────┤
│ [Use "Story Behind Song" generator from Suggestion #2]
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ POST 4: RELEASE DAY (Day 0)                          │
├─────────────────────────────────────────────────────┤
│ [Use "Content Variants" from Suggestion #1]
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ POST 5: THANK YOU (Day +2)                           │
├─────────────────────────────────────────────────────┤
│ תודה ענקית לכל מי שהאזין ל"לב קפוא" 🙏             │
│ כבר 2,000 השמעות ביומיים! לא מאמין.                 │
│                                                      │
│ עוד לא שמעתם? הלינק בביו 🎧                         │
│ #תודה #מוזיקה_ישראלית                               │
└─────────────────────────────────────────────────────┘

[Schedule All] [Customize] [Preview]
```

---

## Feature Specifications - MVP

### Content Generator Interface

```
╔═══════════════════════════════════════════════════════╗
║ GENERATE SOCIAL CONTENT                               ║
╚═══════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────┐
│ STEP 1: SELECT POST TYPE                             │
├─────────────────────────────────────────────────────┤
│                                                      │
│ ○ New Release Announcement                          │
│ ○ Behind-the-Scenes / Studio                        │
│ ○ Show/Event Announcement                           │
│ ○ Story Behind the Song                             │
│ ○ Engagement Post (Question/Poll)                   │
│ ○ Thank You / Milestone                             │
│ ○ Custom (Write Your Own Prompt)                    │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ STEP 2: SONG & DETAILS                               │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Song: [Lev Kavu'a ▾]                                │
│                                                      │
│ Key Message:                                         │
│ [Out now on Spotify]                                │
│                                                      │
│ Context (optional):                                  │
│ [Wrote during difficult time, recorded in one take]│
│                                                      │
│ Call-to-Action:                                      │
│ ○ Listen now (default)                              │
│ ○ Pre-save                                          │
│ ○ Buy tickets                                       │
│ ○ Follow for more                                   │
│ ○ Comment below                                     │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ STEP 3: PLATFORMS & TONE                             │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Platforms (auto-optimized for each):                │
│ ☑ Instagram                                         │
│ ☑ Facebook                                          │
│ ☐ TikTok                                            │
│                                                      │
│ Language:                                            │
│ ● Hebrew + English (recommended)                    │
│ ○ Hebrew only                                       │
│ ○ English only                                      │
│                                                      │
│ Generate Variants:                                   │
│ ☑ Emotional/Vulnerable                              │
│ ☑ Excited/Energetic                                 │
│ ☑ Conversational/Casual                             │
│ ☐ Poetic/Artistic                                   │
│ ☐ Humorous/Playful                                  │
│                                                      │
│ [Generate Content ✨]                               │
│                                                      │
└─────────────────────────────────────────────────────┘

Generating... ⏳
[Progress bar with fun messages]
"כותב את הקפשן המושלם..."
"מוסיף אמוג'י..."
"בוחר האשטאגים הנכונים..."
```

### Generated Content Display

```
╔═══════════════════════════════════════════════════════╗
║ YOUR GENERATED CONTENT                                 ║
╚═══════════════════════════════════════════════════════╝

Generated 3 variants for Instagram

┌─────────────────────────────────────────────────────┐
│ VARIANT 1: EMOTIONAL/VULNERABLE ⭐ Most Popular     │
├─────────────────────────────────────────────────────┤
│                                                      │
│ 📱 INSTAGRAM (145 chars - optimal)                  │
│                                                      │
│ "לב קפוא" בחוץ עכשיו 💔                             │
│                                                      │
│ כתבתי את השיר הזה בתקופה הכי קשה שעברתי.            │
│ כשהרגשתי שאני לא יכול להרגיש יותר כלום.             │
│                                                      │
│ אם אתם עוברים משהו דומה - אתם לא לבד.              │
│                                                      │
│ 🎧 לינק בביו                                        │
│                                                      │
│ #מוזיקהישראלית #אינדי #שיר_חדש #לב_קפוא            │
│ #IsraeliMusic #Indie #NewSong                       │
│                                                      │
│ ────────────────────────────────────                 │
│                                                      │
│ 📘 FACEBOOK (75 chars - high engagement)            │
│                                                      │
│ "לב קפוא" החדש שלי בחוץ 💔                          │
│ שיר על ניתוק רגשי בתקופה קשה.                      │
│                                                      │
│ 🎧 תשמעו בלינק: [Spotify link]                     │
│                                                      │
│ #מוזיקה_ישראלית #שיר_חדש                            │
│                                                      │
│ [Copy Caption] [Edit] [Share to Clipboard]         │
│                                                      │
└─────────────────────────────────────────────────────┘

[View Variant 2: Excited/Energetic]
[View Variant 3: Conversational/Casual]

[Save to Library] [Schedule Post] [Generate More]
```

### Hebrew-Specific Features

**1. RTL Text Handling**
```javascript
// Automatic RTL detection and formatting
function formatHebrewCaption(text) {
    return `<div dir="rtl" lang="he">${text}</div>`;
}

// Mixed Hebrew-English handling
// Hebrew text flows RTL
// Hashtags, URLs, emojis flow LTR naturally
```

**2. Cultural Context Prompts**
```python
# Claude system prompt includes:
cultural_context = """
You are writing for the Israeli indie music scene. Key considerations:
- Tone should be informal and authentic (like talking to friends)
- Use natural Hebrew slang where appropriate ("אחלה", "יאללה", "בטח")
- Avoid overly formal language
- Community > individual achievement (we did this vs I did this)
- Shabbat awareness (don't schedule posts Friday eve - Saturday eve)
- Mix Hebrew and English naturally (common in Israeli social media)
"""
```

---

## Data Model

```sql
-- Generated Content Library
CREATE TABLE generated_content (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    song_id UUID REFERENCES songs(id),
    
    post_type VARCHAR(100) NOT NULL, -- 'release', 'bts', 'story', etc.
    platform VARCHAR(50) NOT NULL, -- 'instagram', 'facebook', 'tiktok'
    
    language VARCHAR(20) NOT NULL, -- 'hebrew', 'english', 'bilingual'
    tone VARCHAR(50), -- 'emotional', 'excited', 'casual', etc.
    
    caption_hebrew TEXT,
    caption_english TEXT,
    hashtags TEXT[],
    
    character_count INTEGER,
    
    -- Usage tracking
    times_used INTEGER DEFAULT 0,
    last_used_at TIMESTAMP,
    
    -- User feedback
    rating INTEGER, -- 1-5 stars
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Content Templates (pre-built)
CREATE TABLE content_templates (
    id UUID PRIMARY KEY,
    
    template_name VARCHAR(255) NOT NULL,
    template_category VARCHAR(100), -- 'release', 'bts', 'story', etc.
    
    prompt_template TEXT NOT NULL, -- Claude prompt with variables
    
    example_output_hebrew TEXT,
    example_output_english TEXT,
    
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Saved Content (user's library)
CREATE TABLE saved_content (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    generated_content_id UUID REFERENCES generated_content(id),
    
    custom_label VARCHAR(255), -- User's custom name
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Technical Implementation

### Content Generation Service

```python
# /backend/services/content_generation_service.py

class HebrewContentGenerator:
    """
    Generate Hebrew social media content using Claude
    """
    
    def __init__(self, anthropic_client):
        self.client = anthropic_client
    
    async def generate_variants(
        self,
        song: Song,
        post_type: str,
        key_message: str,
        context: str,
        tones: List[str],
        platforms: List[str],
        language: str = "bilingual"
    ) -> List[Dict]:
        """
        Generate multiple content variants
        """
        
        variants = []
        
        for tone in tones:
            prompt = self._build_prompt(
                song, post_type, key_message, 
                context, tone, language
            )
            
            response = await self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            content = self._parse_response(response.content[0].text)
            
            # Generate platform-specific versions
            for platform in platforms:
                optimized = self._optimize_for_platform(content, platform)
                variants.append({
                    'tone': tone,
                    'platform': platform,
                    'content': optimized
                })
        
        return variants
    
    def _build_prompt(
        self, song, post_type, key_message, 
        context, tone, language
    ) -> str:
        """
        Build Claude prompt with context
        """
        
        base_prompt = f"""
        You are a social media expert for Israeli indie musicians. 
        
        TASK: Write a {post_type} post for Instagram.
        
        SONG DETAILS:
        - Title: {song.title} ({song.title_english})
        - Genre: {song.primary_genre}
        - Mood: {', '.join(song.mood_tags)}
        - Story: {song.story_behind_song[:200]}...
        
        KEY MESSAGE: {key_message}
        ADDITIONAL CONTEXT: {context}
        
        TONE: {tone}
        LANGUAGE: {language}
        
        REQUIREMENTS:
        1. If bilingual, write Hebrew first, then English
        2. Keep Hebrew text 125-150 characters for Instagram
        3. Use informal, authentic Hebrew (like talking to friends)
        4. Include natural Hebrew slang where appropriate
        5. Mix Hebrew and English hashtags (3-5 each)
        6. Add relevant emojis
        7. Include call-to-action (🎧 link in bio)
        8. Format with proper spacing and line breaks
        
        CULTURAL CONTEXT:
        - Israeli indie scene values authenticity over polish
        - Community-focused language (we > I)
        - Avoid overly formal Hebrew
        
        OUTPUT FORMAT:
        HEBREW:
        [Hebrew caption here]
        
        [Hashtags in Hebrew]
        
        ENGLISH:
        [English caption here]
        
        [Hashtags in English]
        """
        
        return base_prompt
    
    def _optimize_for_platform(self, content: Dict, platform: str) -> Dict:
        """
        Platform-specific optimization
        """
        
        if platform == "instagram":
            # Already optimized
            return content
            
        elif platform == "facebook":
            # Shorter version
            return {
                'hebrew': content['hebrew'][:150],
                'english': content['english'][:150],
                'hashtags': content['hashtags'][:5]  # Fewer hashtags
            }
            
        elif platform == "tiktok":
            # Very short, hook-focused
            return {
                'hebrew': content['hebrew'][:100],
                'english': content['english'][:100],
                'hashtags': content['hashtags'][:3]
            }
        
        return content
```

---

## Success Metrics

**Metric 1: Generation Usage**
- Target: 70%+ of users generate content at least once per song
- Measurement: Track generation API calls
- Success: Feature is adopted

**Metric 2: Variant Selection Distribution**
- Target: All tones used (not just one preferred)
- Measurement: Track which variants users choose
- Success: Options are valuable

**Metric 3: Content Reuse**
- Target: 40%+ of generated content is saved/reused
- Measurement: Track saves and reposts
- Success: Quality is high

**Metric 4: Time Savings**
- Target: 80%+ users report it saves time
- Measurement: User survey
- Success: Clear value prop

---

## Questions for Review

1. ✅ **Variant system useful?** Or just pick one tone?
2. ✅ **Hebrew slang appropriate?** Or too casual?
3. ✅ **Story generator needed in MVP?** Or save for Phase 2?
4. ✅ **Post series generator priority?** Or individual posts first?
5. ✅ **Image generation needed?** Or text-only MVP?

---

## 🎉 MVP 1 COMPLETE! 

All 6 components designed:
1. ✅ Smart Song Profile
2. ✅ Israeli Playlist & Radio Discovery
3. ✅ SubmitHub Integration
4. ✅ Campaign & Budget Management
5. ✅ Dashboard + Insights Engine
6. ✅ Hebrew Social Content Generation

**Total estimated implementation:** 6-8 weeks for MVP 1
**Next step:** Review all components and build! 🚀
