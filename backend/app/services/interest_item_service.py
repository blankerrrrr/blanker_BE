from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.core.time import utc_now
from app.db.models.interest_item import InterestItem, InterestItemGroup
from app.db.repositories.interest_item_repository import InterestItemRepository
from app.db.repositories.interest_target_repository import InterestTargetRepository
from app.schemas.interest_item import (
    InterestItemCreateRequest,
    InterestItemCreateResponse,
    InterestItemDetailResponse,
    InterestItemListItemResponse,
    InterestItemListResponse,
)


class InterestItemService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.interest_items = InterestItemRepository(session)
        self.interest_targets = InterestTargetRepository(session)

    # 사용자의 관심 정보 그룹 목록을 페이지 단위로 조회한다.
    async def list_items(
        self,
        user_id: str,
        page: int,
        size: int,
    ) -> InterestItemListResponse:
        total_elements = await self.interest_items.count_groups(user_id)
        groups = await self.interest_items.find_groups(
            user_id,
            offset=(page - 1) * size,
            limit=size,
        )
        return InterestItemListResponse(
            items=[self._group_to_list_item(group) for group in groups],
            page=page,
            size=size,
            total_elements=total_elements,
            total_pages=ceil(total_elements / size) if total_elements else 0,
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
        return self._item_to_detail(item)

    # 새 관심 정보를 저장하고 같은 출처는 중복 저장으로 처리한다.
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
                group_id=existing_item.group_id,
                duplicate=True,
                saved_at=existing_item.created_at,
            )

        group = await self.interest_items.get_group_by_title(user_id, request.title)
        duplicate = group is not None
        if group is None:
            group = await self._create_group(user_id, request)

        item = InterestItem(
            user_id=user_id,
            group_id=group.group_id,
            title=request.title,
            summary=request.summary,
            content_text=request.content_text,
            related_topics=request.related_topics,
            source_url=request.source_url,
            selector=request.selector,
            duplicate_score=1 if duplicate else None,
        )
        await self.interest_items.save_item(item)

        if group.representative_item_id is None:
            group.representative_item_id = item.interest_item_id
        group.source_count += 1
        group.updated_at = utc_now()
        await self.interest_items.save_group(group)
        await self.session.commit()

        return InterestItemCreateResponse(
            interest_item_id=item.interest_item_id,
            group_id=group.group_id,
            duplicate=duplicate,
            saved_at=item.created_at,
        )

    # 새 관심 정보 그룹을 생성한다.
    async def _create_group(
        self,
        user_id: str,
        request: InterestItemCreateRequest,
    ) -> InterestItemGroup:
        group = InterestItemGroup(
            user_id=user_id,
            title=request.title,
            summary=request.summary,
            related_topics=request.related_topics,
            source_count=0,
        )
        return await self.interest_items.save_group(group)

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

    # 관심 정보 그룹 모델을 목록 응답 항목으로 변환한다.
    @staticmethod
    def _group_to_list_item(
            group: InterestItemGroup,
    ) -> InterestItemListItemResponse:
        return InterestItemListItemResponse(
            interest_item_id=group.representative_item_id or "",
            group_id=group.group_id,
            title=group.title,
            summary=group.summary,
            related_topics=group.related_topics,
            source_count=group.source_count,
            discovered_at=group.created_at,
        )

    # 관심 정보 모델을 상세 응답으로 변환한다.
    @staticmethod
    def _item_to_detail(item: InterestItem) -> InterestItemDetailResponse:
        return InterestItemDetailResponse(
            interest_item_id=item.interest_item_id,
            group_id=item.group_id,
            title=item.title,
            summary=item.summary,
            related_topics=item.related_topics,
            source_url=item.source_url,
            selector=item.selector,
            discovered_at=item.discovered_at,
        )
