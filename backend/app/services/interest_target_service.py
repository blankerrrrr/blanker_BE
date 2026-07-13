from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.db.models.interest_target import InterestTarget
from app.db.repositories.interest_target_repository import InterestTargetRepository
from app.schemas.interest_target import (
    InterestTargetCreateRequest,
    InterestTargetListResponse,
    InterestTargetResponse,
    InterestTargetUpdateRequest,
)


class InterestTargetService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.interest_targets = InterestTargetRepository(session)

    # 사용자의 관심 대상 목록을 조회한다.
    async def list(self, user_id: str) -> InterestTargetListResponse:
        targets = await self.interest_targets.find_all_by_user_id(user_id)
        return InterestTargetListResponse(
            items=[self._to_response(target) for target in targets],
        )

    # 새 관심 대상을 생성하고 사용자 내 중복 등록을 막는다.
    async def create(
        self,
        user_id: str,
        request: InterestTargetCreateRequest,
    ) -> InterestTargetResponse:
        existing_target = await self.interest_targets.get_by_type_and_name(
            user_id,
            request.type.value,
            request.name,
        )
        if existing_target is not None:
            raise AppException(ErrorCode.INTEREST_TARGET_ALREADY_EXISTS)

        target = InterestTarget(
            user_id=user_id,
            type=request.type.value,
            name=request.name,
            aliases=request.aliases,
            keywords=request.keywords,
        )
        await self.interest_targets.save(target)
        await self.session.commit()
        return self._to_response(target)

    # 사용자가 소유한 관심 대상의 수정 가능한 필드를 갱신한다.
    async def update(
        self,
        user_id: str,
        interest_target_id: str,
        request: InterestTargetUpdateRequest,
    ) -> InterestTargetResponse:
        target = await self._get_owned_target(user_id, interest_target_id)

        if request.name is not None:
            target.name = request.name
        if request.aliases is not None:
            target.aliases = request.aliases
        if request.keywords is not None:
            target.keywords = request.keywords

        await self.interest_targets.save(target)
        await self.session.commit()
        return self._to_response(target)

    # 사용자가 소유한 관심 대상을 삭제한다.
    async def delete(self, user_id: str, interest_target_id: str) -> None:
        target = await self._get_owned_target(user_id, interest_target_id)
        await self.interest_targets.delete(target)
        await self.session.commit()

    # 사용자 소유권을 확인하며 관심 대상을 조회한다.
    async def _get_owned_target(
        self,
        user_id: str,
        interest_target_id: str,
    ) -> InterestTarget:
        target = await self.interest_targets.get_by_id(user_id, interest_target_id)
        if target is None:
            raise AppException(ErrorCode.INTEREST_TARGET_NOT_FOUND)
        return target

    # 관심 대상 DB 모델을 응답 스키마로 변환한다.
    @staticmethod
    def _to_response(target: InterestTarget) -> InterestTargetResponse:
        return InterestTargetResponse(
            interest_target_id=target.interest_target_id,
            type=target.type,
            name=target.name,
            aliases=target.aliases,
            keywords=target.keywords,
            created_at=target.created_at,
            updated_at=target.updated_at,
        )
