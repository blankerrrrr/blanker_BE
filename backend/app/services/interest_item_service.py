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
            totalElements=total_elements,
            totalPages=ceil(total_elements / size) if total_elements else 0,
        )

    async def get_detail(
        self,
        user_id: str,
        interest_item_id: str,
    ) -> InterestItemDetailResponse:
        item = await self.interest_items.get_item_by_id(user_id, interest_item_id)
        if item is None:
            raise AppException(ErrorCode.INTEREST_ITEM_NOT_FOUND)
        return self._item_to_detail(item)

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
                interestItemId=existing_item.interest_item_id,
                groupId=existing_item.group_id,
                duplicate=True,
                savedAt=existing_item.created_at,
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
            interestItemId=item.interest_item_id,
            groupId=group.group_id,
            duplicate=duplicate,
            savedAt=item.created_at,
        )

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

    def _group_to_list_item(
        self,
        group: InterestItemGroup,
    ) -> InterestItemListItemResponse:
        return InterestItemListItemResponse(
            interestItemId=group.representative_item_id or "",
            groupId=group.group_id,
            title=group.title,
            summary=group.summary,
            relatedTopics=group.related_topics,
            sourceCount=group.source_count,
            discoveredAt=group.created_at,
        )

    def _item_to_detail(self, item: InterestItem) -> InterestItemDetailResponse:
        return InterestItemDetailResponse(
            interestItemId=item.interest_item_id,
            groupId=item.group_id,
            title=item.title,
            summary=item.summary,
            relatedTopics=item.related_topics,
            sourceUrl=item.source_url,
            selector=item.selector,
            discoveredAt=item.discovered_at,
        )
