from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_current_user_id
from app.core.response import success_response
from app.services.web_search_service import WebSearchService

router = APIRouter()

CurrentUserId = Annotated[str, Depends(get_current_user_id)]


@router.get("")
async def search_web(
    _user_id: CurrentUserId,
    query: Annotated[str, Query(min_length=1, max_length=200)],
    count: int = Query(default=5, ge=1, le=20),
    search_lang: Annotated[
        str | None,
        Query(alias="searchLang", min_length=2, max_length=5),
    ] = "ko",
    freshness: str | None = Query(default=None, max_length=32),
) -> dict[str, object]:
    service = WebSearchService()
    result = await service.search(
        query=query.strip(),
        count=count,
        search_lang=search_lang,
        freshness=freshness,
    )
    return success_response(result.model_dump(mode="json", by_alias=True))
