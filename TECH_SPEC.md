# Technical Specifications
## Israeli Indie Music Promotion Tool

**Version:** 1.0  
**Date:** [To be filled]  
**Status:** Draft  
**Based on:** PRD v1.0

---

## Instructions for Creation

**This document should be created using Claude Code Teams AFTER PRD is complete:**

1. Provide PRD.md and all 6 component design documents
2. Ask the team (CEO, PM, Frontend Dev, Backend Dev, AI Specialist) to translate product requirements into technical specifications
3. Focus on: architecture, data models, APIs, algorithms, infrastructure
4. Review and iterate until all technical details are clear

---

## Document Structure (To Be Filled)

### 1. System Architecture

#### 1.1 High-Level Architecture
```
[Diagram or description to be created by team]

User Browser
    ↓
Frontend (React SPA)
    ↓
Backend API (FastAPI)
    ↓
Database (PostgreSQL)
    ↓
External Services (Spotify, Anthropic)
```

#### 1.2 Component Architecture
- Backend modules and their interactions
- Frontend structure and routing
- Service layer organization
- Data flow patterns

#### 1.3 Technology Stack

**Backend:**
- Language: Python 3.11+
- Framework: FastAPI 0.104+
- ORM: SQLAlchemy 2.0+
- Database: PostgreSQL 15+
- Migration: Alembic
- Async: asyncio, aiohttp

**Frontend:**
- Language: TypeScript 5.0+
- Framework: React 18+
- Build Tool: Vite 5.0+
- Styling: TailwindCSS 3.3+
- State Management: TanStack Query v5
- Routing: React Router v6
- Forms: React Hook Form + Zod

**DevOps:**
- Containerization: Docker
- CI/CD: GitHub Actions (or similar)
- Hosting: TBD (Railway/Render/DigitalOcean)
- Monitoring: Sentry (errors), Posthog (analytics)

---

### 2. Data Models

#### 2.1 Database Schema

**Users Table**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    spotify_user_id VARCHAR(255),
    spotify_access_token TEXT,
    spotify_refresh_token TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

**Songs Table**
```sql
-- (Full schema from component_01_smart_song_profile.md)
CREATE TABLE songs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    -- [All fields from design doc]
    ...
);
```

_[Continue with all other tables from component designs]_

#### 2.2 Data Relationships
- ER diagram
- Foreign key constraints
- Cascade delete rules

#### 2.3 Indexes
- Primary indexes
- Performance indexes
- Unique constraints

---

### 3. API Specifications

#### 3.1 Authentication Endpoints

**POST /api/auth/register**
```json
Request:
{
    "email": "artist@example.com",
    "password": "SecurePass123!",
    "full_name": "Artist Name"
}

Response: 201 Created
{
    "user": {
        "id": "uuid",
        "email": "artist@example.com",
        "full_name": "Artist Name"
    },
    "access_token": "jwt.token.here",
    "token_type": "bearer"
}

Errors:
- 400: Invalid email/password format
- 409: Email already exists
```

_[Continue with all other endpoints]_

#### 3.2 API Design Patterns
- RESTful principles
- Pagination strategy (cursor-based or offset)
- Filtering and sorting conventions
- Error response format (RFC 7807)

#### 3.3 Rate Limiting
- Per endpoint limits
- User tier limits (if applicable)
- Rate limit headers

---

### 4. Business Logic

#### 4.1 Health Score Calculation
```python
def calculate_health_score(data: UserMetrics) -> int:
    """
    Calculate health score (0-100) from:
    - Streams trend (30% weight)
    - Save rate (25% weight)  
    - Follower conversion (20% weight)
    - Playlist momentum (15% weight)
    - Campaign ROI (10% weight)
    
    Algorithm details in component_05 design doc.
    """
    # Implementation details
    pass
```

#### 4.2 Budget Pacing Algorithm
```python
def check_budget_pacing(campaign: Campaign) -> BudgetAlert:
    """
    Alert if:
    - 80% of budget spent
    - Spending 15%+ ahead of expected pace
    
    Algorithm details in component_04 design doc.
    """
    # Implementation details
    pass
```

#### 4.3 Content Generation Prompts
```python
def build_content_prompt(
    song: Song,
    tone: str,
    platform: str,
    language: str
) -> str:
    """
    Build Claude prompt for social content generation.
    
    Full prompt templates in component_06 design doc.
    """
    # Implementation details
    pass
```

---

### 5. External Service Integrations

#### 5.1 Spotify Web API

**Authentication Flow:**
1. User clicks "Connect Spotify"
2. Redirect to Spotify OAuth: `/api/spotify/auth`
3. Spotify redirects back: `/api/spotify/callback?code=...`
4. Exchange code for access token
5. Store tokens in database

**Key Endpoints Used:**
- `GET /v1/search` - Search tracks
- `GET /v1/tracks/{id}` - Get track details
- `GET /v1/audio-features/{id}` - Get audio features
- `GET /v1/artists/{id}` - Get artist info

**Rate Limits:**
- 100 requests per 30 seconds
- Implement exponential backoff
- Cache responses (1 hour TTL)

**Error Handling:**
- 401: Refresh token and retry
- 429: Backoff and queue request
- 5xx: Retry up to 3 times

#### 5.2 Anthropic API

**Model:** claude-sonnet-4-20250514

**Content Generation:**
```python
response = await client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2000,
    messages=[{
        "role": "user",
        "content": prompt
    }]
)
```

**Token Management:**
- Estimate tokens before request
- Track usage per user/day
- Implement limits (e.g., 10 generations/day for free tier)

**Cost Optimization:**
- Cache common prompts
- Use smaller model for simple tasks
- Batch requests when possible

---

### 6. Security Specifications

#### 6.1 Authentication & Authorization
- JWT with RS256 signing
- Token expiry: 7 days
- Refresh token flow
- RBAC (if multi-user teams in Phase 2)

#### 6.2 Data Protection
- Passwords: bcrypt (cost factor 12)
- Sensitive data: Encrypted at rest
- API keys: Environment variables
- CORS: Whitelist frontend origin

#### 6.3 Input Validation
- Pydantic models for request validation
- SQL injection prevention (parameterized queries)
- XSS prevention (sanitize HTML output)
- File upload validation (type, size)

---

### 7. Performance Requirements

#### 7.1 Response Time Targets
- API endpoints: < 500ms (p95)
- Database queries: < 100ms (p95)
- Frontend page load: < 2s (LCP)
- AI content generation: < 10s

#### 7.2 Optimization Strategies
- Database indexing
- Query optimization (avoid N+1)
- Frontend code splitting
- Image optimization (WebP, lazy loading)
- CDN for static assets

#### 7.3 Caching Strategy
- API responses: Redis (if needed)
- Static assets: Browser cache (1 year)
- Database queries: Application-level cache (15 min)

---

### 8. Infrastructure

#### 8.1 Development Environment
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Database
docker run -d -p 5432:5432 \
  -e POSTGRES_DB=music_promo_dev \
  postgres:15
```

#### 8.2 Production Environment
- Containerized deployment (Docker)
- Database: Managed PostgreSQL
- Secrets: Environment variables
- SSL/TLS: Let's Encrypt
- Monitoring: Sentry + logs

#### 8.3 CI/CD Pipeline
```yaml
# Example GitHub Actions workflow
on: [push]
jobs:
  test:
    - Run linter
    - Run tests
    - Check migrations
  deploy:
    - Build Docker image
    - Push to registry
    - Deploy to hosting
```

---

### 9. Testing Strategy

#### 9.1 Backend Testing
- Unit tests: pytest
- Integration tests: TestClient (FastAPI)
- Database tests: Test database
- API tests: Postman/Thunder Client

#### 9.2 Frontend Testing
- Unit tests: Vitest
- Component tests: React Testing Library
- E2E tests: Playwright
- Visual regression: Percy (optional)

#### 9.3 Test Coverage Targets
- Backend: 80%+ coverage
- Frontend: 70%+ coverage
- Critical paths: 100% coverage

---

### 10. Monitoring & Observability

#### 10.1 Logging
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Centralized logging (if multi-server)
- Log rotation (daily, keep 30 days)

#### 10.2 Metrics
- Request rate (per endpoint)
- Response times (p50, p95, p99)
- Error rates (4xx, 5xx)
- Database connection pool
- AI token usage

#### 10.3 Alerting
- API error rate > 5%
- Database connection failures
- Disk space < 20%
- Memory usage > 80%

---

### 11. Deployment

#### 11.1 Deployment Checklist
- [ ] Run all tests
- [ ] Run database migrations
- [ ] Update environment variables
- [ ] Build production assets
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Run smoke tests
- [ ] Monitor for errors

#### 11.2 Rollback Plan
- Keep previous Docker image
- Database migration rollback script
- Feature flags for risky changes
- Blue-green deployment (Phase 2)

---

### 12. Scalability Considerations

#### 12.1 Current Design (MVP)
- Supports: 100 concurrent users
- Database: Single instance
- Backend: Single server
- Frontend: Static hosting

#### 12.2 Future Scaling (Phase 2+)
- Load balancer for backend
- Database read replicas
- Redis for caching/sessions
- CDN for frontend assets
- Background job queue (Celery/RQ)

---

### 13. Open Technical Questions

_To be resolved during TECH_SPEC creation:_
- Which hosting provider? (Railway vs Render vs DigitalOcean)
- Real-time features? (WebSockets for live updates)
- File storage? (Local vs S3 for images/receipts)
- Analytics service? (Posthog vs Mixpanel vs custom)

---

## Approval Sign-Off

- [ ] Backend Developer - Architecture approved
- [ ] Frontend Developer - Implementation feasible
- [ ] AI Specialist - AI integration viable
- [ ] DevOps/Infrastructure - Deployable
- [ ] Security Review - Security measures adequate

**Created by:** Claude Code Teams  
**Reviewed by:** [Your name]  
**Approved on:** [Date]

---

## Next Steps After Approval

1. Set up Claude Code hooks (`.claude/hooks/`)
2. Initialize project structure
3. Begin Phase 1: Foundation implementation
