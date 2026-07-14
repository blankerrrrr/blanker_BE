from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.interest import Interest
from app.db.repositories.interest_repository import InterestRepository


@dataclass(frozen=True)
class InterestCatalogItem:
    interest_type: str
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
            existing_interest = await self.interests.get_by_type_title_genre(
                item.interest_type,
                item.title,
                item.genre,
            )
            if existing_interest is None:
                await self.interests.save(
                    Interest(
                        interest_type=item.interest_type,
                        interest_type_image_url=item.interest_type_image_url,
                        title=item.title,
                        genre=item.genre,
                        image_url=item.image_url,
                    ),
                )
                imported_count += 1
                continue

            existing_interest.image_url = item.image_url
            existing_interest.interest_type_image_url = item.interest_type_image_url
            await self.interests.save(existing_interest)

        await self.session.commit()
        return imported_count
