"""
US-005: Playlist CRUD endpoints.

  GET /api/v1/playlists                 — list all
  GET /api/v1/playlists?language=hebrew — filter by language
  GET /api/v1/playlists?genre=indie     — filter by genre (word match)
  GET /api/v1/radio-stations            — list all radio stations
"""
import pytest


# ---------------------------------------------------------------------------
# Playlists
# ---------------------------------------------------------------------------

def test_list_playlists_returns_all(client, auth_headers, sample_playlist):
    r = client.get("/api/v1/playlists", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    # Verify shape
    first = data[0]
    assert "id" in first
    assert "name" in first
    assert "genres" in first
    assert "languages" in first


def test_list_playlists_filter_language(client, db, auth_headers):
    """Filter by language= returns only matching playlists."""
    from app.models.playlist import Playlist

    hebrew = Playlist(
        name="Hebrew Only",
        genres=["pop"],
        languages=["hebrew"],
        is_active=True,
    )
    english = Playlist(
        name="English Only",
        genres=["pop"],
        languages=["english"],
        is_active=True,
    )
    db.add_all([hebrew, english])
    db.flush()

    r = client.get("/api/v1/playlists?language=hebrew", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    names = [p["name"] for p in data]
    assert "Hebrew Only" in names
    assert "English Only" not in names


def test_list_playlists_filter_genre(client, db, auth_headers):
    """Filter by genre= returns playlists whose genre list contains the word."""
    from app.models.playlist import Playlist

    indie_pl = Playlist(
        name="Indie Vibes",
        genres=["indie", "alternative"],
        languages=["hebrew"],
        is_active=True,
    )
    pop_pl = Playlist(
        name="Pure Pop",
        genres=["pop", "mainstream pop"],
        languages=["hebrew"],
        is_active=True,
    )
    db.add_all([indie_pl, pop_pl])
    db.flush()

    r = client.get("/api/v1/playlists?genre=indie", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    names = [p["name"] for p in data]
    assert "Indie Vibes" in names
    assert "Pure Pop" not in names


def test_list_playlists_requires_auth(client):
    r = client.get("/api/v1/playlists")
    assert r.status_code == 401


# ---------------------------------------------------------------------------
# Radio stations
# ---------------------------------------------------------------------------

def test_list_radio_stations(client, auth_headers, sample_radio_station):
    r = client.get("/api/v1/radio-stations", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    first = data[0]
    assert "id" in first
    assert "name" in first
    assert "station_type" in first
    assert "genres_focus" in first


def test_list_radio_stations_requires_auth(client):
    r = client.get("/api/v1/radio-stations")
    assert r.status_code == 401
