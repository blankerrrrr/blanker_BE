from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.interest import Interest, InterestCatalog
from app.db.repositories.interest_repository import InterestRepository
from app.schemas.interest import InterestType


@dataclass(frozen=True)
class InterestCatalogItem:
    interest_type: InterestType
    title: str
    genre: str
    image_url: str | None = None
    interest_type_image_url: str | None = None


class InterestCatalogImportService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.interests = InterestRepository(session)

    # 외부 API에서 가져온 관심사 데이터를 중복 없이 저장한다.
    async def import_items(self, items: list[InterestCatalogItem]) -> int:
        imported_count = 0
        for item in items:
            catalog = await self._find_or_create_catalog(
                item.interest_type.value,
                item.interest_type_image_url,
            )
            existing_interest = await self.interests.get_by_type_title_genre(
                item.interest_type.value,
                item.title,
                item.genre,
            )
            if existing_interest is None:
                await self.interests.save(
                    Interest(
                        interest_catalog_id=catalog.id,
                        title=item.title,
                        genre=item.genre,
                        image_url=item.image_url,
                    ),
                )
                imported_count += 1
                continue

            existing_interest.image_url = item.image_url
            await self.interests.save(existing_interest)

        await self.session.commit()
        return imported_count

    async def import_types(self, items: list[tuple[InterestType, str | None]]) -> int:
        imported_count = 0
        for interest_type, image_url in items:
            catalog = await self.interests.get_catalog_by_name(interest_type.value)
            if catalog is None:
                await self.interests.save_catalog(
                    InterestCatalog(name=interest_type.value, image_url=image_url),
                )
                imported_count += 1
                continue

            if image_url is not None and catalog.image_url != image_url:
                catalog.image_url = image_url
                await self.interests.save_catalog(catalog)

        await self.session.commit()
        return imported_count

    async def _find_or_create_catalog(
        self,
        name: str,
        image_url: str | None,
    ) -> InterestCatalog:
        catalog = await self.interests.get_catalog_by_name(name)
        if catalog is not None:
            if image_url is not None and catalog.image_url != image_url:
                catalog.image_url = image_url
                await self.interests.save_catalog(catalog)
            return catalog

        return await self.interests.save_catalog(
            InterestCatalog(name=name, image_url=image_url),
        )
