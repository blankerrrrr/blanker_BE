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


def _split_genres(value: str | None) -> list[str]:
    if not value:
        return ["전체"]
    genres = [
        genre.strip()
        for part in value.split(",")
        for genre in part.split(">")
        if genre.strip()
    ]
    return list(dict.fromkeys(genres)) or ["전체"]


def _first_string(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return next((item for item in value if isinstance(item, str)), None)
    return None


def _tmdb_genres(media_type: str) -> dict[int, str]:
    if settings.tmdb_access_token is None:
        return {}
    payload = _read_json(
        f"{settings.tmdb_api_url}/genre/{media_type}/list?language=ko-KR",
        _tmdb_headers(),
    )
    return {
        int(item["id"]): item["name"]
        for item in payload.get("genres", [])
        if item.get("id") is not None and item.get("name")
    }


def _genre_names_from_ids(ids: list[int], genre_map: dict[int, str]) -> list[str]:
    names = [genre_map[genre_id] for genre_id in ids if genre_id in genre_map]
    return list(dict.fromkeys(names)) or ["전체"]


def fetch_tmdb_movies(limit: int) -> list[InterestCatalogItem]:
    if settings.tmdb_access_token is None:
        return []
    genres = _tmdb_genres("movie")
    payload = _read_json(
        f"{settings.tmdb_api_url}/movie/popular?language=ko-KR&page=1",
        _tmdb_headers(),
    )
    return [
        InterestCatalogItem(
            interest_type=InterestType.MOVIE,
            title=item["title"],
            genres=_genre_names_from_ids(item.get("genre_ids", []), genres),
            image_url=_tmdb_image(item.get("poster_path")),
        )
        for item in payload.get("results", [])[:limit]
        if item.get("title")
    ]


def fetch_tmdb_dramas(limit: int) -> list[InterestCatalogItem]:
    if settings.tmdb_access_token is None:
        return []
    genres = _tmdb_genres("tv")
    payload = _read_json(
        f"{settings.tmdb_api_url}/tv/popular?language=ko-KR&page=1",
        _tmdb_headers(),
    )
    return [
        InterestCatalogItem(
            interest_type=InterestType.DRAMA,
            title=item["name"],
            genres=_genre_names_from_ids(item.get("genre_ids", []), genres),
            image_url=_tmdb_image(item.get("poster_path")),
        )
        for item in payload.get("results", [])[:limit]
        if item.get("name")
    ]


def fetch_anime(limit: int) -> list[InterestCatalogItem]:
    if settings.tmdb_access_token is None:
        return []
    genres = _tmdb_genres("tv")
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
            genres=_genre_names_from_ids(item.get("genre_ids", []), genres),
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
            genres=_split_genres(item.get("categoryName")),
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
            genres=[
                genre["name"]
                for genre in item.get("genres", [])
                if genre.get("name")
            ]
            or ["전체"],
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
                genres=_split_genres(node.findtext("genrenm") or "뮤지컬"),
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
            genres=_split_genres(item.get("genre") or item.get("genreNm")),
            image_url=_first_string(item.get("thumbnail")),
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
