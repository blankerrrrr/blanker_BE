from pydantic import Field

from app.schemas.analysis import (
    BlockCategory,
    ContentUnitType,
    RelevanceLevel,
    RiskLevel,
)
from app.schemas.common import CamelModel


class AnalysisInput(CamelModel):
    client_content_id: str
    unit_type: ContentUnitType
    text: str | None = None
    image_url: str | None = None
    alt_text: str | None = None
    context_text: str | None = None
    selector: str | None = None
    interest_terms: set[str] = Field(default_factory=set)

    @property
    def content_text(self) -> str:
        return " ".join(
            value
            for value in (
                self.text,
                self.alt_text,
                self.context_text,
                self.image_url,
            )
            if value
        )


class ClassificationResult(CamelModel):
    categories: list[BlockCategory] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    relevance_level: RelevanceLevel = RelevanceLevel.LOW
    related_topics: list[str] = Field(default_factory=list)
    reason: str | None = None

    @property
    def should_block(self) -> bool:
        return self.risk_level == RiskLevel.HIGH or (
            self.risk_level == RiskLevel.MEDIUM
            and self.relevance_level != RelevanceLevel.LOW
        )


class DuplicateCandidate(CamelModel):
    source_id: str
    title: str | None = None
    url: str | None = None
    summary: str | None = None
    related_topics: list[str] = Field(default_factory=list)

    @property
    def searchable_text(self) -> str:
        return " ".join(
            value
            for value in (
                self.title,
                self.url,
                self.summary,
                " ".join(self.related_topics),
            )
            if value
        )


class DuplicateResult(CamelModel):
    is_duplicate: bool
    representative_id: str | None = None
    score: float = 0.0
    reason: str | None = None


class InterestTargetEnrichmentResult(CamelModel):
    type: str = "WORK"
    aliases: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
