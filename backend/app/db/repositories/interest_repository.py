from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.interest import Interest
from app.db.repositories.public_id import save_with_public_id


class InterestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_all(
        self,
        interest_type: str,
        genre: str,
        keyword: str | None,
    ) -> list[Interest]:
        statement = select(Interest).where(Interest.interest_type == interest_type)
        if keyword:
            statement = statement.where(Interest.title.ilike(f"%{keyword}%"))
        elif genre != "전체":
            statement = statement.where(Interest.genre == genre)

        result = await self.session.execute(
            statement.order_by(Interest.genre.asc(), Interest.title.asc()),
        )
        return list(result.scalars().all())

    async def find_types(self) -> list[tuple[str, str | None]]:
        result = await self.session.execute(
            select(
                Interest.interest_type,
                func.max(Interest.interest_type_image_url),
            )
            .group_by(Interest.interest_type)
            .order_by(Interest.interest_type),
        )
        return [(row[0], row[1]) for row in result.all()]

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
