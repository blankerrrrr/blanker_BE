from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db_session
from app.core.response import success_response
from app.schemas.interest_item import InterestItemCreateRequest
from app.services.interest_item_service import InterestItemService

router = APIRouter()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]


@router.get("")
async def list_interest_items(
    user_id: CurrentUserId,
    session: DbSession,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
) -> dict[str, object]:
    service = InterestItemService(session)
    result = await service.list_items(user_id, page, size)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.get("/urls")
async def list_interest_item_urls(
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = InterestItemService(session)
    result = await service.list_urls(user_id)
    return success_response(jsonable_encoder(result.root, by_alias=True))


@router.get("/{interest_item_id}")
async def get_interest_item(
    interest_item_id: str,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = InterestItemService(session)
    result = await service.get_detail(user_id, interest_item_id)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_interest_item(
    request: InterestItemCreateRequest,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = InterestItemService(session)
    result = await service.create(user_id, request)
    return success_response(result.model_dump(mode="json", by_alias=True))
