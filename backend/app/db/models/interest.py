from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.time import utc_now
from app.db.base import Base


class Interest(Base):
    __tablename__ = "interests"
    __table_args__ = (
        UniqueConstraint("title", "genre", name="uk_interests_title_genre"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    interest_id: Mapped[str | None] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(200))
    genre: Mapped[str] = mapped_column(String(100))
    image_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
