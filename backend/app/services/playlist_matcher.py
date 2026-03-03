"""
Match algorithm: score songs against playlists and radio stations.
"""
from app.models.playlist import Playlist
from app.models.radio_station import RadioStation
from app.models.song import Song


def score_playlist(song: Song, playlist: Playlist) -> tuple[int, list[str]]:
    """
    Return (score 0-100, reasons list) for a song/playlist pair.

    Scoring breakdown:
      - Genre match  : 40 pts — at least one word from song.genre appears as a
                                whole word in any of the playlist's genre tags
      - Language match: 35 pts (20 pts if the playlist covers "both")
      - Mood overlap : up to 25 pts (12 pts per overlapping tag, capped at 25)
    """
    score = 0
    reasons: list[str] = []

    # Genre match (40 pts)
    # Split both sides into word sets and check for any intersection.
    # "pop" vs "hip hop" → {"pop"} ∩ {"hip","hop"} = ∅  — no false positive.
    # "pop" vs "hebrew pop" → {"pop"} ∩ {"hebrew","pop"} = {"pop"} — match.
    if song.genre and playlist.genres:
        song_words = set(song.genre.lower().split())
        for pg in playlist.genres:
            pg_words = set(pg.lower().split())
            if song_words & pg_words:
                score += 40
                reasons.append("genre match")
                break

    # Language match (35 pts)
    # Normalise song.language to lowercase to handle any capitalisation stored
    # via direct API calls (the UI enforces lowercase, the API currently does not).
    if song.language and playlist.languages:
        song_lang = song.language.lower()
        playlist_langs = [lang.lower() for lang in playlist.languages]
        if song_lang == "both":
            score += 35
            reasons.append("language match")
        elif song_lang in playlist_langs:
            score += 35
            reasons.append("language match")
        elif "both" in playlist_langs:
            score += 20
            reasons.append("partial language match")

    # Mood tag overlap (25 pts max, 12 pts per overlapping tag)
    if song.mood_tags and playlist.mood_tags:
        song_moods = {t.lower() for t in song.mood_tags}
        playlist_moods = {t.lower() for t in playlist.mood_tags}
        overlap = len(song_moods & playlist_moods)
        if overlap > 0:
            score += min(overlap * 12, 25)
            reasons.append("mood match")

    return min(score, 100), reasons


def score_radio_station(song: Song, station: RadioStation) -> tuple[str, bool]:
    """
    Return (label, is_recommended) for a song/station pair.

    Uses the same word-set intersection logic as score_playlist.
      - 2+ genre tags match → "Recommended"
      - 1 genre tag matches → "Secondary"
      - 0 matches           → "Low match"
    """
    if not song.genre or not station.genres_focus:
        return "Low match", False

    song_words = set(song.genre.lower().split())
    overlap_count = sum(
        1 for sg in station.genres_focus
        if song_words & set(sg.lower().split())
    )

    if overlap_count >= 2:
        return "Recommended", True
    if overlap_count == 1:
        return "Secondary", False
    return "Low match", False
