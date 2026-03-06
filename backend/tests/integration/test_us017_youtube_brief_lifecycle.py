"""
US-017: YouTube Brief Lifecycle Management
- PATCH /youtube-briefs/{id} updates status
- filmed_at auto-set when status → filmed
- published_at set and youtube_url required when status → published
- POST /youtube-briefs/{id}/stats — log performance snapshot
- GET /youtube-briefs — list all user briefs (?status= filter)
- GET /youtube-briefs/{id} — get single brief
- DELETE /youtube-briefs/{id} — hard delete 204
"""
import pytest
from datetime import date

from app.models.youtube_brief import YouTubeBrief, YouTubeBriefStat


@pytest.fixture()
def sample_brief(db, sample_song):
    brief = YouTubeBrief(
        user_id=sample_song.user_id,
        song_id=sample_song.id,
        concept_type="making_of",
        seo_title="My Making Of Video",
        status="draft",
    )
    db.add(brief)
    db.flush()
    return brief


# ---------------------------------------------------------------------------
# Status transitions
# ---------------------------------------------------------------------------

def test_patch_draft_to_planned(client, sample_brief, auth_headers):
    resp = client.patch(
        f"/api/v1/youtube-briefs/{sample_brief.id}",
        json={"status": "planned"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "planned"


def test_patch_planned_to_filmed_sets_filmed_at(client, sample_brief, auth_headers):
    # First set to planned
    client.patch(
        f"/api/v1/youtube-briefs/{sample_brief.id}",
        json={"status": "planned"},
        headers=auth_headers,
    )
    resp = client.patch(
        f"/api/v1/youtube-briefs/{sample_brief.id}",
        json={"status": "filmed"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "filmed"
    assert data["filmed_at"] is not None


def test_patch_to_published_requires_youtube_url(client, sample_brief, auth_headers):
    """422 if status=published but no youtube_url."""
    resp = client.patch(
        f"/api/v1/youtube-briefs/{sample_brief.id}",
        json={"status": "published"},
        headers=auth_headers,
    )
    assert resp.status_code == 422


def test_patch_to_published_with_valid_url(client, sample_brief, auth_headers):
    """Sets published_at and saves youtube_url when provided."""
    resp = client.patch(
        f"/api/v1/youtube-briefs/{sample_brief.id}",
        json={
            "status": "published",
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "published"
    assert data["published_at"] is not None
    assert "youtube.com" in data["youtube_url"]


def test_patch_published_invalid_youtube_url(client, sample_brief, auth_headers):
    """422 if youtube_url is provided but not a valid YouTube URL."""
    resp = client.patch(
        f"/api/v1/youtube-briefs/{sample_brief.id}",
        json={
            "status": "published",
            "youtube_url": "https://www.example.com/not-youtube",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

def test_post_stats_snapshot(client, sample_brief, auth_headers):
    """POST /youtube-briefs/{id}/stats logs a performance snapshot."""
    resp = client.post(
        f"/api/v1/youtube-briefs/{sample_brief.id}/stats",
        json={
            "snapshot_date": "2026-03-01",
            "views": 1500,
            "likes": 80,
            "comments": 12,
            "subscribers_gained": 5,
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["views"] == 1500
    assert data["likes"] == 80


def test_post_stats_upsert_duplicate_date(client, sample_brief, auth_headers):
    """POST with same snapshot_date updates rather than creates duplicate."""
    payload = {"snapshot_date": "2026-03-01", "views": 1000}
    client.post(f"/api/v1/youtube-briefs/{sample_brief.id}/stats", json=payload, headers=auth_headers)
    payload["views"] = 2000
    resp = client.post(
        f"/api/v1/youtube-briefs/{sample_brief.id}/stats",
        json=payload,
        headers=auth_headers,
    )
    assert resp.status_code in (200, 201)
    assert resp.json()["views"] == 2000


# ---------------------------------------------------------------------------
# List / Get / Delete
# ---------------------------------------------------------------------------

def test_list_all_user_briefs(client, sample_brief, auth_headers):
    """GET /youtube-briefs returns all briefs for current user."""
    resp = client.get("/api/v1/youtube-briefs", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(b["id"] == sample_brief.id for b in data)


def test_list_briefs_filter_by_status(client, sample_brief, auth_headers):
    """GET /youtube-briefs?status=draft filters correctly."""
    resp = client.get("/api/v1/youtube-briefs?status=draft", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert all(b["status"] == "draft" for b in data)


def test_get_single_brief(client, sample_brief, auth_headers):
    resp = client.get(f"/api/v1/youtube-briefs/{sample_brief.id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == sample_brief.id


def test_delete_brief(client, sample_brief, auth_headers):
    resp = client.delete(f"/api/v1/youtube-briefs/{sample_brief.id}", headers=auth_headers)
    assert resp.status_code == 204
    # Verify gone
    resp2 = client.get(f"/api/v1/youtube-briefs/{sample_brief.id}", headers=auth_headers)
    assert resp2.status_code == 404
