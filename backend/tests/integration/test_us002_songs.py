"""
US-002 / US-003: Song CRUD — create, list, get, delete.

All Spotify API calls are mocked so tests run offline.
"""
from unittest.mock import MagicMock, patch

import pytest

# Mocked Spotify metadata returned by SpotifyService.get_track_metadata()
MOCK_SPOTIFY_DATA = {
    "spotify_track_id": "4iV5W9uYEdYUVa79Axb7Rh",
    "title": "Test Song",
    "artist_name": "Test Artist",
    "album_name": "Test Album",
    "release_date": "2024-01-15",
    "duration_ms": 210000,
    "spotify_url": "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh",
    "album_image_url": "https://i.scdn.co/image/abc123",
    "popularity": 65,
}

CREATE_SONG_PAYLOAD = {
    "spotify_url": "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh",
    "story": "This song is about late nights in Tel Aviv.",
    "mood_tags": ["melancholic", "urban"],
    "themes": ["loneliness", "city life"],
    "comparable_artists": ["Idan Raichel", "Static & Ben El"],
}


class TestCreateSong:
    def test_create_song_happy_path(self, client, auth_headers):
        with patch("app.api.songs.SpotifyService") as MockSpotify:
            mock_instance = MagicMock()
            mock_instance.get_track_metadata.return_value = MOCK_SPOTIFY_DATA
            MockSpotify.return_value = mock_instance

            resp = client.post("/api/v1/songs", json=CREATE_SONG_PAYLOAD, headers=auth_headers)

        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Test Song"
        assert data["spotify_track_id"] == "4iV5W9uYEdYUVa79Axb7Rh"
        assert data["story"] == CREATE_SONG_PAYLOAD["story"]
        assert "id" in data

    def test_create_song_unauthenticated(self, client):
        resp = client.post("/api/v1/songs", json=CREATE_SONG_PAYLOAD)
        assert resp.status_code == 401

    def test_create_song_invalid_spotify_url(self, client, auth_headers):
        payload = {**CREATE_SONG_PAYLOAD, "spotify_url": "https://youtube.com/watch?v=abc"}
        resp = client.post("/api/v1/songs", json=payload, headers=auth_headers)
        assert resp.status_code == 422

    def test_create_song_duplicate_track_id_returns_409(self, client, auth_headers, sample_song):
        # sample_song fixture already added the same track
        with patch("app.api.songs.SpotifyService") as MockSpotify:
            mock_instance = MagicMock()
            mock_instance.get_track_metadata.return_value = MOCK_SPOTIFY_DATA
            MockSpotify.return_value = mock_instance

            resp = client.post("/api/v1/songs", json=CREATE_SONG_PAYLOAD, headers=auth_headers)

        assert resp.status_code == 409


class TestListSongs:
    def test_list_songs_returns_own_songs(self, client, auth_headers, sample_song):
        resp = client.get("/api/v1/songs", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(s["id"] == sample_song.id for s in data)

    def test_list_songs_unauthenticated(self, client):
        resp = client.get("/api/v1/songs")
        assert resp.status_code == 401


class TestGetSong:
    def test_get_song_by_id(self, client, auth_headers, sample_song):
        resp = client.get(f"/api/v1/songs/{sample_song.id}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == sample_song.id

    def test_get_nonexistent_song_returns_404(self, client, auth_headers):
        resp = client.get("/api/v1/songs/99999", headers=auth_headers)
        assert resp.status_code == 404


class TestDeleteSong:
    def test_delete_song(self, client, auth_headers, sample_song):
        resp = client.delete(f"/api/v1/songs/{sample_song.id}", headers=auth_headers)
        assert resp.status_code == 204

        # Confirm gone
        get_resp = client.get(f"/api/v1/songs/{sample_song.id}", headers=auth_headers)
        assert get_resp.status_code == 404

    def test_delete_nonexistent_returns_404(self, client, auth_headers):
        resp = client.delete("/api/v1/songs/99999", headers=auth_headers)
        assert resp.status_code == 404
