from datetime import datetime
from enum import StrEnum

from pydantic import Field

from app.schemas.common import CamelModel
from app.schemas.interest_target import InterestTargetResponse


class InterestType(StrEnum):
    MOVIE = "영화"
    DRAMA = "드라마"
    ANIMATION = "애니메이션"
    NOVEL = "소설"
    GAME = "게임"
    MUSICAL = "뮤지컬"
    WEBTOON = "웹툰"
    OTHER = "기타"


class InterestResponse(CamelModel):
    interest_id: str
    interest_type: str
    interest_type_image_url: str | None = None
    title: str
    genre: str
    summary: str | None = None
    image_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class InterestListResponse(CamelModel):
    items: list[InterestResponse]
    page: int
    size: int
    total_elements: int
    total_pages: int


class InterestTypeResponse(CamelModel):
    name: str
    image_url: str | None = None


class InterestTypeListResponse(CamelModel):
    items: list[InterestTypeResponse]


class SelectedInterestTypeResponse(CamelModel):
    name: str


class SelectedInterestTypeListResponse(CamelModel):
    items: list[SelectedInterestTypeResponse]


class InterestGenreResponse(CamelModel):
    name: str


class InterestGenreListResponse(CamelModel):
    items: list[InterestGenreResponse]


class InterestSelectRequest(CamelModel):
    interest_ids: list[str] = Field(min_length=1)


class InterestSelectResponse(CamelModel):
    items: list[InterestTargetResponse]


class SelectedInterestResponse(CamelModel):
    interest_target_id: str
    interest_id: str
    interest_type: str
    interest_type_image_url: str | None = None
    title: str
    genre: str
    summary: str | None = None
    image_url: str | None = None
    created_at: datetime | None = None


class SelectedInterestListResponse(CamelModel):
    items: list[SelectedInterestResponse]
