from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db_session
from app.core.response import success_response
from app.schemas.block_setting import BlockSettingsUpdateRequest
from app.services.block_setting_service import BlockSettingService

router = APIRouter()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]


@router.get("")
async def get_block_settings(
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = BlockSettingService(session)
    result = await service.get(user_id)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.put("")
async def update_block_settings(
    request: BlockSettingsUpdateRequest,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = BlockSettingService(session)
    result = await service.update(user_id, request)
    return success_response(result.model_dump(mode="json", by_alias=True))
