from sqlalchemy.ext.asyncio import AsyncSession

from app.core.time import utc_now
from app.db.models.block_setting import BlockSetting
from app.db.repositories.block_setting_repository import BlockSettingRepository
from app.schemas.block_setting import (
    BlockSettingCategory,
    BlockSettingItem,
    BlockSettingsResponse,
    BlockSettingsUpdateRequest,
    BlockSettingsUpdateResponse,
    Sensitivity,
)

DEFAULT_SETTINGS = {
    BlockSettingCategory.SPOILER: BlockSettingItem(
        enabled=True,
        sensitivity=Sensitivity.HIGH,
    ),
    BlockSettingCategory.HARMFUL: BlockSettingItem(
        enabled=True,
        sensitivity=Sensitivity.MEDIUM,
    ),
    BlockSettingCategory.INTEREST: BlockSettingItem(
        enabled=True,
        sensitivity=Sensitivity.LOW,
    ),
}


class BlockSettingService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.block_settings = BlockSettingRepository(session)

    async def get(self, user_id: str) -> BlockSettingsResponse:
        settings = await self.block_settings.find_all_by_user_id(user_id)
        setting_map = {
            BlockSettingCategory(setting.category): BlockSettingItem(
                enabled=setting.enabled,
                sensitivity=Sensitivity(setting.sensitivity),
            )
            for setting in settings
        }
        return self._to_response(DEFAULT_SETTINGS | setting_map)

    async def update(
        self,
        user_id: str,
        request: BlockSettingsUpdateRequest,
    ) -> BlockSettingsUpdateResponse:
        requested_settings = {
            BlockSettingCategory.SPOILER: request.spoiler,
            BlockSettingCategory.HARMFUL: request.harmful,
            BlockSettingCategory.INTEREST: request.interest,
        }
        updated_at = utc_now()
        for category, item in requested_settings.items():
            setting = await self.block_settings.get_by_category(user_id, category.value)
            if setting is None:
                setting = BlockSetting(
                    user_id=user_id,
                    category=category.value,
                    enabled=item.enabled,
                    sensitivity=item.sensitivity.value,
                )
            else:
                setting.enabled = item.enabled
                setting.sensitivity = item.sensitivity.value
                setting.updated_at = updated_at
            await self.block_settings.save(setting)

        await self.session.commit()
        return BlockSettingsUpdateResponse(updatedAt=updated_at)

    def _to_response(
        self,
        settings: dict[BlockSettingCategory, BlockSettingItem],
    ) -> BlockSettingsResponse:
        return BlockSettingsResponse(
            spoiler=settings[BlockSettingCategory.SPOILER],
            harmful=settings[BlockSettingCategory.HARMFUL],
            interest=settings[BlockSettingCategory.INTEREST],
        )
