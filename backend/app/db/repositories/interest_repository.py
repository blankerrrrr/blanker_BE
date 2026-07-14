from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.interest import Interest
from app.db.repositories.public_id import save_with_public_id


class InterestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_all(self) -> list[Interest]:
        result = await self.session.execute(
            select(Interest).order_by(Interest.genre.asc(), Interest.title.asc()),
        )
        return list(result.scalars().all())

    async def find_all_by_ids(self, interest_ids: list[str]) -> list[Interest]:
        if not interest_ids:
            return []
        result = await self.session.execute(
            select(Interest).where(Interest.interest_id.in_(interest_ids)),
        )
        return list(result.scalars().all())

    async def save(self, interest: Interest) -> Interest:
        return await save_with_public_id(
            self.session,
            interest,
            "interest_id",
            "interest",
        )
