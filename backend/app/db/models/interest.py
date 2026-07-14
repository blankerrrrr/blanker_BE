from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.time import utc_now
from app.db.base import Base


class InterestCatalog(Base):
    __tablename__ = "interest_catalog"
    __table_args__ = (
        UniqueConstraint("name", name="uk_interest_catalog_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
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

    interests: Mapped[list["Interest"]] = relationship(back_populates="catalog")


class Interest(Base):
    __tablename__ = "interests"
    __table_args__ = (
        UniqueConstraint(
            "interest_catalog_id",
            "title",
            name="uk_interests_catalog_title",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    interest_id: Mapped[str | None] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=True,
    )
    interest_catalog_id: Mapped[int] = mapped_column(
        ForeignKey("interest_catalog.id"),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str | None] = mapped_column(String(250), nullable=True)
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

    catalog: Mapped[InterestCatalog] = relationship(back_populates="interests")
    genre_mappings: Mapped[list["InterestGenreMapping"]] = relationship(
        back_populates="interest",
        cascade="all, delete-orphan",
    )


class InterestGenre(Base):
    __tablename__ = "interest_genres"
    __table_args__ = (
        UniqueConstraint("name", name="uk_interest_genres_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    interest_mappings: Mapped[list["InterestGenreMapping"]] = relationship(
        back_populates="genre",
        cascade="all, delete-orphan",
    )


class InterestGenreMapping(Base):
    __tablename__ = "interest_genre_mappings"
    __table_args__ = (
        UniqueConstraint(
            "interest_id",
            "genre_id",
            name="uk_interest_genre_mappings_interest_genre",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    interest_id: Mapped[int] = mapped_column(
        ForeignKey("interests.id", ondelete="CASCADE"),
        index=True,
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("interest_genres.id", ondelete="CASCADE"),
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )

    interest: Mapped[Interest] = relationship(back_populates="genre_mappings")
    genre: Mapped[InterestGenre] = relationship(back_populates="interest_mappings")
