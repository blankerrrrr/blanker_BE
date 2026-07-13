from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db_session
from app.core.response import success_response
from app.schemas.interest_target import (
    InterestTargetCreateRequest,
    InterestTargetUpdateRequest,
)
from app.services.interest_target_service import InterestTargetService

router = APIRouter()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]


@router.get("")
async def list_interest_targets(
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = InterestTargetService(session)
    result = await service.list(user_id)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_interest_target(
    request: InterestTargetCreateRequest,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = InterestTargetService(session)
    result = await service.create(user_id, request)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.patch("/{interest_target_id}")
async def update_interest_target(
    interest_target_id: str,
    request: InterestTargetUpdateRequest,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = InterestTargetService(session)
    result = await service.update(user_id, interest_target_id, request)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.delete("/{interest_target_id}")
async def delete_interest_target(
    interest_target_id: str,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = InterestTargetService(session)
    await service.delete(user_id, interest_target_id)
    return success_response(None)
