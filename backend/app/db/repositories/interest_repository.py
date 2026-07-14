from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.interest import (
    Interest,
    InterestCatalog,
    InterestGenre,
    InterestGenreMapping,
)
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
            .options(
                selectinload(Interest.catalog),
                selectinload(Interest.genre_mappings).selectinload(
                    InterestGenreMapping.genre,
                ),
            )
            .where(InterestCatalog.name == interest_type)
        )
        if keyword:
            statement = statement.where(Interest.title.ilike(f"%{keyword}%"))
        elif genre != "전체":
            statement = statement.join(InterestGenreMapping).join(InterestGenre).where(
                InterestGenre.name == genre,
            )

        result = await self.session.execute(
            statement.order_by(Interest.title.asc()),
        )
        return list(result.scalars().unique().all())

    async def find_types(self) -> list[tuple[str, str | None]]:
        result = await self.session.execute(
            select(InterestCatalog.name, InterestCatalog.image_url).order_by(
                InterestCatalog.id.asc(),
            ),
        )
        return [(row[0], row[1]) for row in result.all()]

    async def find_type_title_pairs(self) -> list[tuple[str, str]]:
        result = await self.session.execute(
            select(InterestCatalog.name, Interest.title).join(Interest),
        )
        return [(row[0], row[1]) for row in result.all()]

    async def find_all_by_ids(self, interest_ids: list[str]) -> list[Interest]:
        if not interest_ids:
            return []
        result = await self.session.execute(
            select(Interest)
            .options(
                selectinload(Interest.catalog),
                selectinload(Interest.genre_mappings).selectinload(
                    InterestGenreMapping.genre,
                ),
            )
            .where(Interest.interest_id.in_(interest_ids)),
        )
        return list(result.scalars().all())

    async def find_genres_by_type(self, interest_type: str) -> list[str]:
        result = await self.session.execute(
            select(InterestGenre.name)
            .join(InterestGenreMapping)
            .join(Interest)
            .join(InterestCatalog)
            .where(InterestCatalog.name == interest_type)
            .distinct()
            .order_by(InterestGenre.name.asc()),
        )
        return list(result.scalars().all())

    async def get_by_type_title(
        self,
        interest_type: str,
        title: str,
    ) -> Interest | None:
        result = await self.session.execute(
            select(Interest)
            .join(InterestCatalog)
            .options(
                selectinload(Interest.catalog),
                selectinload(Interest.genre_mappings).selectinload(
                    InterestGenreMapping.genre,
                ),
            )
            .where(
                InterestCatalog.name == interest_type,
                Interest.title == title,
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

    async def get_genre_by_name(self, name: str) -> InterestGenre | None:
        result = await self.session.execute(
            select(InterestGenre).where(InterestGenre.name == name),
        )
        return result.scalar_one_or_none()

    async def save_genre(self, genre: InterestGenre) -> InterestGenre:
        self.session.add(genre)
        await self.session.flush()
        await self.session.refresh(genre)
        return genre

    async def get_genre_mapping(
        self,
        interest_id: int,
        genre_id: int,
    ) -> InterestGenreMapping | None:
        result = await self.session.execute(
            select(InterestGenreMapping).where(
                InterestGenreMapping.interest_id == interest_id,
                InterestGenreMapping.genre_id == genre_id,
            ),
        )
        return result.scalar_one_or_none()

    async def save_genre_mapping(
        self,
        mapping: InterestGenreMapping,
    ) -> InterestGenreMapping:
        self.session.add(mapping)
        await self.session.flush()
        await self.session.refresh(mapping)
        return mapping

    async def save(self, interest: Interest) -> Interest:
        return await save_with_public_id(
            self.session,
            interest,
            "interest_id",
            "interest",
        )
