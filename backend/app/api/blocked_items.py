from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db_session
from app.core.response import success_response
from app.schemas.analysis import BlockCategory
from app.schemas.blocked_item import BlockedItemCreateRequest
from app.services.blocked_item_service import BlockedItemService

router = APIRouter()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]
CategoryFilter = Annotated[BlockCategory | None, Query()]


@router.get("")
async def list_blocked_items(
    user_id: CurrentUserId,
    session: DbSession,
    interest_target_id: Annotated[str | None, Query(alias="interestTargetId")] = None,
    interest_type: Annotated[str | None, Query(alias="interestType")] = None,
    type: CategoryFilter = None,
) -> dict[str, object]:
    service = BlockedItemService(session)
    result = await service.list(user_id, interest_target_id, interest_type, type)
    return success_response(jsonable_encoder(result.root, by_alias=True))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_blocked_item(
    request: BlockedItemCreateRequest,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = BlockedItemService(session)
    result = await service.create(user_id, request)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.delete("/{blocked_item_id}")
async def delete_blocked_item(
    blocked_item_id: str,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = BlockedItemService(session)
    await service.delete(user_id, blocked_item_id)
    return success_response(None)
