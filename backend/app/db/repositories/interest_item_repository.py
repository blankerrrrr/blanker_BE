from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.interest_item import InterestItem
from app.db.repositories.public_id import save_with_public_id


class InterestItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def count_items(self, user_id: str) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(InterestItem).where(
                InterestItem.user_id == user_id,
            ),
        )
        return int(result.scalar_one())

    async def find_items(
        self,
        user_id: str,
        offset: int,
        limit: int,
    ) -> list[InterestItem]:
        result = await self.session.execute(
            select(InterestItem)
            .where(InterestItem.user_id == user_id)
            .order_by(InterestItem.discovered_at.desc())
            .offset(offset)
            .limit(limit),
        )
        return list(result.scalars().all())

    async def get_item_by_id(
        self,
        user_id: str,
        interest_item_id: str,
    ) -> InterestItem | None:
        result = await self.session.execute(
            select(InterestItem).where(
                InterestItem.user_id == user_id,
                InterestItem.interest_item_id == interest_item_id,
            ),
        )
        return result.scalar_one_or_none()

    async def get_item_by_source_url(
        self,
        user_id: str,
        source_url: str,
    ) -> InterestItem | None:
        result = await self.session.execute(
            select(InterestItem).where(
                InterestItem.user_id == user_id,
                InterestItem.source_url == source_url,
            ),
        )
        return result.scalar_one_or_none()

    async def save_item(self, item: InterestItem) -> InterestItem:
        return await save_with_public_id(
            self.session,
            item,
            "interest_item_id",
            "interest_item",
        )
