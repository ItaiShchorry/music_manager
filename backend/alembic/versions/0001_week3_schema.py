"""Week 3 schema: genre/language on songs + playlists, radio_stations, pitch_submissions tables.

Revision ID: 0001
Revises: —
Create Date: 2026-03-03
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # songs — add genre and language columns (nullable, no default needed)
    # ------------------------------------------------------------------
    with op.batch_alter_table("songs") as batch_op:
        batch_op.add_column(sa.Column("genre", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("language", sa.String(50), nullable=True))

    # ------------------------------------------------------------------
    # playlists
    # ------------------------------------------------------------------
    op.create_table(
        "playlists",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("spotify_id", sa.String(100), unique=True, nullable=True),
        sa.Column("curator_name", sa.String(255), nullable=True),
        sa.Column("curator_contact", sa.String(255), nullable=True),
        sa.Column("follower_count", sa.Integer, nullable=True),
        sa.Column("genres", sa.JSON, nullable=True),
        sa.Column("languages", sa.JSON, nullable=True),
        sa.Column("mood_tags", sa.JSON, nullable=True),
        sa.Column("submission_method", sa.String(50), nullable=True),
        sa.Column("submission_guidelines", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )

    # ------------------------------------------------------------------
    # radio_stations
    # ------------------------------------------------------------------
    op.create_table(
        "radio_stations",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("name_hebrew", sa.String(255), nullable=True),
        sa.Column("station_type", sa.String(50), nullable=False),
        sa.Column("contact_email", sa.String(255), nullable=True),
        sa.Column("contact_phone", sa.String(50), nullable=True),
        sa.Column("website", sa.String(255), nullable=True),
        sa.Column("genres_focus", sa.JSON, nullable=True),
        sa.Column("best_for", sa.JSON, nullable=True),
        sa.Column("submission_guidelines", sa.Text, nullable=True),
        sa.Column("response_time", sa.String(100), nullable=True),
        sa.Column("reach_description", sa.String(255), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )

    # ------------------------------------------------------------------
    # pitch_submissions
    # ------------------------------------------------------------------
    op.create_table(
        "pitch_submissions",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("song_id", sa.Integer,
                  sa.ForeignKey("songs.id", ondelete="CASCADE"),
                  nullable=False, index=True),
        sa.Column("target_type", sa.String(20), nullable=False),
        sa.Column("playlist_id", sa.Integer,
                  sa.ForeignKey("playlists.id", ondelete="SET NULL"),
                  nullable=True),
        sa.Column("radio_station_id", sa.Integer,
                  sa.ForeignKey("radio_stations.id", ondelete="SET NULL"),
                  nullable=True),
        sa.Column("pitched_date", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("pitch_method", sa.String(50), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="sent"),
        sa.Column("response_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("response_notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("pitch_submissions")
    op.drop_table("radio_stations")
    op.drop_table("playlists")

    with op.batch_alter_table("songs") as batch_op:
        batch_op.drop_column("language")
        batch_op.drop_column("genre")
