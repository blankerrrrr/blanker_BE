from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analysis import AnalysisContent, AnalysisRequest, AnalysisResult
from app.db.repositories.public_id import save_with_public_id


class AnalysisRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_request(self, request: AnalysisRequest) -> AnalysisRequest:
        return await save_with_public_id(
            self.session,
            request,
            "analysis_request_id",
            "analysis_request",
        )

    async def save_content(self, content: AnalysisContent) -> AnalysisContent:
        return await save_with_public_id(
            self.session,
            content,
            "analysis_content_id",
            "analysis_content",
        )

    async def save_result(self, result: AnalysisResult) -> AnalysisResult:
        return await save_with_public_id(
            self.session,
            result,
            "analysis_result_id",
            "analysis_result",
        )
