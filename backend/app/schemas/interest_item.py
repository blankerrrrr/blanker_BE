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
    group_id: str
    title: str
    summary: str
    related_topics: list[str]
    source_count: int
    discovered_at: datetime


class InterestItemListResponse(CamelModel):
    items: list[InterestItemListItemResponse]
    page: int
    size: int
    total_elements: int
    total_pages: int


class InterestItemDetailResponse(CamelModel):
    interest_item_id: str
    group_id: str
    title: str
    summary: str
    related_topics: list[str]
    source_url: str
    selector: str | None = None
    discovered_at: datetime


class InterestItemCreateResponse(CamelModel):
    interest_item_id: str
    group_id: str
    duplicate: bool
    saved_at: datetime


class InterestItemGroupRepresentativeResponse(CamelModel):
    interest_item_id: str
    title: str
    summary: str


class InterestItemGroupSourceResponse(CamelModel):
    interest_item_id: str
    source_url: str
    discovered_at: datetime


class InterestItemGroupDetailResponse(CamelModel):
    interest_item_group_id: str
    representative: InterestItemGroupRepresentativeResponse | None
    sources: list[InterestItemGroupSourceResponse]
    duplicate_reason: str | None = None


class InterestItemGroupSourceAddRequest(CamelModel):
    interest_item_id: str
    duplicate_score: float | None = None
    duplicate_reason: str | None = None


class InterestItemGroupSourceAddResponse(CamelModel):
    interest_item_group_id: str
    source_count: int
    updated_at: datetime
