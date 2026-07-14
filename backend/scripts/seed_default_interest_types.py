import asyncio
from enum import StrEnum

from app.db.session import async_session
from app.schemas.interest import InterestType
from app.services.interest_catalog_import_service import (
    InterestCatalogImportService,
    InterestCatalogItem,
)


class PreviewImage(StrEnum):
    GAME = "https://blanker-storage.s3.amazonaws.com/public/game-preview.png"
    MOVIE = "https://blanker-storage.s3.amazonaws.com/public/movie-preview.png"
    MUSICAL = "https://blanker-storage.s3.amazonaws.com/public/musical-preview.png"
    OTHER = "https://blanker-storage.s3.amazonaws.com/public/other-preview.png"
    WEBTOON = "https://blanker-storage.s3.amazonaws.com/public/webtoon-preview.png"
    ANIME = "https://blanker-storage.s3.amazonaws.com/public/anime-preview.png"
    BOOK = "https://blanker-storage.s3.amazonaws.com/public/book-preview.png"
    DRAMA = "https://blanker-storage.s3.amazonaws.com/public/drama-preview.png"


DEFAULT_INTEREST_TYPES = (
    (InterestType.MOVIE, PreviewImage.MOVIE),
    (InterestType.DRAMA, PreviewImage.DRAMA),
    (InterestType.ANIMATION, PreviewImage.ANIME),
    (InterestType.NOVEL, PreviewImage.BOOK),
    (InterestType.GAME, PreviewImage.GAME),
    (InterestType.MUSICAL, PreviewImage.MUSICAL),
    (InterestType.WEBTOON, PreviewImage.WEBTOON),
    (InterestType.OTHER, PreviewImage.OTHER),
)


def build_default_items() -> list[InterestCatalogItem]:
    return [
        InterestCatalogItem(
            interest_type=interest_type,
            title=interest_type.value,
            genre="전체",
            image_url=preview_image.value,
            interest_type_image_url=preview_image.value,
        )
        for interest_type, preview_image in DEFAULT_INTEREST_TYPES
    ]


async def main() -> None:
    async with async_session() as session:
        imported_count = await InterestCatalogImportService(session).import_items(
            build_default_items(),
        )
    print(
        f"default_interest_types={len(DEFAULT_INTEREST_TYPES)} "
        f"imported={imported_count}",
    )


if __name__ == "__main__":
    asyncio.run(main())
