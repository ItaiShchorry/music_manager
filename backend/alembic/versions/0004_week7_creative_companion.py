"""Week 7 schema: Creative Companion — post_opportunities, youtube_briefs, creation_entries, user_progress.

Revision ID: 0004
Revises: 0003
Create Date: 2026-03-06
"""
from alembic import op
import sqlalchemy as sa

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # post_opportunities (was never in a migration, create it now)
    # Includes the Week 7 category field from the start.
    # ------------------------------------------------------------------
    op.create_table(
        "post_opportunities",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("song_id", sa.Integer(), sa.ForeignKey("songs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("hook", sa.Text(), nullable=False),
        sa.Column("why_now", sa.Text(), nullable=False),
        sa.Column("signal_type", sa.String(50), nullable=False),
        sa.Column("category", sa.String(20), nullable=False, server_default="promotion"),
        sa.Column("suggested_platform", sa.String(50), nullable=True),
        sa.Column("hashtag_suggestions", sa.JSON(), nullable=True),
        sa.Column("timing_note", sa.Text(), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="active"),
        sa.Column("remind_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # ------------------------------------------------------------------
    # songs — add search_keywords (JSON) — skip if already present
    # (some databases were set up via create_all and already have it)
    # ------------------------------------------------------------------
    conn = op.get_bind()
    existing_cols = [row[1] for row in conn.execute(sa.text("PRAGMA table_info(songs)")).fetchall()]
    if "search_keywords" not in existing_cols:
        with op.batch_alter_table("songs") as batch_op:
            batch_op.add_column(sa.Column("search_keywords", sa.JSON(), nullable=True))

    # ------------------------------------------------------------------
    # youtube_briefs
    # ------------------------------------------------------------------
    op.create_table(
        "youtube_briefs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("song_id", sa.Integer(), sa.ForeignKey("songs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("concept_type", sa.String(50), nullable=False),
        sa.Column("key_message", sa.Text(), nullable=True),
        sa.Column("context", sa.Text(), nullable=True),
        sa.Column("seo_title", sa.String(100), nullable=True),
        sa.Column("hook_paragraph", sa.Text(), nullable=True),
        sa.Column("chapters", sa.JSON(), nullable=True),
        sa.Column("video_description", sa.Text(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("filmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("youtube_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # ------------------------------------------------------------------
    # youtube_brief_stats
    # ------------------------------------------------------------------
    op.create_table(
        "youtube_brief_stats",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("brief_id", sa.Integer(), sa.ForeignKey("youtube_briefs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("views", sa.Integer(), nullable=True),
        sa.Column("likes", sa.Integer(), nullable=True),
        sa.Column("comments", sa.Integer(), nullable=True),
        sa.Column("subscribers_gained", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("brief_id", "snapshot_date", name="uq_brief_stat_date"),
    )

    # ------------------------------------------------------------------
    # creation_entries
    # ------------------------------------------------------------------
    op.create_table(
        "creation_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("opportunity_id", sa.Integer(), sa.ForeignKey("post_opportunities.id", ondelete="SET NULL"), nullable=True),
        sa.Column("content_type", sa.String(20), nullable=False),
        sa.Column("text_content", sa.Text(), nullable=True),
        sa.Column("file_url", sa.String(500), nullable=True),
        sa.Column("external_url", sa.String(500), nullable=True),
        sa.Column("caption_draft", sa.Text(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # ------------------------------------------------------------------
    # user_progress
    # ------------------------------------------------------------------
    op.create_table(
        "user_progress",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("streak_current", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("streak_best", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_challenge_date", sa.Date(), nullable=True),
        sa.Column("total_completed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("level", sa.String(20), nullable=False, server_default="newcomer"),
        sa.Column("badges", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("user_progress")
    op.drop_table("creation_entries")
    op.drop_table("youtube_brief_stats")
    op.drop_table("youtube_briefs")
    op.drop_table("post_opportunities")

    conn = op.get_bind()
    existing_cols = [row[1] for row in conn.execute(sa.text("PRAGMA table_info(songs)")).fetchall()]
    if "search_keywords" in existing_cols:
        with op.batch_alter_table("songs") as batch_op:
            batch_op.drop_column("search_keywords")
