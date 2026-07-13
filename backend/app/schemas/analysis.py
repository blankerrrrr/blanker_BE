from enum import StrEnum

from app.schemas.common import CamelModel


class ContentUnitType(StrEnum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    AREA = "AREA"


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RelevanceLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class BlockCategory(StrEnum):
    SPOILER = "SPOILER"
    HARMFUL = "HARMFUL"
    INTEREST = "INTEREST"


class AnalysisPageRequest(CamelModel):
    url: str
    title: str | None = None


class AnalysisContentRequest(CamelModel):
    client_content_id: str
    unit_type: ContentUnitType
    text: str | None = None
    image_url: str | None = None
    alt_text: str | None = None
    context_text: str | None = None
    selector: str | None = None


class AnalysisRequestCreate(CamelModel):
    page: AnalysisPageRequest
    contents: list[AnalysisContentRequest]


class BlockActionResponse(CamelModel):
    unit_type: ContentUnitType
    reason: str
    related_topics: list[str]


class AnalysisResultResponse(CamelModel):
    client_content_id: str
    categories: list[BlockCategory]
    risk_level: RiskLevel
    relevance_level: RelevanceLevel
    should_block: bool
    block_action: BlockActionResponse | None = None


class AnalysisRequestResponse(CamelModel):
    analysis_request_id: str
    results: list[AnalysisResultResponse]
