from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db_session
from app.core.response import success_response
from app.schemas.interest_target import InterestTargetSyncRequest
from app.services.interest_service import InterestService

router = APIRouter()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]


@router.get("")
async def list_selected_interests(
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = InterestService(session)
    result = await service.list_selected(user_id)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.put("")
async def sync_interest_targets(
    request: InterestTargetSyncRequest,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = InterestService(session)
    result = await service.sync(user_id, request)
    return success_response(result.model_dump(mode="json", by_alias=True))
