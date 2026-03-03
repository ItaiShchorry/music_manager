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
      - Genre match  : 40 pts
      - Language match: 35 pts
      - Mood overlap : 25 pts max (12 pts per overlapping tag)
    """
    score = 0
    reasons: list[str] = []

    # Genre match (40 pts)
    if song.genre and playlist.genres:
        song_words = set(song.genre.lower().split())
        for pg in playlist.genres:
            if any(w in pg.lower() for w in song_words):
                score += 40
                reasons.append("genre match")
                break

    # Language match (35 pts)
    if song.language and playlist.languages:
        playlist_langs = [lang.lower() for lang in playlist.languages]
        if song.language == "both":
            score += 35
            reasons.append("language match")
        elif song.language in playlist_langs:
            score += 35
            reasons.append("language match")
        elif "both" in playlist_langs:
            score += 20
            reasons.append("partial language match")

    # Mood tag overlap (25 pts max)
    if song.mood_tags and playlist.mood_tags:
        song_moods = {t.lower() for t in song.mood_tags}
        playlist_moods = {t.lower() for t in playlist.mood_tags}
        overlap = len(song_moods & playlist_moods)
        if overlap > 0:
            mood_pts = min(overlap * 12, 25)
            score += mood_pts
            reasons.append("mood match")

    return min(score, 100), reasons


def score_radio_station(song: Song, station: RadioStation) -> tuple[str, bool]:
    """
    Return (label, is_recommended) for a song/station pair.

    Scoring: genre overlap only (simpler — small curated list).
      - 2+ genre words match → "Recommended"
      - 1 genre word match  → "Secondary"
      - 0 matches           → "Low match"
    """
    if not song.genre or not station.genres_focus:
        return "Low match", False

    song_words = set(song.genre.lower().split())
    overlap_count = sum(
        1 for sg in station.genres_focus
        if any(w in sg.lower() for w in song_words)
    )

    if overlap_count >= 2:
        return "Recommended", True
    if overlap_count == 1:
        return "Secondary", False
    return "Low match", False
