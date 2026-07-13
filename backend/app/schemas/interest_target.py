from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class InterestTargetType(StrEnum):
    WORK = "WORK"
    PERSON = "PERSON"
    TOPIC = "TOPIC"


class InterestTargetCreateRequest(BaseModel):
    type: InterestTargetType
    name: str
    aliases: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)


class InterestTargetUpdateRequest(BaseModel):
    name: str | None = None
    aliases: list[str] | None = None
    keywords: list[str] | None = None


class InterestTargetResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    interest_target_id: str = Field(alias="interestTargetId")
    type: InterestTargetType
    name: str
    aliases: list[str]
    keywords: list[str]
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")


class InterestTargetListResponse(BaseModel):
    items: list[InterestTargetResponse]
