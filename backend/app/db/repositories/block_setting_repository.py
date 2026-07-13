from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.block_setting import BlockSetting
from app.db.repositories.public_id import save_with_public_id


class BlockSettingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_all_by_user_id(self, user_id: str) -> list[BlockSetting]:
        result = await self.session.execute(
            select(BlockSetting).where(BlockSetting.user_id == user_id),
        )
        return list(result.scalars().all())

    async def get_by_category(
        self,
        user_id: str,
        category: str,
    ) -> BlockSetting | None:
        result = await self.session.execute(
            select(BlockSetting).where(
                BlockSetting.user_id == user_id,
                BlockSetting.category == category,
            ),
        )
        return result.scalar_one_or_none()

    async def save(self, setting: BlockSetting) -> BlockSetting:
        return await save_with_public_id(
            self.session,
            setting,
            "block_setting_id",
            "block_setting",
        )
