from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.db.models.blocked_item import BlockedItem
from app.db.repositories.blocked_item_repository import BlockedItemRepository
from app.db.repositories.interest_target_repository import InterestTargetRepository
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
        self.interest_targets = InterestTargetRepository(session)

    # 사용자의 보관함 항목을 페이지와 카테고리 조건으로 조회한다.
    async def list(
        self,
        user_id: str,
        interest_target_id: str | None,
        category: BlockCategory | None,
    ) -> BlockedItemListResponse:
        targets = await self._find_list_targets(user_id, interest_target_id)
        category_value = category.value if category is not None else None

        target_ids = [
            target.interest_target_id
            for target in targets
            if target.interest_target_id is not None
        ]
        items = await self.blocked_items.find_all_by_interest_target_ids(
            user_id,
            target_ids,
            category_value,
        )
        items_by_target_id: dict[str, list[BlockedItemListItemResponse]] = {
            target_id: [] for target_id in target_ids
        }
        for item in items:
            if item.interest_target_id is None:
                continue
            items_by_target_id.setdefault(item.interest_target_id, []).append(
                self._to_list_item(item),
            )

        return BlockedItemListResponse(
            root=[
                {target.name: items_by_target_id[target.interest_target_id or ""]}
                for target in targets
            ],
        )

    # 새 보관함 항목을 저장하고 중복 원본은 거부한다.
    async def create(
        self,
        user_id: str,
        request: BlockedItemCreateRequest,
    ) -> BlockedItemCreateResponse:
        await self._validate_interest_target(user_id, request.interest_target_id)
        existing_item = await self.blocked_items.get_by_source(
            user_id,
            request.interest_target_id,
            request.source_url,
            request.selector,
        )
        if existing_item is not None:
            raise AppException(ErrorCode.BLOCKED_ITEM_ALREADY_EXISTS)

        item = BlockedItem(
            user_id=user_id,
            analysis_request_id=request.analysis_request_id,
            client_content_id=request.client_content_id,
            interest_target_id=request.interest_target_id,
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
            blocked_item_id=item.blocked_item_id,
            saved_at=item.saved_at,
        )

    async def _validate_interest_target(
        self,
        user_id: str,
        interest_target_id: str,
    ) -> None:
        target = await self.interest_targets.get_by_id(user_id, interest_target_id)
        if target is None:
            raise AppException(ErrorCode.INTEREST_TARGET_NOT_FOUND)

    async def _find_list_targets(
        self,
        user_id: str,
        interest_target_id: str | None,
    ):
        if interest_target_id is None:
            return await self.interest_targets.find_all_by_user_id(user_id)

        target = await self.interest_targets.get_by_id(user_id, interest_target_id)
        if target is None:
            raise AppException(ErrorCode.INTEREST_TARGET_NOT_FOUND)
        return [target]

    # 사용자가 소유한 보관함 항목을 삭제한다.
    async def delete(self, user_id: str, blocked_item_id: str) -> None:
        item = await self.blocked_items.get_by_id(user_id, blocked_item_id)
        if item is None:
            raise AppException(ErrorCode.BLOCKED_ITEM_NOT_FOUND)
        await self.blocked_items.delete(item)
        await self.session.commit()

    # 보관함 DB 모델을 목록 응답 항목으로 변환한다.
    @staticmethod
    def _to_list_item(item: BlockedItem) -> BlockedItemListItemResponse:
        return BlockedItemListItemResponse(
            blocked_item_id=item.blocked_item_id,
            interest_target_id=item.interest_target_id,
            summary=item.summary,
            categories=[BlockCategory(category) for category in item.categories],
            related_topics=item.related_topics,
            source_url=item.source_url,
            found_at=item.found_at,
        )
