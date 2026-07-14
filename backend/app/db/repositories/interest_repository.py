from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.interest import Interest, InterestCatalog
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
        statement = (
            select(Interest)
            .join(InterestCatalog)
            .options(selectinload(Interest.catalog))
            .where(InterestCatalog.name == interest_type)
        )
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
            select(InterestCatalog.name, InterestCatalog.image_url).order_by(
                InterestCatalog.name,
            ),
        )
        return [(row[0], row[1]) for row in result.all()]

    async def find_all_by_ids(self, interest_ids: list[str]) -> list[Interest]:
        if not interest_ids:
            return []
        result = await self.session.execute(
            select(Interest)
            .options(selectinload(Interest.catalog))
            .where(Interest.interest_id.in_(interest_ids)),
        )
        return list(result.scalars().all())

    async def get_by_type_title_genre(
        self,
        interest_type: str,
        title: str,
        genre: str,
    ) -> Interest | None:
        result = await self.session.execute(
            select(Interest)
            .join(InterestCatalog)
            .options(selectinload(Interest.catalog))
            .where(
                InterestCatalog.name == interest_type,
                Interest.title == title,
                Interest.genre == genre,
            ),
        )
        return result.scalar_one_or_none()

    async def get_catalog_by_name(self, name: str) -> InterestCatalog | None:
        result = await self.session.execute(
            select(InterestCatalog).where(InterestCatalog.name == name),
        )
        return result.scalar_one_or_none()

    async def save_catalog(self, catalog: InterestCatalog) -> InterestCatalog:
        self.session.add(catalog)
        await self.session.flush()
        await self.session.refresh(catalog)
        return catalog

    async def save(self, interest: Interest) -> Interest:
        return await save_with_public_id(
            self.session,
            interest,
            "interest_id",
            "interest",
        )
