from datetime import datetime
from enum import StrEnum

from pydantic import Field

from app.schemas.common import CamelModel


class InterestTargetType(StrEnum):
    WORK = "WORK"
    PERSON = "PERSON"
    TOPIC = "TOPIC"


class InterestTargetCreateRequest(CamelModel):
    name: str


class InterestTargetUpdateRequest(CamelModel):
    name: str | None = None
    aliases: list[str] | None = None
    keywords: list[str] | None = None


class InterestTargetResponse(CamelModel):
    interest_target_id: str
    type: InterestTargetType
    name: str
    aliases: list[str]
    keywords: list[str]
    created_at: datetime | None = None
    updated_at: datetime | None = None


class InterestTargetListResponse(CamelModel):
    items: list[InterestTargetResponse]


class InterestTargetTitleResponse(CamelModel):
    interest_target_id: str
    title: str


class InterestTargetTitleListResponse(CamelModel):
    items: list[InterestTargetTitleResponse]


class InterestTargetSyncRequest(CamelModel):
    interest_ids: list[str] = Field(min_length=1)
