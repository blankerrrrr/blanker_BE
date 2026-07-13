from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.time import utc_now
from app.db.base import Base


class BlockSetting(Base):
    __tablename__ = "block_settings"
    __table_args__ = (
        UniqueConstraint("user_id", "category", name="uk_block_settings_user_category"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block_setting_id: Mapped[str | None] = mapped_column(
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
    category: Mapped[str] = mapped_column(String(20))
    enabled: Mapped[bool] = mapped_column(Boolean)
    sensitivity: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
