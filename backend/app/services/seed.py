"""
Seed script for Israeli playlists and radio stations.

Call seed_playlists(db) and seed_radio_stations(db) once at startup
or via a CLI command. Both functions are idempotent — they skip if
the table already has rows.
"""
import logging

from sqlalchemy.orm import Session

from app.models.playlist import Playlist
from app.models.radio_station import RadioStation

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Playlist seed data — 25 Israeli playlists
# ---------------------------------------------------------------------------

PLAYLISTS: list[dict] = [
    # --- Large / Editorial (no direct pitch) ---
    {
        "name": "Top 50 Israel",
        "spotify_id": "37i9dQZEVXbJ6IpvItkgwF",
        "curator_name": "Spotify Editorial",
        "follower_count": 76800,
        "genres": ["pop", "mainstream pop", "hebrew pop"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["upbeat", "popular"],
        "submission_method": None,
        "notes": "Editorial — no direct pitch, submit via Spotify for Artists only",
        "is_active": True,
    },
    {
        "name": "Israeli Hits 2025",
        "spotify_id": "1234israeliHits2025",
        "curator_name": "Eddie T Malakh",
        "curator_contact": "eddie@israelihits.com",
        "follower_count": 14600,
        "genres": ["pop", "hebrew pop", "mainstream"],
        "languages": ["hebrew"],
        "mood_tags": ["upbeat", "energetic"],
        "submission_method": "email",
        "is_active": True,
    },
    {
        "name": "Hot 100 Israel",
        "spotify_id": "hot100israel2025",
        "follower_count": 8200,
        "genres": ["pop", "mainstream pop", "hebrew pop"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["upbeat", "popular"],
        "submission_method": "email",
        "is_active": True,
    },
    {
        "name": "New Music Friday Israel",
        "spotify_id": "37i9dQZF1DX3LDIBRoaCDQ",
        "curator_name": "Spotify Editorial",
        "follower_count": 5100,
        "genres": ["pop", "indie", "alternative", "hebrew pop"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["fresh", "new releases"],
        "submission_method": "spotify_for_artists",
        "notes": "Submit via Spotify for Artists — reviewed weekly",
        "is_active": True,
    },
    # --- Mainstream Hebrew Pop (medium curator) ---
    {
        "name": "הפופ הישראלי",
        "curator_contact": "israelipop@gmail.com",
        "follower_count": 12000,
        "genres": ["hebrew pop", "pop", "mainstream"],
        "languages": ["hebrew"],
        "mood_tags": ["upbeat", "romantic", "popular"],
        "submission_method": "email",
        "is_active": True,
    },
    {
        "name": "Pop Hebrew",
        "follower_count": 8500,
        "genres": ["hebrew pop", "pop"],
        "languages": ["hebrew"],
        "mood_tags": ["upbeat", "feel good"],
        "submission_method": "instagram_dm",
        "is_active": True,
    },
    {
        "name": "Israeli Pop Hits",
        "follower_count": 7300,
        "genres": ["pop", "hebrew pop", "mainstream"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["upbeat", "popular"],
        "submission_method": "email",
        "is_active": True,
    },
    {
        "name": "Best of Israeli Music",
        "follower_count": 6800,
        "genres": ["pop", "hebrew pop", "rock", "indie"],
        "languages": ["hebrew"],
        "mood_tags": ["nostalgic", "upbeat", "popular"],
        "submission_method": "submithub",
        "is_active": True,
    },
    {
        "name": "Chart Israel",
        "follower_count": 5500,
        "genres": ["pop", "mainstream pop", "hebrew pop"],
        "languages": ["hebrew"],
        "mood_tags": ["upbeat", "popular"],
        "submission_method": "email",
        "is_active": True,
    },
    {
        "name": "Israeli Radio Hits",
        "follower_count": 4200,
        "genres": ["pop", "mainstream pop", "hebrew pop", "rock"],
        "languages": ["hebrew"],
        "mood_tags": ["upbeat", "popular"],
        "submission_method": "spotify_for_artists",
        "is_active": True,
    },
    {
        "name": "Galei Tzahal Favorites",
        "follower_count": 3900,
        "genres": ["pop", "rock", "mainstream", "hebrew pop"],
        "languages": ["hebrew"],
        "mood_tags": ["upbeat", "classic"],
        "submission_method": "email",
        "is_active": True,
    },
    {
        "name": "Hebrew Pop 2025",
        "follower_count": 3400,
        "genres": ["hebrew pop", "pop"],
        "languages": ["hebrew"],
        "mood_tags": ["upbeat", "fresh"],
        "submission_method": "submithub",
        "is_active": True,
    },
    # --- Indie / Alternative ---
    {
        "name": "Israeli Indie",
        "spotify_id": "37i9dQZF1DX4SBhb3fqCJd",
        "curator_name": "Spotify Editorial",
        "follower_count": 558,
        "genres": ["indie", "alternative", "indie pop"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["melancholic", "introspective", "chill"],
        "submission_method": "spotify_for_artists",
        "notes": "Sounds of Spotify — editorial, submit via Spotify for Artists",
        "is_active": True,
    },
    {
        "name": "Indie Israel",
        "follower_count": 2100,
        "genres": ["indie", "indie pop", "alternative"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["chill", "introspective", "melancholic"],
        "submission_method": "email",
        "is_active": True,
    },
    {
        "name": "Alternative Israel",
        "follower_count": 1800,
        "genres": ["alternative", "indie", "rock"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["energetic", "introspective"],
        "submission_method": "instagram_dm",
        "is_active": True,
    },
    {
        "name": "Israeli Alt Rock",
        "follower_count": 1400,
        "genres": ["alternative", "rock", "indie rock"],
        "languages": ["hebrew"],
        "mood_tags": ["energetic", "dark"],
        "submission_method": "email",
        "is_active": True,
    },
    # --- Acoustic / Singer-Songwriter ---
    {
        "name": "Israeli Acoustic Sessions",
        "follower_count": 3200,
        "genres": ["acoustic", "singer-songwriter", "folk"],
        "languages": ["hebrew"],
        "mood_tags": ["calm", "introspective", "romantic"],
        "submission_method": "email",
        "is_active": True,
    },
    {
        "name": "Hebrew Singer-Songwriter",
        "follower_count": 2700,
        "genres": ["singer-songwriter", "acoustic", "folk"],
        "languages": ["hebrew"],
        "mood_tags": ["introspective", "melancholic", "romantic"],
        "submission_method": "email",
        "is_active": True,
    },
    {
        "name": "Quiet Israeli Nights",
        "follower_count": 1900,
        "genres": ["acoustic", "ambient", "chill", "singer-songwriter"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["calm", "late night", "melancholic"],
        "submission_method": "instagram_dm",
        "is_active": True,
    },
    {
        "name": "Acoustic Souls Israel",
        "follower_count": 1100,
        "genres": ["acoustic", "singer-songwriter"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["calm", "introspective"],
        "submission_method": "email",
        "is_active": True,
    },
    # --- Cross-genre / Mood ---
    {
        "name": "New Jewish Music",
        "follower_count": 3700,
        "genres": ["pop", "indie", "folk", "world"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["spiritual", "upbeat", "introspective"],
        "submission_method": "email",
        "notes": "Accepts Jewish-themed content across all genres",
        "is_active": True,
    },
    {
        "name": "Late Night Israel",
        "follower_count": 2800,
        "genres": ["pop", "indie", "r&b", "electronic"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["late night", "chill", "melancholic"],
        "submission_method": "submithub",
        "is_active": True,
    },
    {
        "name": "Israeli Soul",
        "follower_count": 2400,
        "genres": ["soul", "r&b", "pop"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["soulful", "romantic", "upbeat"],
        "submission_method": "email",
        "is_active": True,
    },
    {
        "name": "Feel Good Hebrew",
        "follower_count": 1600,
        "genres": ["pop", "hebrew pop", "dance"],
        "languages": ["hebrew"],
        "mood_tags": ["feel good", "upbeat", "happy"],
        "submission_method": "instagram_dm",
        "is_active": True,
    },
    {
        "name": "Road Trip Israel",
        "follower_count": 1300,
        "genres": ["pop", "rock", "indie"],
        "languages": ["hebrew", "english"],
        "mood_tags": ["energetic", "upbeat", "feel good"],
        "submission_method": "email",
        "is_active": True,
    },
]

# ---------------------------------------------------------------------------
# Radio station seed data — 6 Israeli stations
# ---------------------------------------------------------------------------

RADIO_STATIONS: list[dict] = [
    {
        "name": "Galei Tzahal",
        "name_hebrew": "גלי צה\"ל",
        "station_type": "national",
        "website": "https://glz.co.il",
        "genres_focus": ["mainstream pop", "rock", "hip hop", "hebrew pop"],
        "best_for": ["established artists", "chart hits"],
        "submission_guidelines": (
            "Contact music director via official station website. "
            "Most selective — best for established artists with chart potential."
        ),
        "response_time": "4-8 weeks",
        "reach_description": "Largest Israeli radio station — ~1M weekly listeners",
        "notes": "Most selective. New/indie artists have very low acceptance rate.",
    },
    {
        "name": "Kan Gimel",
        "name_hebrew": "כאן גימל",
        "station_type": "national",
        "website": "https://kan.org.il/gimel",
        "genres_focus": ["mainstream pop", "hebrew pop", "mizrahi"],
        "best_for": ["mainstream pop", "chart-oriented artists"],
        "submission_guidelines": (
            "Submit via Kan official submission form on website. "
            "Focus on mainstream Hebrew pop with broad commercial appeal."
        ),
        "response_time": "3-6 weeks",
        "reach_description": "National broadcast — ~600k weekly listeners",
    },
    {
        "name": "Kan 88",
        "name_hebrew": "כאן 88",
        "station_type": "national",
        "contact_email": "88music@kan.org.il",
        "website": "https://kan.org.il/88",
        "genres_focus": ["indie", "alternative", "world music", "indie pop"],
        "best_for": ["new artists", "indie", "alternative", "experimental"],
        "submission_guidelines": (
            "Email MP3 + artist bio + press photo to 88music@kan.org.il. "
            "Most open station for new and indie artists. "
            "Include social media links and a short pitch."
        ),
        "response_time": "2-4 weeks",
        "reach_description": "National broadcast — ~200k weekly listeners, tastemaker audience",
        "notes": "Most new-artist-friendly national station. Actively discovers new talent.",
    },
    {
        "name": "103FM",
        "name_hebrew": "103FM",
        "station_type": "national",
        "website": "https://103fm.maariv.co.il",
        "genres_focus": ["mainstream pop", "rock", "hebrew pop"],
        "best_for": ["mainstream pop", "rock"],
        "submission_guidelines": (
            "Contact music department via website contact form. "
            "Focused on mainstream commercial appeal."
        ),
        "response_time": "4-8 weeks",
        "reach_description": "National broadcast — ~500k weekly listeners",
    },
    {
        "name": "Eco 99FM",
        "name_hebrew": "אקו 99",
        "station_type": "national",
        "website": "https://eco99fm.maariv.co.il",
        "genres_focus": ["pop", "r&b", "electronic", "dance"],
        "best_for": ["pop", "r&b", "dance music"],
        "submission_guidelines": (
            "Submit via website or contact music editor directly. "
            "Leans towards contemporary pop, R&B, and electronic."
        ),
        "response_time": "3-5 weeks",
        "reach_description": "National broadcast — ~350k weekly listeners",
    },
    {
        "name": "Radio Haifa",
        "name_hebrew": "רדיו חיפה",
        "station_type": "regional",
        "website": "https://radiohaifa.co.il",
        "genres_focus": ["indie", "world music", "alternative", "acoustic"],
        "best_for": ["new artists", "indie", "world music", "acoustic"],
        "submission_guidelines": (
            "Email submission to music department via website. "
            "Regional and university-affiliated — very open to new local artists."
        ),
        "response_time": "1-3 weeks",
        "reach_description": "Northern Israel + online streaming — ~80k weekly listeners",
        "notes": "University-affiliated. Great starting point for new artists.",
    },
]


# ---------------------------------------------------------------------------
# Seed functions
# ---------------------------------------------------------------------------

def seed_playlists(db: Session) -> int:
    """Insert playlists if table is empty. Returns number of rows inserted."""
    existing = db.query(Playlist).count()
    if existing > 0:
        logger.info(f"Playlists table already has {existing} rows — skipping seed")
        return 0

    rows = [Playlist(**p) for p in PLAYLISTS]
    db.add_all(rows)
    db.flush()
    logger.info(f"Seeded {len(rows)} playlists")
    return len(rows)


def seed_radio_stations(db: Session) -> int:
    """Insert radio stations if table is empty. Returns number of rows inserted."""
    existing = db.query(RadioStation).count()
    if existing > 0:
        logger.info(f"Radio stations table already has {existing} rows — skipping seed")
        return 0

    rows = [RadioStation(**s) for s in RADIO_STATIONS]
    db.add_all(rows)
    db.flush()
    logger.info(f"Seeded {len(rows)} radio stations")
    return len(rows)
