from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.interest import Interest, InterestCatalog
from app.db.models.interest_target import InterestTarget
from app.db.repositories.public_id import save_with_public_id


class InterestTargetRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_all_by_user_id(
        self,
        user_id: str,
        interest_type: str | None = None,
    ) -> list[InterestTarget]:
        statement = select(InterestTarget).where(InterestTarget.user_id == user_id)
        if interest_type is not None:
            statement = (
                statement.join(
                    Interest,
                    Interest.interest_id == InterestTarget.interest_id,
                )
                .join(InterestCatalog)
                .where(InterestCatalog.name == interest_type)
            )
        result = await self.session.execute(
            statement.order_by(InterestTarget.created_at.desc()),
        )
        return list(result.scalars().all())

    async def find_selected_type_names(self, user_id: str) -> list[str]:
        result = await self.session.execute(
            select(InterestCatalog.name)
            .join(Interest)
            .join(
                InterestTarget,
                InterestTarget.interest_id == Interest.interest_id,
            )
            .where(InterestTarget.user_id == user_id)
            .group_by(InterestCatalog.id, InterestCatalog.name)
            .order_by(InterestCatalog.id.asc()),
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

    async def get_by_name(
        self,
        user_id: str,
        name: str,
    ) -> InterestTarget | None:
        result = await self.session.execute(
            select(InterestTarget).where(
                InterestTarget.user_id == user_id,
                func.lower(func.btrim(InterestTarget.name)) == name.lower(),
            ),
        )
        return result.scalar_one_or_none()

    async def save(self, interest_target: InterestTarget) -> InterestTarget:
        return await save_with_public_id(
            self.session,
            interest_target,
            "interest_target_id",
            "interest_target",
        )

    async def find_catalog_targets_by_user_id(
        self,
        user_id: str,
    ) -> list[InterestTarget]:
        result = await self.session.execute(
            select(InterestTarget)
            .where(
                InterestTarget.user_id == user_id,
                InterestTarget.interest_id.is_not(None),
            )
            .order_by(InterestTarget.created_at.desc()),
        )
        return list(result.scalars().all())

    async def find_catalog_target_by_interest_id(
        self,
        user_id: str,
        interest_id: str,
    ) -> InterestTarget | None:
        result = await self.session.execute(
            select(InterestTarget).where(
                InterestTarget.user_id == user_id,
                InterestTarget.interest_id == interest_id,
            ),
        )
        return result.scalar_one_or_none()

    async def delete(self, interest_target: InterestTarget) -> None:
        await self.session.delete(interest_target)
