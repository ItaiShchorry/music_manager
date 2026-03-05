"""Week 4 schema: add generated_content table.

Revision ID: 0002
Revises: 0001
Create Date: 2026-03-04
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "generated_content",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("song_id", sa.Integer(), sa.ForeignKey("songs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("post_type", sa.String(100), nullable=False),
        sa.Column("platform", sa.String(50), nullable=False),
        sa.Column("tone", sa.String(50), nullable=False),
        sa.Column("caption_hebrew", sa.Text(), nullable=True),
        sa.Column("caption_english", sa.Text(), nullable=True),
        sa.Column("hashtags", sa.JSON(), nullable=True),
        sa.Column("character_count", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("generated_content")
