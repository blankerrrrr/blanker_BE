from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InterestItemCreateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str
    summary: str
    content_text: str | None = Field(default=None, alias="contentText")
    related_topics: list[str] = Field(default_factory=list, alias="relatedTopics")
    source_url: str = Field(alias="sourceUrl")
    selector: str | None = None


class InterestItemListItemResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    interest_item_id: str = Field(alias="interestItemId")
    group_id: str = Field(alias="groupId")
    title: str
    summary: str
    related_topics: list[str] = Field(alias="relatedTopics")
    source_count: int = Field(alias="sourceCount")
    discovered_at: datetime = Field(alias="discoveredAt")


class InterestItemListResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    items: list[InterestItemListItemResponse]
    page: int
    size: int
    total_elements: int = Field(alias="totalElements")
    total_pages: int = Field(alias="totalPages")


class InterestItemDetailResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    interest_item_id: str = Field(alias="interestItemId")
    group_id: str = Field(alias="groupId")
    title: str
    summary: str
    related_topics: list[str] = Field(alias="relatedTopics")
    source_url: str = Field(alias="sourceUrl")
    selector: str | None = None
    discovered_at: datetime = Field(alias="discoveredAt")


class InterestItemCreateResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    interest_item_id: str = Field(alias="interestItemId")
    group_id: str = Field(alias="groupId")
    duplicate: bool
    saved_at: datetime = Field(alias="savedAt")


class InterestItemGroupRepresentativeResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    interest_item_id: str = Field(alias="interestItemId")
    title: str
    summary: str


class InterestItemGroupSourceResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    interest_item_id: str = Field(alias="interestItemId")
    source_url: str = Field(alias="sourceUrl")
    discovered_at: datetime = Field(alias="discoveredAt")


class InterestItemGroupDetailResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    interest_item_group_id: str = Field(alias="interestItemGroupId")
    representative: InterestItemGroupRepresentativeResponse | None
    sources: list[InterestItemGroupSourceResponse]
    duplicate_reason: str | None = Field(default=None, alias="duplicateReason")


class InterestItemGroupSourceAddRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    interest_item_id: str = Field(alias="interestItemId")
    duplicate_score: float | None = Field(default=None, alias="duplicateScore")
    duplicate_reason: str | None = Field(default=None, alias="duplicateReason")


class InterestItemGroupSourceAddResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    interest_item_group_id: str = Field(alias="interestItemGroupId")
    source_count: int = Field(alias="sourceCount")
    updated_at: datetime = Field(alias="updatedAt")
