from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.db.models.interest import Interest
from app.db.models.interest_target import InterestTarget
from app.db.repositories.interest_repository import InterestRepository
from app.db.repositories.interest_target_repository import InterestTargetRepository
from app.schemas.interest import (
    InterestListResponse,
    InterestResponse,
    InterestSelectRequest,
    InterestSelectResponse,
    InterestTypeListResponse,
    InterestTypeResponse,
)
from app.schemas.interest_target import InterestTargetResponse


class InterestService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.interests = InterestRepository(session)
        self.interest_targets = InterestTargetRepository(session)

    # DB에 저장된 온보딩용 관심사 목록을 조회한다.
    async def list(
        self,
        interest_type: str,
        genre: str,
        keyword: str | None,
    ) -> InterestListResponse:
        interests = await self.interests.find_all(interest_type, genre, keyword)
        return InterestListResponse(
            items=[self._to_response(interest) for interest in interests],
        )

    # DB에 저장된 관심사 종류 목록을 중복 없이 조회한다.
    async def list_types(self) -> InterestTypeListResponse:
        interest_types = await self.interests.find_types()
        return InterestTypeListResponse(
            items=[
                InterestTypeResponse(name=name, image_url=image_url)
                for name, image_url in interest_types
            ],
        )

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

    # 이미 저장된 개인 관심사는 재사용하고, 없으면 새로 생성한다.
    async def _find_or_create_target(
        self,
        user_id: str,
        interest: Interest,
    ) -> InterestTarget:
        existing_target = await self.interest_targets.get_by_type_and_name(
            user_id,
            "WORK",
            interest.title,
        )
        if existing_target is not None:
            return existing_target

        target = InterestTarget(
            user_id=user_id,
            type="WORK",
            name=interest.title,
            aliases=[],
            keywords=[interest.interest_type, interest.genre],
        )
        await self.interest_targets.save(target)
        return target

    # 관심사 DB 모델을 응답 스키마로 변환한다.
    @staticmethod
    def _to_response(interest: Interest) -> InterestResponse:
        return InterestResponse(
            interest_id=interest.interest_id,
            interest_type=interest.interest_type,
            interest_type_image_url=interest.interest_type_image_url,
            title=interest.title,
            genre=interest.genre,
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
