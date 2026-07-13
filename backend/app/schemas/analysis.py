from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


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


class AnalysisPageRequest(BaseModel):
    url: str
    title: str | None = None


class AnalysisContentRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    client_content_id: str = Field(alias="clientContentId")
    unit_type: ContentUnitType = Field(alias="unitType")
    text: str | None = None
    image_url: str | None = Field(default=None, alias="imageUrl")
    alt_text: str | None = Field(default=None, alias="altText")
    context_text: str | None = Field(default=None, alias="contextText")
    selector: str | None = None


class AnalysisRequestCreate(BaseModel):
    page: AnalysisPageRequest
    contents: list[AnalysisContentRequest]


class BlockActionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    unit_type: ContentUnitType = Field(alias="unitType")
    reason: str
    related_topics: list[str] = Field(alias="relatedTopics")


class AnalysisResultResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    client_content_id: str = Field(alias="clientContentId")
    categories: list[BlockCategory]
    risk_level: RiskLevel = Field(alias="riskLevel")
    relevance_level: RelevanceLevel = Field(alias="relevanceLevel")
    should_block: bool = Field(alias="shouldBlock")
    block_action: BlockActionResponse | None = Field(default=None, alias="blockAction")


class AnalysisRequestResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    analysis_request_id: str = Field(alias="analysisRequestId")
    results: list[AnalysisResultResponse]
