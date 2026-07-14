from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.time import utc_now
from app.db.base import Base


class BlockedItem(Base):
    __tablename__ = "blocked_items"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "interest_target_id",
            "source_url",
            "selector",
            name="uk_blocked_items_user_target_source_selector",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    blocked_item_id: Mapped[str | None] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=True,
    )
    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("users.user_id"),
        index=True,
    )
    analysis_request_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    client_content_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    interest_target_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("interest_targets.interest_target_id"),
        index=True,
        nullable=True,
    )
    summary: Mapped[str] = mapped_column(Text)
    categories: Mapped[list[str]] = mapped_column(JSON, default=list)
    related_topics: Mapped[list[str]] = mapped_column(JSON, default=list)
    source_url: Mapped[str] = mapped_column(Text)
    selector: Mapped[str | None] = mapped_column(Text, nullable=True)
    position_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    found_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
