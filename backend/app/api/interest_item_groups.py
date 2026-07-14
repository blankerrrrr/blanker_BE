from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db_session
from app.core.response import success_response
from app.services.duplicate_group_service import DuplicateGroupService

router = APIRouter()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]


@router.get("/{interest_item_group_id}")
async def get_interest_item_group(
    interest_item_group_id: str,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = DuplicateGroupService(session)
    result = await service.get_detail(user_id, interest_item_group_id)
    return success_response(result.model_dump(mode="json", by_alias=True))


