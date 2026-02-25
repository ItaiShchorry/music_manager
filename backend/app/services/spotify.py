import logging
import re
from urllib.parse import urlparse

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.config import settings

logger = logging.getLogger(__name__)

# 22-character Spotify base62 ID
_TRACK_ID_RE = re.compile(r"^[A-Za-z0-9]{22}$")


def parse_spotify_track_id(url_or_id: str) -> str:
    """
    Accept any of:
      - https://open.spotify.com/track/<id>
      - https://open.spotify.com/track/<id>?si=...
      - spotify:track:<id>
      - raw 22-char ID

    Returns the track ID string.
    Raises ValueError for anything else.
    """
    s = url_or_id.strip()

    if not s:
        raise ValueError("Empty input")

    # spotify URI
    if s.startswith("spotify:track:"):
        track_id = s.split(":")[-1]
        if _TRACK_ID_RE.match(track_id):
            return track_id
        raise ValueError(f"Invalid track ID in URI: {s!r}")

    # URL
    if s.startswith("http"):
        parsed = urlparse(s)
        if parsed.netloc != "open.spotify.com":
            raise ValueError(f"Not a Spotify URL: {s!r}")
        parts = parsed.path.strip("/").split("/")
        if len(parts) < 2 or parts[0] != "track":
            raise ValueError(f"Not a track URL (got {parts[0]!r}): {s!r}")
        track_id = parts[1]
        if _TRACK_ID_RE.match(track_id):
            return track_id
        raise ValueError(f"Invalid track ID in URL: {s!r}")

    # Raw ID
    if _TRACK_ID_RE.match(s):
        return s

    raise ValueError(f"Cannot parse Spotify track ID from: {s!r}")


class SpotifyService:
    def __init__(self):
        auth = SpotifyClientCredentials(
            client_id=settings.spotify_client_id,
            client_secret=settings.spotify_client_secret,
        )
        self._sp = spotipy.Spotify(auth_manager=auth)

    def get_track_metadata(self, track_id: str) -> dict:
        logger.info(f"Fetching Spotify track: {track_id}")
        track = self._sp.track(track_id)
        logger.debug(f"Spotify response for {track_id}: {track}")

        release_date = track["album"].get("release_date")

        return {
            "spotify_track_id": track["id"],
            "title": track["name"],
            "artist_name": ", ".join(a["name"] for a in track["artists"]),
            "album_name": track["album"]["name"],
            "release_date": release_date,
            "duration_ms": track["duration_ms"],
            "spotify_url": track["external_urls"].get("spotify"),
            "album_image_url": (
                track["album"]["images"][0]["url"] if track["album"]["images"] else None
            ),
            "popularity": track["popularity"],
        }
