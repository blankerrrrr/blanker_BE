from datetime import datetime
from enum import StrEnum

from app.schemas.common import CamelModel


class BlockSettingCategory(StrEnum):
    SPOILER = "SPOILER"
    HARMFUL = "HARMFUL"
    INTEREST = "INTEREST"


class Sensitivity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class BlockSettingItem(CamelModel):
    enabled: bool
    sensitivity: Sensitivity


class BlockSettingsResponse(CamelModel):
    spoiler: BlockSettingItem
    harmful: BlockSettingItem
    interest: BlockSettingItem


class BlockSettingsUpdateRequest(BlockSettingsResponse):
    pass


class BlockSettingsUpdateResponse(CamelModel):
    updated_at: datetime
