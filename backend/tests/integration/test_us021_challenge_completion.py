"""
US-021: Challenge Completion Flow
- POST /challenges/{opportunity_id}/complete → 201, CreationEntry saved
- POST /uploads → 201, file_url returned
- Completing challenge marks opportunity as 'used'
- UserProgress created on first completion
- 404 if opportunity not found / not owned
- 401 if unauthenticated
"""
import io
import pytest

from app.models.post_opportunity import PostOpportunity
from app.models.creation_entry import CreationEntry
from app.models.user_progress import UserProgress


@pytest.fixture()
def active_opportunity(db, sample_user, sample_song):
    opp = PostOpportunity(
        user_id=sample_user.id,
        song_id=sample_song.id,
        hook="Write a verse about longing",
        why_now="Your catalog focuses on longing",
        signal_type="lyric_prompt",
        category="creative",
        status="active",
    )
    db.add(opp)
    db.flush()
    return opp


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_complete_challenge_text(client, active_opportunity, auth_headers, db):
    """POST /challenges/{id}/complete with text_content creates CreationEntry."""
    resp = client.post(
        f"/api/v1/challenges/{active_opportunity.id}/complete",
        json={
            "content_type": "text",
            "text_content": "בלילה שקט / הכל נגמר / רק הזיכרון נשאר",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["content_type"] == "text"
    assert "בלילה שקט" in data["text_content"]
    assert data["opportunity_id"] == active_opportunity.id


def test_complete_challenge_marks_opportunity_used(client, active_opportunity, auth_headers, db):
    """Completing a challenge sets opportunity status to 'used'."""
    client.post(
        f"/api/v1/challenges/{active_opportunity.id}/complete",
        json={"content_type": "text", "text_content": "Some lyrics"},
        headers=auth_headers,
    )
    db.expire(active_opportunity)
    opp = db.query(PostOpportunity).filter(PostOpportunity.id == active_opportunity.id).first()
    assert opp.status == "used"


def test_complete_challenge_creates_user_progress(client, active_opportunity, auth_headers, db, sample_user):
    """First challenge completion creates UserProgress record."""
    client.post(
        f"/api/v1/challenges/{active_opportunity.id}/complete",
        json={"content_type": "text", "text_content": "Some lyrics"},
        headers=auth_headers,
    )
    progress = db.query(UserProgress).filter(UserProgress.user_id == sample_user.id).first()
    assert progress is not None
    assert progress.total_completed >= 1


def test_complete_challenge_404_not_found(client, auth_headers):
    """404 when opportunity_id does not exist."""
    resp = client.post(
        "/api/v1/challenges/99999/complete",
        json={"content_type": "text", "text_content": "Hello"},
        headers=auth_headers,
    )
    assert resp.status_code == 404


def test_complete_challenge_401_unauthenticated(client, active_opportunity):
    """401 when no auth token."""
    resp = client.post(
        f"/api/v1/challenges/{active_opportunity.id}/complete",
        json={"content_type": "text", "text_content": "Hello"},
    )
    assert resp.status_code == 401


def test_list_creations(client, active_opportunity, auth_headers, db, sample_user):
    """GET /challenges returns user's creation entries."""
    entry = CreationEntry(
        user_id=sample_user.id,
        opportunity_id=active_opportunity.id,
        content_type="text",
        text_content="Test lyrics",
        status="draft",
    )
    db.add(entry)
    db.flush()

    resp = client.get("/api/v1/challenges", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_upload_file(client, auth_headers):
    """POST /uploads accepts a multipart file and returns file_url."""
    file_content = b"fake audio content"
    resp = client.post(
        "/api/v1/uploads",
        files={"file": ("test_audio.webm", io.BytesIO(file_content), "audio/webm")},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "file_url" in data
    assert data["file_url"].endswith("test_audio.webm") or "uploads" in data["file_url"]
