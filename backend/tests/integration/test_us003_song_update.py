"""
US-003: Update manual song fields via PATCH /api/v1/songs/{id}

Input/output cases defined first (TDD pattern).
"""
import pytest

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------
# (patch_body, field_to_check, expected_value)
PATCH_CASES = [
    # Happy path — update story
    (
        {"story": "This song was written after a long night in Tel Aviv."},
        "story",
        "This song was written after a long night in Tel Aviv.",
    ),
    # Partial update — only mood_tags changed, story stays None
    (
        {"mood_tags": ["melancholic", "dreamy"]},
        "mood_tags",
        ["melancholic", "dreamy"],
    ),
    # Empty body — nothing changes (200 OK)
    (
        {},
        "story",
        None,  # sample_song has no story by default
    ),
]


@pytest.mark.parametrize("body,field,expected", PATCH_CASES)
def test_patch_song_happy(client, auth_headers, sample_song, body, field, expected):
    resp = client.patch(f"/api/v1/songs/{sample_song.id}", json=body, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()[field] == expected


def test_patch_song_partial_does_not_overwrite(client, auth_headers, sample_song, db):
    """Patching mood_tags must not erase an existing story."""
    # First set story via a patch
    r1 = client.patch(
        f"/api/v1/songs/{sample_song.id}",
        json={"story": "Original story"},
        headers=auth_headers,
    )
    assert r1.status_code == 200

    # Now patch only mood_tags
    r2 = client.patch(
        f"/api/v1/songs/{sample_song.id}",
        json={"mood_tags": ["upbeat"]},
        headers=auth_headers,
    )
    assert r2.status_code == 200
    data = r2.json()
    assert data["story"] == "Original story"   # must still be there
    assert data["mood_tags"] == ["upbeat"]


def test_patch_song_requires_auth(client, sample_song):
    resp = client.patch(f"/api/v1/songs/{sample_song.id}", json={"story": "x"})
    assert resp.status_code == 401


def test_patch_song_not_found(client, auth_headers):
    resp = client.patch("/api/v1/songs/99999", json={"story": "x"}, headers=auth_headers)
    assert resp.status_code == 404


def test_patch_song_wrong_user(client, db, sample_song):
    """Another user's token must not be able to patch someone else's song."""
    from app.models.user import User
    from app.utils.auth import create_access_token, hash_password

    other = User(email="other@example.com", hashed_password=hash_password("pw"), name="Other")
    db.add(other)
    db.flush()
    other_token = create_access_token(other.id)
    other_headers = {"Authorization": f"Bearer {other_token}"}

    resp = client.patch(
        f"/api/v1/songs/{sample_song.id}",
        json={"story": "hijack"},
        headers=other_headers,
    )
    assert resp.status_code == 404  # not visible to other user → 404
