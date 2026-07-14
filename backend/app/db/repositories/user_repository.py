from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analysis import AnalysisContent, AnalysisRequest, AnalysisResult
from app.db.models.block_setting import BlockSetting
from app.db.models.blocked_item import BlockedItem
from app.db.models.interest_item import InterestItem
from app.db.models.interest_target import InterestTarget
from app.db.models.user import User
from app.db.repositories.public_id import save_with_public_id


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: str) -> User | None:
        result = await self.session.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    async def save(self, user: User) -> User:
        return await save_with_public_id(self.session, user, "user_id", "user")

    async def delete_owned_data(self, user_id: str) -> None:
        request_ids = select(AnalysisRequest.analysis_request_id).where(
            AnalysisRequest.user_id == user_id,
        )
        content_ids = select(AnalysisContent.analysis_content_id).where(
            AnalysisContent.analysis_request_id.in_(request_ids),
        )

        await self.session.execute(
            delete(AnalysisResult).where(
                AnalysisResult.analysis_content_id.in_(content_ids),
            ),
        )
        await self.session.execute(
            delete(AnalysisContent).where(
                AnalysisContent.analysis_request_id.in_(request_ids),
            ),
        )
        await self.session.execute(
            delete(AnalysisRequest).where(AnalysisRequest.user_id == user_id),
        )
        await self.session.execute(
            delete(BlockedItem).where(BlockedItem.user_id == user_id),
        )
        await self.session.execute(
            delete(InterestItem).where(InterestItem.user_id == user_id),
        )
        await self.session.execute(
            delete(BlockSetting).where(BlockSetting.user_id == user_id),
        )
        await self.session.execute(
            delete(InterestTarget).where(InterestTarget.user_id == user_id),
        )

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
