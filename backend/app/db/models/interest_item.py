from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    JSON,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.time import utc_now
from app.db.base import Base


class InterestItemGroup(Base):
    __tablename__ = "interest_item_groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[str | None] = mapped_column(
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
    representative_item_id: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(500))
    summary: Mapped[str] = mapped_column(Text)
    related_topics: Mapped[list[str]] = mapped_column(JSON, default=list)
    duplicate_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )


class InterestItem(Base):
    __tablename__ = "interest_items"
    __table_args__ = (
        UniqueConstraint("user_id", "source_url", name="uk_interest_items_user_source"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    interest_item_id: Mapped[str | None] = mapped_column(
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
    group_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("interest_item_groups.group_id"),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(500))
    summary: Mapped[str] = mapped_column(Text)
    content_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    related_topics: Mapped[list[str]] = mapped_column(JSON, default=list)
    source_url: Mapped[str] = mapped_column(Text)
    selector: Mapped[str | None] = mapped_column(Text, nullable=True)
    duplicate_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 4),
        nullable=True,
    )
    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
