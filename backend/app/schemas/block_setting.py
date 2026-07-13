from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class BlockSettingCategory(StrEnum):
    SPOILER = "SPOILER"
    HARMFUL = "HARMFUL"
    INTEREST = "INTEREST"


class Sensitivity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class BlockSettingItem(BaseModel):
    enabled: bool
    sensitivity: Sensitivity


class BlockSettingsResponse(BaseModel):
    spoiler: BlockSettingItem
    harmful: BlockSettingItem
    interest: BlockSettingItem


class BlockSettingsUpdateRequest(BlockSettingsResponse):
    pass


class BlockSettingsUpdateResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    updated_at: datetime = Field(alias="updatedAt")
