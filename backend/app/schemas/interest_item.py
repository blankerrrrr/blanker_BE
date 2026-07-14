from datetime import datetime

from pydantic import Field

from app.schemas.common import CamelModel


class InterestItemCreateRequest(CamelModel):
    title: str
    summary: str
    content_text: str | None = None
    related_topics: list[str] = Field(default_factory=list)
    source_url: str
    selector: str | None = None


class InterestItemListItemResponse(CamelModel):
    interest_item_id: str
    title: str
    summary: str
    related_topics: list[str]
    discovered_at: datetime


class InterestItemListResponse(CamelModel):
    items: list[InterestItemListItemResponse]
    page: int
    size: int
    total_elements: int
    total_pages: int


class InterestItemDetailResponse(CamelModel):
    interest_item_id: str
    title: str
    summary: str
    related_topics: list[str]
    source_url: str
    selector: str | None = None
    discovered_at: datetime


class InterestItemCreateResponse(CamelModel):
    interest_item_id: str
    duplicate: bool
    saved_at: datetime
