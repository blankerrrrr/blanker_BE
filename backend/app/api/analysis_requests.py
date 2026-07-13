from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db_session
from app.core.response import success_response
from app.schemas.analysis import AnalysisRequestCreate
from app.services.analysis_service import AnalysisService

router = APIRouter()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]


@router.post("")
async def create_analysis_request(
    request: AnalysisRequestCreate,
    user_id: CurrentUserId,
    session: DbSession,
) -> dict[str, object]:
    service = AnalysisService(session)
    result = await service.analyze(user_id, request)
    return success_response(result.model_dump(mode="json", by_alias=True))
