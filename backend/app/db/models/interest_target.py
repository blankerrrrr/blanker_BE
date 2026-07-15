from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.time import utc_now
from app.db.base import Base


class InterestTarget(Base):
    __tablename__ = "interest_targets"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "type",
            "name",
            name="uk_interest_targets_user_type_name",
        ),
        Index(
            "uk_interest_targets_user_name_ci",
            "user_id",
            text("lower(btrim(name))"),
            unique=True,
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    interest_target_id: Mapped[str | None] = mapped_column(
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
    interest_id: Mapped[str | None] = mapped_column(
        String(64),
        index=True,
        nullable=True,
    )
    type: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(200))
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list)
    keywords: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
