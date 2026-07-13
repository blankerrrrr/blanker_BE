from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.core.id_generator import generate_public_id
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

    async def list(self, user_id: str) -> InterestTargetListResponse:
        targets = await self.interest_targets.find_all_by_user_id(user_id)
        return InterestTargetListResponse(
            items=[self._to_response(target) for target in targets],
        )

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
            interest_target_id=generate_public_id("target_"),
            user_id=user_id,
            type=request.type.value,
            name=request.name,
            aliases=request.aliases,
            keywords=request.keywords,
        )
        await self.interest_targets.save(target)
        await self.session.commit()
        return self._to_response(target)

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

    async def delete(self, user_id: str, interest_target_id: str) -> None:
        target = await self._get_owned_target(user_id, interest_target_id)
        await self.interest_targets.delete(target)
        await self.session.commit()

    async def _get_owned_target(
        self,
        user_id: str,
        interest_target_id: str,
    ) -> InterestTarget:
        target = await self.interest_targets.get_by_id(user_id, interest_target_id)
        if target is None:
            raise AppException(ErrorCode.INTEREST_TARGET_NOT_FOUND)
        return target

    def _to_response(self, target: InterestTarget) -> InterestTargetResponse:
        return InterestTargetResponse(
            interestTargetId=target.interest_target_id,
            type=target.type,
            name=target.name,
            aliases=target.aliases,
            keywords=target.keywords,
            createdAt=target.created_at,
            updatedAt=target.updated_at,
        )
