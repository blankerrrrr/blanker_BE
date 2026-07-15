from __future__ import annotations

from math import ceil
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.query_cache import QueryCache
from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.db.models.interest import Interest
from app.db.models.interest_target import InterestTarget
from app.db.repositories.interest_repository import InterestRepository
from app.db.repositories.interest_target_repository import InterestTargetRepository
from app.schemas.common import CamelModel
from app.schemas.interest import (
    InterestGenreListResponse,
    InterestGenreResponse,
    InterestListResponse,
    InterestResponse,
    InterestSelectRequest,
    InterestSelectResponse,
    InterestTypeListResponse,
    InterestTypeResponse,
    SelectedInterestListResponse,
    SelectedInterestResponse,
    SelectedInterestTypeListResponse,
    SelectedInterestTypeResponse,
)
from app.schemas.interest_target import (
    InterestTargetResponse,
    InterestTargetSyncRequest,
)

T = TypeVar("T", bound=CamelModel)


class InterestService:
    CATALOG_CACHE_TTL_SECONDS = 60 * 10

    def __init__(
        self,
        session: AsyncSession,
        query_cache: QueryCache | None = None,
    ) -> None:
        self.session = session
        self.interests = InterestRepository(session)
        self.interest_targets = InterestTargetRepository(session)
        self.query_cache = query_cache

    # DB에 저장된 온보딩용 관심사 목록을 조회한다.
    async def list(
        self,
        interest_type: str,
        genres: list[str],
        keyword: str | None,
        page: int,
        size: int,
    ) -> InterestListResponse:
        cache_key = QueryCache.key(
            "interests:list",
            {
                "interestType": interest_type,
                "genre": genres,
                "keyword": keyword,
                "page": page,
                "size": size,
            },
        )
        cached = await self._get_cached(cache_key, InterestListResponse)
        if cached is not None:
            return cached

        total_elements = await self.interests.count_all(
            interest_type,
            genres,
            keyword,
        )
        interests = await self.interests.find_all(
            interest_type,
            genres,
            keyword,
            offset=(page - 1) * size,
            limit=size,
        )
        result = InterestListResponse(
            items=[self._to_response(interest) for interest in interests],
            page=page,
            size=size,
            total_elements=total_elements,
            total_pages=ceil(total_elements / size) if total_elements else 0,
        )
        await self._set_cached(cache_key, result)
        return result

    # DB에 저장된 관심사 종류 목록을 중복 없이 조회한다.
    async def list_types(self) -> InterestTypeListResponse:
        cache_key = QueryCache.key("interests:types", {})
        cached = await self._get_cached(cache_key, InterestTypeListResponse)
        if cached is not None:
            return cached

        interest_types = await self.interests.find_types()
        result = InterestTypeListResponse(
            items=[
                InterestTypeResponse(name=name, image_url=image_url)
                for name, image_url in interest_types
            ],
        )
        await self._set_cached(cache_key, result)
        return result

    # 관심사 종류별 장르 목록을 조회한다.
    async def list_genres(self, interest_type: str) -> InterestGenreListResponse:
        cache_key = QueryCache.key(
            "interests:genres",
            {"interestType": interest_type},
        )
        cached = await self._get_cached(cache_key, InterestGenreListResponse)
        if cached is not None:
            return cached

        genre_names = await self.interests.find_genres_by_type(interest_type)
        result = InterestGenreListResponse(
            items=[InterestGenreResponse(name=name) for name in genre_names],
        )
        await self._set_cached(cache_key, result)
        return result

    # 선택한 관심사를 현재 사용자의 개인 관심사로 저장한다.
    async def select(
        self,
        user_id: str,
        request: InterestSelectRequest,
    ) -> InterestSelectResponse:
        interest_ids = list(dict.fromkeys(request.interest_ids))
        interests = await self.interests.find_all_by_ids(interest_ids)
        if len(interests) != len(interest_ids):
            raise AppException(ErrorCode.INTEREST_NOT_FOUND)

        targets: list[InterestTarget] = []
        for interest in interests:
            target = await self._find_or_create_target(user_id, interest)
            targets.append(target)

        await self.session.commit()
        return InterestSelectResponse(
            items=[self._to_target_response(target) for target in targets],
        )

    # 사용자가 선택한 카탈로그 관심사 목록을 조회한다.
    async def list_selected(self, user_id: str) -> SelectedInterestListResponse:
        targets = await self.interest_targets.find_catalog_targets_by_user_id(user_id)
        if not targets:
            return SelectedInterestListResponse(items=[])
        interest_ids = [t.interest_id for t in targets if t.interest_id]
        interests = {
            i.interest_id: i
            for i in await self.interests.find_all_by_ids(interest_ids)
        }
        items = []
        for target in targets:
            interest = interests.get(target.interest_id)
            if interest:
                items.append(self._to_selected_response(target, interest))
        return SelectedInterestListResponse(items=items)

    # 사용자가 선택한 관심사가 속한 관심사 종류만 조회한다.
    async def list_selected_types(
        self,
        user_id: str,
    ) -> SelectedInterestTypeListResponse:
        names = await self.interest_targets.find_selected_type_names(user_id)
        return SelectedInterestTypeListResponse(
            items=[SelectedInterestTypeResponse(name=name) for name in names],
        )

    # 카탈로그 관심사 선택 목록을 동기화한다 (추가 및 제거).
    async def sync(
        self,
        user_id: str,
        request: InterestTargetSyncRequest,
    ) -> SelectedInterestListResponse:
        interest_ids = list(dict.fromkeys(request.interest_ids))
        interests = await self.interests.find_all_by_ids(interest_ids)
        if len(interests) != len(interest_ids):
            raise AppException(ErrorCode.INTEREST_NOT_FOUND)

        current_targets = (
            await self.interest_targets.find_catalog_targets_by_user_id(user_id)
        )
        current_map = {t.interest_id: t for t in current_targets}
        requested_ids = set(interest_ids)

        for target in current_targets:
            if target.interest_id not in requested_ids:
                await self.interest_targets.delete(target)

        interest_map = {i.interest_id: i for i in interests}
        synced_targets: list[InterestTarget] = []
        for iid in interest_ids:
            interest = interest_map[iid]
            target = current_map.get(iid)
            if target is None:
                target = await self._find_or_create_target(user_id, interest)

            target.type = "WORK"
            target.name = interest.title
            target.interest_id = interest.interest_id
            target.keywords = [interest.catalog.name, *self._genre_names(interest)]
            await self.interest_targets.save(target)
            synced_targets.append(target)

        await self.session.commit()

        items = []
        for target in synced_targets:
            interest = interest_map.get(target.interest_id)
            if interest:
                items.append(self._to_selected_response(target, interest))
        return SelectedInterestListResponse(items=items)

    # 이미 저장된 개인 관심사는 재사용하고, 없으면 새로 생성한다.
    async def _find_or_create_target(
        self,
        user_id: str,
        interest: Interest,
    ) -> InterestTarget:
        existing_target = (
            await self.interest_targets.find_catalog_target_by_interest_id(
                user_id,
                interest.interest_id,
            )
        )
        if existing_target is not None:
            return existing_target

        existing_target = await self.interest_targets.get_by_type_and_name(
            user_id,
            "WORK",
            interest.title,
        )
        if existing_target is not None:
            if existing_target.interest_id is None:
                existing_target.interest_id = interest.interest_id
                await self.interest_targets.save(existing_target)
            return existing_target

        target = InterestTarget(
            user_id=user_id,
            type="WORK",
            name=interest.title,
            interest_id=interest.interest_id,
            aliases=[],
            keywords=[interest.catalog.name, *self._genre_names(interest)],
        )
        await self.interest_targets.save(target)
        return target

    @staticmethod
    def _to_selected_response(
        target: InterestTarget,
        interest: Interest,
    ) -> SelectedInterestResponse:
        return SelectedInterestResponse(
            interest_target_id=target.interest_target_id,
            interest_id=interest.interest_id,
            interest_type=interest.catalog.name,
            interest_type_image_url=interest.catalog.image_url,
            title=interest.title,
            genre=InterestService._genres_text(interest),
            summary=interest.summary,
            image_url=interest.image_url,
            created_at=target.created_at,
        )

    # 관심사 DB 모델을 응답 스키마로 변환한다.
    @staticmethod
    def _to_response(interest: Interest) -> InterestResponse:
        return InterestResponse(
            interest_id=interest.interest_id,
            interest_type=interest.catalog.name,
            interest_type_image_url=interest.catalog.image_url,
            title=interest.title,
            genre=InterestService._genres_text(interest),
            summary=interest.summary,
            image_url=interest.image_url,
            created_at=interest.created_at,
            updated_at=interest.updated_at,
        )

    # 개인 관심사 DB 모델을 응답 스키마로 변환한다.
    @staticmethod
    def _to_target_response(target: InterestTarget) -> InterestTargetResponse:
        return InterestTargetResponse(
            interest_target_id=target.interest_target_id,
            type=target.type,
            name=target.name,
            aliases=target.aliases,
            keywords=target.keywords,
            created_at=target.created_at,
            updated_at=target.updated_at,
        )

    @staticmethod
    def _genre_names(interest: Interest) -> list[str]:
        return [
            mapping.genre.name
            for mapping in interest.genre_mappings
            if mapping.genre is not None
        ]

    @staticmethod
    def _genres_text(interest: Interest) -> str:
        names = InterestService._genre_names(interest)
        return ", ".join(names) if names else "전체"

    async def _get_cached(self, key: str, model_type: type[T]) -> T | None:
        if self.query_cache is None:
            return None
        return await self.query_cache.get_model(key, model_type)

    async def _set_cached(self, key: str, value: CamelModel) -> None:
        if self.query_cache is None:
            return
        await self.query_cache.set_model(
            key,
            value,
            ttl_seconds=self.CATALOG_CACHE_TTL_SECONDS,
        )
