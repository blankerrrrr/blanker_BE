from datetime import datetime

from pydantic import Field

from app.schemas.common import CamelModel
from app.schemas.interest_target import InterestTargetResponse


class InterestResponse(CamelModel):
    interest_id: str
    interest_type: str
    interest_type_image_url: str | None = None
    title: str
    genre: str
    image_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class InterestListResponse(CamelModel):
    items: list[InterestResponse]


class InterestTypeResponse(CamelModel):
    name: str
    image_url: str | None = None


class InterestTypeListResponse(CamelModel):
    items: list[InterestTypeResponse]


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
    image_url: str | None = None
    created_at: datetime | None = None


class SelectedInterestListResponse(CamelModel):
    items: list[SelectedInterestResponse]
