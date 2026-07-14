from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.db.models.interest_item import InterestItem, InterestItemGroup
from app.db.repositories.interest_item_repository import InterestItemRepository
from app.schemas.interest_item import (
    InterestItemGroupDetailResponse,
    InterestItemGroupRepresentativeResponse,
    InterestItemGroupSourceResponse,
)


class DuplicateGroupService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.interest_items = InterestItemRepository(session)

    # 중복 그룹의 대표 항목과 출처 목록을 조회한다.
    async def get_detail(
        self,
        user_id: str,
        group_id: str,
    ) -> InterestItemGroupDetailResponse:
        group = await self._get_group(user_id, group_id)
        items = await self.interest_items.find_items_by_group_id(user_id, group_id)
        representative = self._find_representative(group, items)
        return InterestItemGroupDetailResponse(
            interest_item_group_id=group.group_id,
            representative=self._to_representative(representative)
            if representative is not None
            else None,
            sources=[self._to_source(item) for item in items],
            duplicate_reason=group.duplicate_reason,
        )

    # 사용자가 소유한 관심 정보 그룹을 조회한다.
    async def _get_group(self, user_id: str, group_id: str) -> InterestItemGroup:
        group = await self.interest_items.get_group_by_id(user_id, group_id)
        if group is None:
            raise AppException(ErrorCode.INTEREST_ITEM_GROUP_NOT_FOUND)
        return group

    # 그룹의 대표 항목을 찾고 없으면 첫 번째 출처를 대체 대표로 사용한다.
    def _find_representative(
        self,
        group: InterestItemGroup,
        items: list[InterestItem],
    ) -> InterestItem | None:
        for item in items:
            if item.interest_item_id == group.representative_item_id:
                return item
        return items[0] if items else None

    # 관심 정보 항목을 그룹 대표 응답으로 변환한다.
    def _to_representative(
        self,
        item: InterestItem,
    ) -> InterestItemGroupRepresentativeResponse:
        return InterestItemGroupRepresentativeResponse(
            interest_item_id=item.interest_item_id,
            title=item.title,
            summary=item.summary,
        )

    # 관심 정보 항목을 그룹 출처 응답으로 변환한다.
    @staticmethod
    def _to_source(item: InterestItem) -> InterestItemGroupSourceResponse:
        return InterestItemGroupSourceResponse(
            interest_item_id=item.interest_item_id,
            source_url=item.source_url,
            discovered_at=item.discovered_at,
        )
