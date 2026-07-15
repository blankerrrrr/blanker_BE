from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.core.s3 import S3ImageStorage
from app.db.models.interest_item import InterestItem
from app.db.repositories.interest_item_repository import InterestItemRepository
from app.db.repositories.interest_target_repository import InterestTargetRepository
from app.schemas.interest_item import (
    InterestItemCreateRequest,
    InterestItemCreateResponse,
    InterestItemDetailResponse,
    InterestItemListItemResponse,
    InterestItemListResponse,
    InterestItemUrlListResponse,
    InterestItemUrlResponse,
)


class InterestItemService:
    def __init__(
        self,
        session: AsyncSession,
        image_storage: S3ImageStorage | None = None,
    ) -> None:
        self.session = session
        self.interest_items = InterestItemRepository(session)
        self.interest_targets = InterestTargetRepository(session)
        self.image_storage = image_storage or S3ImageStorage()

    # 사용자의 관심 정보 목록을 페이지 단위로 조회한다.
    async def list_items(
        self,
        user_id: str,
        page: int,
        size: int,
    ) -> InterestItemListResponse:
        total_elements = await self.interest_items.count_items(user_id)
        items = await self.interest_items.find_items(
            user_id,
            offset=(page - 1) * size,
            limit=size,
        )
        return InterestItemListResponse(
            items=[self._to_list_item(item) for item in items],
            page=page,
            size=size,
            total_elements=total_elements,
            total_pages=ceil(total_elements / size) if total_elements else 0,
        )

    # 사용자의 수집 관심 정보 원본 URL 목록을 조회한다.
    async def list_urls(self, user_id: str) -> InterestItemUrlListResponse:
        items = await self.interest_items.find_urls(user_id)
        items_by_date: dict[str, list[InterestItemUrlResponse]] = {}
        for item in sorted(items, key=lambda item: item.discovered_at, reverse=True):
            date_key = item.discovered_at.date().isoformat()
            items_by_date.setdefault(date_key, []).append(self._to_url_item(item))
        return InterestItemUrlListResponse(
            root=[
                {date_key: date_items}
                for date_key, date_items in items_by_date.items()
            ],
        )

    # 사용자가 소유한 관심 정보 상세를 조회한다.
    async def get_detail(
        self,
        user_id: str,
        interest_item_id: str,
    ) -> InterestItemDetailResponse:
        item = await self.interest_items.get_item_by_id(user_id, interest_item_id)
        if item is None:
            raise AppException(ErrorCode.INTEREST_ITEM_NOT_FOUND)
        return self._to_detail(item)

    # 새 관심 정보를 저장한다. 같은 출처 URL이 이미 존재하면 중복으로 처리한다.
    async def create(
        self,
        user_id: str,
        request: InterestItemCreateRequest,
    ) -> InterestItemCreateResponse:
        await self._validate_relevance(user_id, request.related_topics)

        existing_item = await self.interest_items.get_item_by_source_url(
            user_id,
            request.source_url,
        )
        if existing_item is not None:
            return InterestItemCreateResponse(
                interest_item_id=existing_item.interest_item_id,
                duplicate=True,
                saved_at=existing_item.created_at,
            )

        item = InterestItem(
            user_id=user_id,
            title=request.title,
            summary=request.summary,
            content_text=request.content_text,
            related_topics=request.related_topics,
            source_url=request.source_url,
            selector=request.selector,
        )
        await self.interest_items.save_item(item)

        if request.image_url is not None:
            item.image_url = await self.image_storage.upload_from_url(
                request.image_url,
                user_id,
                item.interest_item_id or "",
            )
            await self.interest_items.save_item(item)

        await self.session.commit()

        return InterestItemCreateResponse(
            interest_item_id=item.interest_item_id,
            duplicate=False,
            saved_at=item.created_at,
        )

    # 관심 정보가 사용자의 등록 관심 대상과 관련 있는지 검증한다.
    async def _validate_relevance(
        self,
        user_id: str,
        related_topics: list[str],
    ) -> None:
        targets = await self.interest_targets.find_all_by_user_id(user_id)
        if not targets:
            raise AppException(ErrorCode.INTEREST_ITEM_NOT_RELEVANT)

        normalized_topics = {topic.casefold() for topic in related_topics}
        target_terms: set[str] = set()
        for target in targets:
            target_terms.add(target.name.casefold())
            target_terms.update(alias.casefold() for alias in target.aliases)
            target_terms.update(keyword.casefold() for keyword in target.keywords)

        if normalized_topics.isdisjoint(target_terms):
            raise AppException(ErrorCode.INTEREST_ITEM_NOT_RELEVANT)

    @staticmethod
    def _to_list_item(item: InterestItem) -> InterestItemListItemResponse:
        return InterestItemListItemResponse(
            interest_item_id=item.interest_item_id or "",
            title=item.title,
            summary=item.summary,
            image_url=item.image_url,
            related_topics=item.related_topics,
            discovered_at=item.discovered_at,
        )

    @staticmethod
    def _to_url_item(item: InterestItem) -> InterestItemUrlResponse:
        return InterestItemUrlResponse(
            interest_item_id=item.interest_item_id or "",
            source_url=item.source_url,
            summary=item.summary,
            discovered_at=item.discovered_at,
        )

    @staticmethod
    def _to_detail(item: InterestItem) -> InterestItemDetailResponse:
        return InterestItemDetailResponse(
            interest_item_id=item.interest_item_id or "",
            title=item.title,
            summary=item.summary,
            image_url=item.image_url,
            related_topics=item.related_topics,
            source_url=item.source_url,
            selector=item.selector,
            discovered_at=item.discovered_at,
        )
