from sqlalchemy import cast, func, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.blocked_item import BlockedItem


class BlockedItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def count(self, user_id: str, category: str | None) -> int:
        statement = select(func.count()).select_from(BlockedItem).where(
            BlockedItem.user_id == user_id,
        )
        if category is not None:
            statement = statement.where(
                cast(BlockedItem.categories, JSONB).contains([category]),
            )
        result = await self.session.execute(statement)
        return int(result.scalar_one())

    async def find_all(
        self,
        user_id: str,
        category: str | None,
        offset: int,
        limit: int,
    ) -> list[BlockedItem]:
        statement = select(BlockedItem).where(BlockedItem.user_id == user_id)
        if category is not None:
            statement = statement.where(
                cast(BlockedItem.categories, JSONB).contains([category]),
            )
        result = await self.session.execute(
            statement.order_by(BlockedItem.saved_at.desc()).offset(offset).limit(limit),
        )
        return list(result.scalars().all())

    async def get_by_id(self, user_id: str, blocked_item_id: str) -> BlockedItem | None:
        result = await self.session.execute(
            select(BlockedItem).where(
                BlockedItem.user_id == user_id,
                BlockedItem.blocked_item_id == blocked_item_id,
            ),
        )
        return result.scalar_one_or_none()

    async def get_by_source(
        self,
        user_id: str,
        source_url: str,
        selector: str | None,
    ) -> BlockedItem | None:
        result = await self.session.execute(
            select(BlockedItem).where(
                BlockedItem.user_id == user_id,
                BlockedItem.source_url == source_url,
                BlockedItem.selector == selector,
            ),
        )
        return result.scalar_one_or_none()

    async def save(self, item: BlockedItem) -> BlockedItem:
        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)
        return item

    async def delete(self, item: BlockedItem) -> None:
        await self.session.delete(item)
