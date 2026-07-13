from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.analysis import BlockCategory


class BlockedItemCreateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    analysis_request_id: str | None = Field(default=None, alias="analysisRequestId")
    client_content_id: str | None = Field(default=None, alias="clientContentId")
    summary: str
    categories: list[BlockCategory]
    related_topics: list[str] = Field(default_factory=list, alias="relatedTopics")
    source_url: str = Field(alias="sourceUrl")
    selector: str | None = None
    position_text: str | None = Field(default=None, alias="positionText")


class BlockedItemListItemResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    blocked_item_id: str = Field(alias="blockedItemId")
    summary: str
    categories: list[BlockCategory]
    related_topics: list[str] = Field(alias="relatedTopics")
    source_url: str = Field(alias="sourceUrl")
    found_at: datetime = Field(alias="foundAt")


class BlockedItemListResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[BlockedItemListItemResponse]
    page: int
    size: int
    total_elements: int = Field(alias="totalElements")
    total_pages: int = Field(alias="totalPages")


class BlockedItemCreateResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    blocked_item_id: str = Field(alias="blockedItemId")
    saved_at: datetime = Field(alias="savedAt")
