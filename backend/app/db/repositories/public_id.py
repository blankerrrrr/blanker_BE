from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession


async def save_with_public_id(
    session: AsyncSession,
    instance: Any,
    field_name: str,
    model_name: str,
) -> Any:
    if getattr(instance, field_name) is None:
        setattr(instance, field_name, f"{model_name}_pending_{uuid4().hex}")
    session.add(instance)
    await session.flush()
    setattr(instance, field_name, f"{model_name}_{instance.id}")
    await session.flush()
    await session.refresh(instance)
    return instance
