"""
US-003b: PATCH /songs/{id} — genre and language fields.

TDD: write tests first, run red, implement, run green.
"""
import pytest

# ---------------------------------------------------------------------------
# Input / expected output cases
# ---------------------------------------------------------------------------

CASES_GENRE = [
    # (patch_payload, expected_genre, expected_language)
    ({"genre": "mainstream Hebrew pop"}, "mainstream Hebrew pop", None),  # happy path
    ({"genre": "indie rock"}, "indie rock", None),  # different genre
    ({"genre": ""}, "", None),  # empty string allowed
]

CASES_LANGUAGE = [
    ({"language": "hebrew"}, None, "hebrew"),
    ({"language": "english"}, None, "english"),
    ({"language": "both"}, None, "both"),
]

CASES_COMBINED = [
    (
        {"genre": "mainstream Hebrew pop", "language": "hebrew"},
        "mainstream Hebrew pop",
        "hebrew",
    ),
]

CASES_PARTIAL = [
    # Patching genre only should not affect language (stays None)
    ({"genre": "pop"}, "pop", None),
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("payload,expected_genre,expected_language", CASES_GENRE)
def test_patch_genre(client, sample_song, auth_headers, payload, expected_genre, expected_language):
    r = client.patch(f"/api/v1/songs/{sample_song.id}", json=payload, headers=auth_headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["genre"] == expected_genre
    assert data["language"] == expected_language


@pytest.mark.parametrize("payload,expected_genre,expected_language", CASES_LANGUAGE)
def test_patch_language(client, sample_song, auth_headers, payload, expected_genre, expected_language):
    r = client.patch(f"/api/v1/songs/{sample_song.id}", json=payload, headers=auth_headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["genre"] == expected_genre
    assert data["language"] == expected_language


@pytest.mark.parametrize("payload,expected_genre,expected_language", CASES_COMBINED)
def test_patch_genre_and_language(client, sample_song, auth_headers, payload, expected_genre, expected_language):
    r = client.patch(f"/api/v1/songs/{sample_song.id}", json=payload, headers=auth_headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["genre"] == expected_genre
    assert data["language"] == expected_language


@pytest.mark.parametrize("payload,expected_genre,expected_language", CASES_PARTIAL)
def test_patch_genre_does_not_affect_language(client, sample_song, auth_headers, payload, expected_genre, expected_language):
    """Patching only genre should leave language untouched (None by default)."""
    r = client.patch(f"/api/v1/songs/{sample_song.id}", json=payload, headers=auth_headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["genre"] == expected_genre
    assert data["language"] == expected_language


def test_patch_requires_auth(client, sample_song):
    r = client.patch(f"/api/v1/songs/{sample_song.id}", json={"genre": "pop"})
    assert r.status_code == 401


def test_get_song_returns_genre_language(client, sample_song, auth_headers):
    """GET /songs/{id} should include genre and language in response."""
    r = client.get(f"/api/v1/songs/{sample_song.id}", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert "genre" in data
    assert "language" in data
