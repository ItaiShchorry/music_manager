# Claude Code Instructions - Music Promotion Tool

## Project Information

**Git Repository:** [Your repo URL here]

**Project Type:** Full-stack web application for Israeli indie music promotion

**Tech Stack:**
- Backend: Python 3.11+, FastAPI, PostgreSQL, SQLAlchemy
- Frontend: React 18, TypeScript, Vite, TailwindCSS
- AI: Anthropic Python SDK, Claude Sonnet 4

---

## Core Working Principles

### Code Quality Standards

1. **Keep Code Clean:**
   - Follow DRY (Don't Repeat Yourself) principle
   - If code is used more than once, extract to a function or separate file
   - Remove orphaned/dead code immediately after changes
   - Use meaningful variable and function names
   - Add comments for complex logic only (code should be self-documenting)

2. **Temporary Files:**
   - ALL test files, experiments, and temporary code go in `/tmp` directory
   - Never commit files from `/tmp` (already in .gitignore)
   - Clean up `/tmp` after finishing experiments

3. **Code Reusability:**
   - If a code block is used 2+ times → extract to function
   - If a function is used across files → move to `/utils` or `/services`
   - Create shared components in `/components/common` for frontend

### Documentation Updates

**CRITICAL:** After any significant code change, update the following files:
- `STATUS.md` - Current project state, what works, what doesn't
- This file (`Claude.md`) - If you discover a new pattern or mistake to avoid

### Reference Documents

Always consult these before starting work:
- `/docs/component_01_smart_song_profile.md` - Song profile system
- `/docs/component_02_israeli_playlist_radio_discovery.md` - Playlist discovery
- `/docs/component_03_submithub_integration.md` - SubmitHub features
- `/docs/component_04_campaign_budget_management.md` - Campaign & budget
- `/docs/component_05_dashboard_insights_engine.md` - Dashboard & insights
- `/docs/component_06_hebrew_social_content_generation.md` - Hebrew content generation
- `PRD.md` - Product requirements
- `TECH_SPEC.md` - Technical specifications
- `STATUS.md` - Current project status

---

## Git Workflow

### Protected Branches
- `main` - Production branch (NO direct commits)
- Always work on feature branches: `feature/[component-name]`

### Commit Strategy
- Commit frequently (after each logical unit of work)
- Use conventional commit format: `type(scope): description`
  - `feat(songs): add Spotify search integration`
  - `fix(dashboard): correct health score calculation`
  - `docs(readme): update installation instructions`
  - `refactor(api): extract auth middleware`

### Before Every Commit
- Run code formatter
- Run code review hook
- Run `pytest tests/ -v` — ALL tests must be green. No exceptions.

---

## Development Practices

### Logging (CRITICAL for AI projects)

**Always include comprehensive logging:**
- Log all API calls (request + response)
- Log all database operations
- Log all external service calls (Spotify, Anthropic)
- Log errors with full stack traces
- Save logs to `/logs` directory with rotation

Example:
```python
import logging

logger = logging.getLogger(__name__)

# Log important operations
logger.info(f"Fetching Spotify track: {track_id}")
logger.debug(f"API response: {response.json()}")
logger.error(f"Failed to fetch track: {str(e)}", exc_info=True)
```

### Test-Driven Development (MANDATORY)

**Every User Story must follow this cycle — no exceptions:**

```
1. READ   the US acceptance criteria in PRD.md
2. WRITE  the test file with input/output tuples BEFORE any implementation
3. RUN    pytest → tests MUST FAIL (red) to confirm they're real tests
4. BUILD  the implementation
5. RUN    pytest → tests MUST PASS (green)
6. COMMIT tests + implementation together
```

**Test file naming:** `test_us{number}_{short_description}.py`
- Maps 1:1 to User Story numbers in PRD.md
- Lives in `backend/tests/unit/` (pure logic) or `backend/tests/integration/` (DB + HTTP)

**Input/output tuple pattern — define cases FIRST:**
```python
# Each test file starts with explicit cases before any test function
CASES = [
    (input_1, expected_output_1),   # happy path
    (input_2, expected_output_2),   # edge case
    (input_3, expected_output_3),   # error/invalid input
]

@pytest.mark.parametrize("input, expected", CASES)
def test_feature(input, expected):
    assert my_function(input) == expected
```

**Minimum cases per test:**
- 1 happy path (valid, typical input)
- 1+ edge cases (boundary values, empty, None)
- 1 invalid/error case (bad input → correct error response)

**Claude API calls in tests:** Always mock the Anthropic client. Never make real API calls in tests.

**Running tests:**
```powershell
# From backend/ directory
pytest tests/ -v                    # all tests
pytest tests/ -k "us008" -v         # one user story
pytest tests/unit/ -v               # unit tests only
```

**Before every commit:** All tests must be green. A failing test blocks the commit.

### Database Migrations

- Always create migration for schema changes: `alembic revision --autogenerate -m "description"`
- Never modify old migrations
- Test migrations up AND down

---

## Component-Specific Guidelines

### Component 1: Smart Song Profile
- Spotify API rate limits: max 100 requests/30 seconds
- Always validate Spotify track_id before storing
- Manual entry fields: story, mood_tags, themes, comparable_artists

### Component 5: Dashboard Health Score
- Recalculate health score daily (cron job or manual trigger)
- Weight formula: streams(30%) + save_rate(25%) + follower_conv(20%) + playlists(15%) + ROI(10%)

### Component 6: Hebrew Content Generation
- Use Claude Sonnet 4 model: `claude-sonnet-4-20250514`
- Always generate 3 tone variants minimum
- Character limits: Instagram 125-150, Facebook 40-80, TikTok 50-100
- Mix Hebrew + English hashtags (3-5 each)

---

## Common Patterns

### API Endpoint Structure
```python
@router.post("/songs", response_model=SongResponse)
async def create_song(
    song: SongCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Creating song for user {current_user.id}")
    # Implementation
```

### Frontend Data Fetching
```typescript
// Use TanStack Query
const { data, isLoading, error } = useQuery({
  queryKey: ['songs'],
  queryFn: fetchSongs,
})
```

### Error Handling
```python
try:
    result = await spotify_service.get_track(track_id)
except SpotifyAPIError as e:
    logger.error(f"Spotify API error: {e}")
    raise HTTPException(status_code=502, detail="Spotify service unavailable")
```

---

## Lessons Learned / Corrections

_This section will be updated as we discover patterns and fix mistakes_

### Date: [Add dates as you update]

**Issue:** [What went wrong]
**Correction:** [How to do it properly]
**Context:** [Why this matters]

---

## Search & Research

Before implementing a new feature:
1. Search the web for best practices
2. Check if similar features exist in component design docs
3. Review existing code for similar patterns
4. Ask clarifying questions before starting

---

## Notes

- Hebrew text requires RTL support: use `dir="rtl" lang="he"` 
- Israeli timezone: Asia/Jerusalem (UTC+2/+3 with DST)
- Currency: USD for international services, ILS for display
- Always test with Hebrew content (don't just use English)

## Windows Development Notes

This project is developed on **Windows**. Key things to keep in mind:

- **Shell:** Use PowerShell, not CMD. All commands in docs assume PowerShell.
- **Paths:** Use backslashes (`\`) or forward slashes (`/`) — Node.js and Python handle both.
- **No chmod:** Hook scripts are invoked with `node <script>` explicitly — no execute permissions needed.
- **Line endings:** Run this once after cloning: `git config core.autocrlf true`
- **mkdir:** Use `mkdir .claude\hooks` or `New-Item -ItemType Directory -Path ".claude\hooks"`
- **Python venv:** Activate with `.venv\Scripts\Activate.ps1` (not `source .venv/bin/activate`)
- **Temp dir:** Use project-local `tmp\` folder, NOT Windows system `%TEMP%` — it's already in `.gitignore`

