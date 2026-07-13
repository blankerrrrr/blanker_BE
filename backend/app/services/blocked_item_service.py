from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.core.id_generator import generate_public_id
from app.db.models.blocked_item import BlockedItem
from app.db.repositories.blocked_item_repository import BlockedItemRepository
from app.schemas.analysis import BlockCategory
from app.schemas.blocked_item import (
    BlockedItemCreateRequest,
    BlockedItemCreateResponse,
    BlockedItemListItemResponse,
    BlockedItemListResponse,
)


class BlockedItemService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.blocked_items = BlockedItemRepository(session)

    async def list(
        self,
        user_id: str,
        page: int,
        size: int,
        category: BlockCategory | None,
    ) -> BlockedItemListResponse:
        category_value = category.value if category is not None else None
        total_elements = await self.blocked_items.count(user_id, category_value)
        items = await self.blocked_items.find_all(
            user_id,
            category_value,
            offset=(page - 1) * size,
            limit=size,
        )
        return BlockedItemListResponse(
            items=[self._to_list_item(item) for item in items],
            page=page,
            size=size,
            totalElements=total_elements,
            totalPages=ceil(total_elements / size) if total_elements else 0,
        )

    async def create(
        self,
        user_id: str,
        request: BlockedItemCreateRequest,
    ) -> BlockedItemCreateResponse:
        existing_item = await self.blocked_items.get_by_source(
            user_id,
            request.source_url,
            request.selector,
        )
        if existing_item is not None:
            raise AppException(ErrorCode.BLOCKED_ITEM_ALREADY_EXISTS)

        item = BlockedItem(
            blocked_item_id=generate_public_id("blocked_"),
            user_id=user_id,
            analysis_request_id=request.analysis_request_id,
            client_content_id=request.client_content_id,
            summary=request.summary,
            categories=[category.value for category in request.categories],
            related_topics=request.related_topics,
            source_url=request.source_url,
            selector=request.selector,
            position_text=request.position_text,
        )
        await self.blocked_items.save(item)
        await self.session.commit()
        return BlockedItemCreateResponse(
            blockedItemId=item.blocked_item_id,
            savedAt=item.saved_at,
        )

    async def delete(self, user_id: str, blocked_item_id: str) -> None:
        item = await self.blocked_items.get_by_id(user_id, blocked_item_id)
        if item is None:
            raise AppException(ErrorCode.BLOCKED_ITEM_NOT_FOUND)
        await self.blocked_items.delete(item)
        await self.session.commit()

    def _to_list_item(self, item: BlockedItem) -> BlockedItemListItemResponse:
        return BlockedItemListItemResponse(
            blockedItemId=item.blocked_item_id,
            summary=item.summary,
            categories=[BlockCategory(category) for category in item.categories],
            relatedTopics=item.related_topics,
            sourceUrl=item.source_url,
            foundAt=item.found_at,
        )
