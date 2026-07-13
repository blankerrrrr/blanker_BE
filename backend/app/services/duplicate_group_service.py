from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.core.time import utc_now
from app.db.models.interest_item import InterestItem, InterestItemGroup
from app.db.repositories.interest_item_repository import InterestItemRepository
from app.schemas.interest_item import (
    InterestItemGroupDetailResponse,
    InterestItemGroupRepresentativeResponse,
    InterestItemGroupSourceAddRequest,
    InterestItemGroupSourceAddResponse,
    InterestItemGroupSourceResponse,
)


class DuplicateGroupService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.interest_items = InterestItemRepository(session)

    async def get_detail(
        self,
        user_id: str,
        group_id: str,
    ) -> InterestItemGroupDetailResponse:
        group = await self._get_group(user_id, group_id)
        items = await self.interest_items.find_items_by_group_id(user_id, group_id)
        representative = self._find_representative(group, items)
        return InterestItemGroupDetailResponse(
            interestItemGroupId=group.group_id,
            representative=self._to_representative(representative)
            if representative is not None
            else None,
            sources=[self._to_source(item) for item in items],
            duplicateReason=group.duplicate_reason,
        )

    async def add_source(
        self,
        user_id: str,
        group_id: str,
        request: InterestItemGroupSourceAddRequest,
    ) -> InterestItemGroupSourceAddResponse:
        group = await self._get_group(user_id, group_id)
        item = await self.interest_items.get_item_by_id(
            user_id,
            request.interest_item_id,
        )
        if item is None:
            raise AppException(ErrorCode.INTEREST_ITEM_NOT_FOUND)
        if item.group_id == group.group_id:
            raise AppException(ErrorCode.INTEREST_ITEM_ALREADY_GROUPED)

        old_group = await self.interest_items.get_group_by_id(user_id, item.group_id)
        item.group_id = group.group_id
        if request.duplicate_score is not None:
            item.duplicate_score = Decimal(str(request.duplicate_score))
        await self.interest_items.save_item(item)

        if group.representative_item_id is None:
            group.representative_item_id = item.interest_item_id
        if request.duplicate_reason is not None:
            group.duplicate_reason = request.duplicate_reason
        group.source_count = await self.interest_items.count_items_by_group_id(
            user_id,
            group.group_id,
        )
        group.updated_at = utc_now()
        await self.interest_items.save_group(group)

        if old_group is not None:
            old_group.source_count = await self.interest_items.count_items_by_group_id(
                user_id,
                old_group.group_id,
            )
            old_group.updated_at = utc_now()
            await self.interest_items.save_group(old_group)

        await self.session.commit()
        return InterestItemGroupSourceAddResponse(
            interestItemGroupId=group.group_id,
            sourceCount=group.source_count,
            updatedAt=group.updated_at,
        )

    async def _get_group(self, user_id: str, group_id: str) -> InterestItemGroup:
        group = await self.interest_items.get_group_by_id(user_id, group_id)
        if group is None:
            raise AppException(ErrorCode.INTEREST_ITEM_GROUP_NOT_FOUND)
        return group

    def _find_representative(
        self,
        group: InterestItemGroup,
        items: list[InterestItem],
    ) -> InterestItem | None:
        for item in items:
            if item.interest_item_id == group.representative_item_id:
                return item
        return items[0] if items else None

    def _to_representative(
        self,
        item: InterestItem,
    ) -> InterestItemGroupRepresentativeResponse:
        return InterestItemGroupRepresentativeResponse(
            interestItemId=item.interest_item_id,
            title=item.title,
            summary=item.summary,
        )

    def _to_source(self, item: InterestItem) -> InterestItemGroupSourceResponse:
        return InterestItemGroupSourceResponse(
            interestItemId=item.interest_item_id,
            sourceUrl=item.source_url,
            discoveredAt=item.discovered_at,
        )
