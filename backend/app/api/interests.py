from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db_session, get_query_cache
from app.cache.query_cache import QueryCache
from app.core.response import success_response
from app.schemas.interest import InterestSelectRequest, InterestType
from app.schemas.interest_target import InterestTargetCreateRequest
from app.services.interest_service import InterestService
from app.services.interest_target_service import InterestTargetService

router = APIRouter()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]
QueryCacheDep = Annotated[QueryCache, Depends(get_query_cache)]


@router.get("")
async def list_interests(
    session: DbSession,
    user_id: CurrentUserId,
    query_cache: QueryCacheDep,
    interest_type: Annotated[InterestType, Query(alias="interestType")],
    genre: Annotated[list[str] | None, Query()] = None,
    keyword: str | None = None,
) -> dict[str, object]:
    service = InterestService(session, query_cache=query_cache)
    result = await service.list(interest_type, genre or ["전체"], keyword)
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.get("/types")
async def list_interest_types(
    session: DbSession,
    user_id: CurrentUserId,
    query_cache: QueryCacheDep,
) -> dict[str, object]:
    service = InterestService(session, query_cache=query_cache)
    result = await service.list_types()
    return success_response(result.model_dump(mode="json", by_alias=True))


@router.get("/genres")
async def list_interest_genres(
    session: DbSession,
    user_id: CurrentUserId,
    query_cache: QueryCacheDep,
    interest_type: Annotated[InterestType, Query(alias="interestType")],
) -> dict[str, object]:
    service = InterestService(session, query_cache=query_cache)
    result = await service.list_genres(interest_type)
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


@router.post("/targets", status_code=status.HTTP_201_CREATED)
async def create_interest_target(
    request: InterestTargetCreateRequest,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = InterestTargetService(session)
    result = await service.create(user_id, request)
    return success_response(result.model_dump(mode="json", by_alias=True))
