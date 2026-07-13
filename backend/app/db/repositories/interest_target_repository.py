from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.interest_target import InterestTarget


class InterestTargetRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_all_by_user_id(self, user_id: str) -> list[InterestTarget]:
        result = await self.session.execute(
            select(InterestTarget)
            .where(InterestTarget.user_id == user_id)
            .order_by(InterestTarget.created_at.desc()),
        )
        return list(result.scalars().all())

    async def get_by_id(
        self,
        user_id: str,
        interest_target_id: str,
    ) -> InterestTarget | None:
        result = await self.session.execute(
            select(InterestTarget).where(
                InterestTarget.user_id == user_id,
                InterestTarget.interest_target_id == interest_target_id,
            ),
        )
        return result.scalar_one_or_none()

    async def get_by_type_and_name(
        self,
        user_id: str,
        target_type: str,
        name: str,
    ) -> InterestTarget | None:
        result = await self.session.execute(
            select(InterestTarget).where(
                InterestTarget.user_id == user_id,
                InterestTarget.type == target_type,
                InterestTarget.name == name,
            ),
        )
        return result.scalar_one_or_none()

    async def save(self, interest_target: InterestTarget) -> InterestTarget:
        self.session.add(interest_target)
        await self.session.flush()
        await self.session.refresh(interest_target)
        return interest_target

    async def delete(self, interest_target: InterestTarget) -> None:
        await self.session.delete(interest_target)
