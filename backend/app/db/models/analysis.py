from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.time import utc_now
from app.db.base import Base


class AnalysisRequest(Base):
    __tablename__ = "analysis_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    analysis_request_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("users.user_id"),
        index=True,
    )
    page_url: Mapped[str] = mapped_column(Text)
    page_title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )


class AnalysisContent(Base):
    __tablename__ = "analysis_contents"
    __table_args__ = (
        UniqueConstraint(
            "analysis_request_id",
            "client_content_id",
            name="uk_analysis_contents_request_client_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    analysis_content_id: Mapped[str] = mapped_column(String(64), unique=True)
    analysis_request_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("analysis_requests.analysis_request_id"),
        index=True,
    )
    client_content_id: Mapped[str] = mapped_column(String(100))
    unit_type: Mapped[str] = mapped_column(String(20))
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    alt_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    context_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    selector: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    analysis_result_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    analysis_content_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("analysis_contents.analysis_content_id"),
        unique=True,
    )
    categories: Mapped[list[str]] = mapped_column(JSON, default=list)
    risk_level: Mapped[str] = mapped_column(String(20))
    relevance_level: Mapped[str] = mapped_column(String(20))
    should_block: Mapped[bool] = mapped_column(Boolean)
    block_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    related_topics: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
