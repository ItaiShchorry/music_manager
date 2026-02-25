"""
US-002: Parse Spotify track ID from URL or raw ID.

Cases: (input, expected_result)
  - valid URL                → track_id string
  - valid URL with query     → track_id string (stripped)
  - raw 22-char ID           → same ID returned
  - album URL                → ValueError
  - artist URL               → ValueError
  - random garbage           → ValueError
  - empty string             → ValueError
"""
import pytest

from app.services.spotify import parse_spotify_track_id

VALID_CASES = [
    # (input, expected_track_id)
    (
        "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh",
        "4iV5W9uYEdYUVa79Axb7Rh",
    ),
    (
        "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh?si=abc123",
        "4iV5W9uYEdYUVa79Axb7Rh",
    ),
    (
        "spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
        "4iV5W9uYEdYUVa79Axb7Rh",
    ),
    (
        "4iV5W9uYEdYUVa79Axb7Rh",  # raw ID — 22 alphanumeric chars
        "4iV5W9uYEdYUVa79Axb7Rh",
    ),
]

INVALID_CASES = [
    "https://open.spotify.com/album/37i9dQZF1DXcBWIGoYBM5M",  # album URL
    "https://open.spotify.com/artist/4kYSro6naA4h99UJbsxpgj",  # artist URL
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",              # wrong domain
    "not-a-url-or-id",                                           # garbage
    "",                                                           # empty
]


@pytest.mark.parametrize("url,expected", VALID_CASES)
def test_valid_spotify_inputs(url, expected):
    assert parse_spotify_track_id(url) == expected


@pytest.mark.parametrize("bad_input", INVALID_CASES)
def test_invalid_inputs_raise_value_error(bad_input):
    with pytest.raises(ValueError):
        parse_spotify_track_id(bad_input)
