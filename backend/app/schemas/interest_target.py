from datetime import datetime
from enum import StrEnum

from pydantic import Field

from app.schemas.common import CamelModel


class InterestTargetType(StrEnum):
    WORK = "WORK"
    PERSON = "PERSON"
    TOPIC = "TOPIC"


class InterestTargetCreateRequest(CamelModel):
    type: InterestTargetType
    name: str
    aliases: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)


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
