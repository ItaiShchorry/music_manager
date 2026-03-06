"""
US-018: SEO Search Keywords on Song
- search_keywords field on Song model
- PATCH /songs/{id} accepts search_keywords list
- GET /songs/{id} returns search_keywords
- Empty list normalised to null
"""
import pytest

# ---------------------------------------------------------------------------
# CASES — (patch_body, expected_search_keywords)
# ---------------------------------------------------------------------------

CASES = [
    # happy path: set keywords
    (
        {"search_keywords": ["songs about moving on", "Hebrew music for heartbreak"]},
        ["songs about moving on", "Hebrew music for heartbreak"],
    ),
    # single keyword
    (
        {"search_keywords": ["indie Israeli pop"]},
        ["indie Israeli pop"],
    ),
    # empty list → null
    (
        {"search_keywords": []},
        None,
    ),
]


@pytest.mark.parametrize("patch_body, expected", CASES)
def test_patch_search_keywords(client, sample_song, auth_headers, patch_body, expected):
    resp = client.patch(
        f"/api/v1/songs/{sample_song.id}",
        json=patch_body,
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["search_keywords"] == expected


def test_get_song_includes_search_keywords(client, sample_song, auth_headers, db):
    """GET /songs/{id} returns search_keywords field."""
    from app.models.song import Song
    song = db.query(Song).filter(Song.id == sample_song.id).first()
    song.search_keywords = ["melancholic Hebrew indie"]
    db.commit()

    resp = client.get(f"/api/v1/songs/{sample_song.id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["search_keywords"] == ["melancholic Hebrew indie"]


def test_search_keywords_not_set_returns_null(client, sample_song, auth_headers):
    """Song with no search_keywords returns null."""
    resp = client.get(f"/api/v1/songs/{sample_song.id}", headers=auth_headers)
    assert resp.status_code == 200
    # Default is null (not set on sample_song fixture)
    assert resp.json()["search_keywords"] is None
