import argparse
import asyncio
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from app.core.config import settings
from app.db.session import async_session
from app.schemas.interest import InterestType
from app.services.interest_catalog_import_service import (
    InterestCatalogImportService,
    InterestCatalogItem,
)


def _read_json(url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def _read_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=20) as response:
        return response.read().decode("utf-8")


def _tmdb_headers() -> dict[str, str]:
    if settings.tmdb_access_token is None:
        return {}
    return {"Authorization": f"Bearer {settings.tmdb_access_token}"}


def _tmdb_image(path: str | None) -> str | None:
    if path is None:
        return None
    return f"{settings.tmdb_image_url}{path}"


def fetch_tmdb_movies(limit: int) -> list[InterestCatalogItem]:
    if settings.tmdb_access_token is None:
        return []
    payload = _read_json(
        f"{settings.tmdb_api_url}/movie/popular?language=ko-KR&page=1",
        _tmdb_headers(),
    )
    return [
        InterestCatalogItem(
            interest_type=InterestType.MOVIE,
            title=item["title"],
            genre="전체",
            image_url=_tmdb_image(item.get("poster_path")),
        )
        for item in payload.get("results", [])[:limit]
        if item.get("title")
    ]


def fetch_tmdb_dramas(limit: int) -> list[InterestCatalogItem]:
    if settings.tmdb_access_token is None:
        return []
    payload = _read_json(
        f"{settings.tmdb_api_url}/tv/popular?language=ko-KR&page=1",
        _tmdb_headers(),
    )
    return [
        InterestCatalogItem(
            interest_type=InterestType.DRAMA,
            title=item["name"],
            genre="전체",
            image_url=_tmdb_image(item.get("poster_path")),
        )
        for item in payload.get("results", [])[:limit]
        if item.get("name")
    ]


def fetch_anime(limit: int) -> list[InterestCatalogItem]:
    if settings.tmdb_access_token is None:
        return []
    query = urllib.parse.urlencode(
        {"with_genres": 16, "language": "ko-KR", "sort_by": "popularity.desc"},
    )
    payload = _read_json(
        f"{settings.tmdb_api_url}/discover/tv?{query}",
        _tmdb_headers(),
    )
    return [
        InterestCatalogItem(
            interest_type=InterestType.ANIMATION,
            title=item["name"],
            genre="전체",
            image_url=_tmdb_image(item.get("poster_path")),
        )
        for item in payload.get("results", [])[:limit]
        if item.get("name")
    ]


def fetch_books(limit: int) -> list[InterestCatalogItem]:
    if settings.aladin_ttb_key is None:
        return []
    query = urllib.parse.urlencode(
        {
            "ttbkey": settings.aladin_ttb_key,
            "QueryType": "Bestseller",
            "SearchTarget": "Book",
            "output": "js",
            "Version": "20131101",
        },
    )
    payload = _read_json(f"{settings.aladin_api_url}/ItemList.aspx?{query}")
    return [
        InterestCatalogItem(
            interest_type=InterestType.NOVEL,
            title=item["title"],
            genre=item.get("categoryName") or "전체",
            image_url=item.get("cover"),
        )
        for item in payload.get("item", [])[:limit]
        if item.get("title")
    ]


def fetch_games(limit: int) -> list[InterestCatalogItem]:
    if settings.rawg_api_key is None:
        return []
    payload = _read_json(
        f"{settings.rawg_api_url}/games?key={settings.rawg_api_key}&ordering=-rating",
    )
    return [
        InterestCatalogItem(
            interest_type=InterestType.GAME,
            title=item["name"],
            genre=(item.get("genres") or [{"name": "전체"}])[0]["name"],
            image_url=item.get("background_image"),
        )
        for item in payload.get("results", [])[:limit]
        if item.get("name")
    ]


def fetch_musicals(limit: int) -> list[InterestCatalogItem]:
    if settings.kopis_service_key is None:
        return []
    url = (
        f"{settings.kopis_api_url}/pblprfr"
        f"?service={settings.kopis_service_key}"
        "&stdate=20260101&eddate=20261231&cpage=1&rows=100&shcate=GGGD"
    )
    root = ET.fromstring(_read_text(url))
    items: list[InterestCatalogItem] = []
    for node in root.findall("db")[:limit]:
        title = node.findtext("prfnm")
        if not title:
            continue
        items.append(
            InterestCatalogItem(
                interest_type=InterestType.MUSICAL,
                title=title,
                genre="뮤지컬",
                image_url=node.findtext("poster"),
            ),
        )
    return items


def fetch_webtoons(limit: int) -> list[InterestCatalogItem]:
    if settings.korea_webtoon_api_url is None:
        return []
    query = urllib.parse.urlencode({"perPage": limit})
    payload = _read_json(f"{settings.korea_webtoon_api_url}/webtoons?{query}")
    return [
        InterestCatalogItem(
            interest_type=InterestType.WEBTOON,
            title=item["title"],
            genre=item.get("genre") or "전체",
            image_url=item.get("thumbnail"),
        )
        for item in payload.get("webtoons", [])
        if item.get("title")
    ]


def fetch_all(limit: int) -> list[InterestCatalogItem]:
    items: list[InterestCatalogItem] = []
    fetchers = (
        fetch_tmdb_movies,
        fetch_tmdb_dramas,
        fetch_anime,
        fetch_books,
        fetch_games,
        fetch_musicals,
        fetch_webtoons,
    )
    for fetcher in fetchers:
        try:
            items.extend(fetcher(limit))
        except Exception as exc:
            print(f"{fetcher.__name__} failed: {exc}")
    return items


async def main() -> None:
    parser = argparse.ArgumentParser(description="Import interests from external APIs")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    items = await asyncio.to_thread(fetch_all, args.limit)
    async with async_session() as session:
        imported_count = await InterestCatalogImportService(session).import_items(items)
    print(f"fetched={len(items)} imported={imported_count}")


if __name__ == "__main__":
    asyncio.run(main())
