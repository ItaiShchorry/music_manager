"""Health score calculator for the dashboard."""
from typing import Optional


def calculate_health_score(
    streams_vs_last_week_pct: Optional[float],
    save_rate: Optional[float],
    follower_conversion_rate: Optional[float],
    total_playlist_adds: Optional[int],
    cost_per_stream: Optional[float],
) -> int:
    """Return health score (0-100) as weighted average of 5 components."""

    # 1. Streams trend (30%)
    trend = streams_vs_last_week_pct or 0.0
    if trend > 20:
        streams_score = 100
    elif trend > 10:
        streams_score = 80
    elif trend > 0:
        streams_score = 60
    elif trend > -10:
        streams_score = 40
    else:
        streams_score = 20

    # 2. Save rate (25%)
    sr = save_rate or 0.0
    if sr >= 15:
        save_score = 100
    elif sr >= 10:
        save_score = 85
    elif sr >= 5:
        save_score = 70
    elif sr >= 3:
        save_score = 50
    else:
        save_score = 30

    # 3. Follower conversion (20%)
    conv = follower_conversion_rate or 0.0
    if conv >= 10:
        conv_score = 100
    elif conv >= 7:
        conv_score = 85
    elif conv >= 5:
        conv_score = 70
    elif conv >= 3:
        conv_score = 50
    else:
        conv_score = 30

    # 4. Playlist adds last week (15%)
    adds = total_playlist_adds or 0
    if adds >= 5:
        playlist_score = 100
    elif adds >= 3:
        playlist_score = 80
    elif adds >= 1:
        playlist_score = 60
    else:
        playlist_score = 40

    # 5. Campaign ROI — cost per stream (10%)
    cps = cost_per_stream
    if cps is None:
        roi_score = 60  # neutral when no campaign data
    elif cps <= 0.03:
        roi_score = 100
    elif cps <= 0.05:
        roi_score = 80
    elif cps <= 0.10:
        roi_score = 60
    else:
        roi_score = 40

    raw = (
        streams_score * 0.30
        + save_score * 0.25
        + conv_score * 0.20
        + playlist_score * 0.15
        + roi_score * 0.10
    )
    return int(round(raw))


def health_label(score: int) -> str:
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Healthy"
    elif score >= 50:
        return "Needs Work"
    return "Critical"
