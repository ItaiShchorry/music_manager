from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CreationEntry(Base):
    __tablename__ = "creation_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    opportunity_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("post_opportunities.id", ondelete="SET NULL"), nullable=True
    )

    content_type: Mapped[str] = mapped_column(String(20), nullable=False)
    # 'text' | 'audio' | 'video' | 'image' | 'link'
    text_content: Mapped[str | None] = mapped_column(Text)
    file_url: Mapped[str | None] = mapped_column(String(500))
    external_url: Mapped[str | None] = mapped_column(String(500))
    caption_draft: Mapped[str | None] = mapped_column(Text)

    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    # 'draft' | 'published'

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User", backref="creation_entries")
    opportunity = relationship("PostOpportunity", backref="creation_entries")
