from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db_session
from app.core.response import success_response
from app.schemas.interest import InterestSelectRequest
from app.services.interest_service import InterestService

router = APIRouter()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]


@router.get("")
async def list_interests(
    session: DbSession,
    interest_type: Annotated[str, Query(alias="interestType")],
    genre: str = "전체",
    keyword: str | None = None,
) -> dict[str, object]:
    service = InterestService(session)
    result = await service.list(interest_type, genre, keyword)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.get("/types")
async def list_interest_types(session: DbSession) -> dict[str, object]:
    service = InterestService(session)
    result = await service.list_types()
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.post("/select")
async def select_interests(
    request: InterestSelectRequest,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = InterestService(session)
    result = await service.select(user_id, request)
    return success_response(result.model_dump(mode="json", by_alias=True))
