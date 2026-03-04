"""Week 5 schema: add campaigns, campaign_songs, expenses, submithub_campaigns, submithub_submissions.

Revision ID: 0003
Revises: 0002
Create Date: 2026-03-05
"""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "campaigns",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("release_type", sa.String(50), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("budget_total", sa.Numeric(10, 2), nullable=False),
        sa.Column("budget_spent", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("primary_goal", sa.String(100), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="planning"),
        sa.Column("budget_recommendation", sa.JSON(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "campaign_songs",
        sa.Column("campaign_id", sa.Integer(), sa.ForeignKey("campaigns.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("song_id", sa.Integer(), sa.ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("campaign_id", sa.Integer(), sa.ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("expense_date", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("subcategory", sa.String(100), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "submithub_campaigns",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("song_id", sa.Integer(), sa.ForeignKey("songs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("campaign_id", sa.Integer(), sa.ForeignKey("campaigns.id", ondelete="SET NULL"), nullable=True),
        sa.Column("campaign_code", sa.String(50), unique=True, nullable=False),
        sa.Column("budget_allocated", sa.Numeric(10, 2), nullable=True),
        sa.Column("curator_count", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="active"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "submithub_submissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("submithub_campaign_id", sa.Integer(), sa.ForeignKey("submithub_campaigns.id", ondelete="CASCADE"), nullable=False),
        sa.Column("curator_name", sa.String(255), nullable=False),
        sa.Column("curator_genre_focus", sa.JSON(), nullable=True),
        sa.Column("curator_approval_rate", sa.Float(), nullable=True),
        sa.Column("submission_date", sa.Date(), nullable=True),
        sa.Column("cost", sa.Numeric(5, 2), nullable=False, server_default="3.00"),
        sa.Column("response_status", sa.String(50), nullable=False, server_default="pending"),
        sa.Column("response_date", sa.Date(), nullable=True),
        sa.Column("curator_feedback", sa.Text(), nullable=True),
        sa.Column("playlist_added", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("playlist_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("submithub_submissions")
    op.drop_table("submithub_campaigns")
    op.drop_table("expenses")
    op.drop_table("campaign_songs")
    op.drop_table("campaigns")
