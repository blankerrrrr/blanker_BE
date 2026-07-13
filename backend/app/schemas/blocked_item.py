from datetime import datetime

from pydantic import Field

from app.schemas.analysis import BlockCategory
from app.schemas.common import CamelModel


class BlockedItemCreateRequest(CamelModel):
    analysis_request_id: str | None = None
    client_content_id: str | None = None
    summary: str
    categories: list[BlockCategory]
    related_topics: list[str] = Field(default_factory=list)
    source_url: str
    selector: str | None = None
    position_text: str | None = None


class BlockedItemListItemResponse(CamelModel):
    blocked_item_id: str
    summary: str
    categories: list[BlockCategory]
    related_topics: list[str]
    source_url: str
    found_at: datetime


class BlockedItemListResponse(CamelModel):
    items: list[BlockedItemListItemResponse]
    page: int
    size: int
    total_elements: int
    total_pages: int


class BlockedItemCreateResponse(CamelModel):
    blocked_item_id: str
    saved_at: datetime
