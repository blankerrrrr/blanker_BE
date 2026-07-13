from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analysis import AnalysisContent, AnalysisRequest, AnalysisResult


class AnalysisRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_request(self, request: AnalysisRequest) -> AnalysisRequest:
        self.session.add(request)
        await self.session.flush()
        await self.session.refresh(request)
        return request

    async def save_content(self, content: AnalysisContent) -> AnalysisContent:
        self.session.add(content)
        await self.session.flush()
        await self.session.refresh(content)
        return content

    async def save_result(self, result: AnalysisResult) -> AnalysisResult:
        self.session.add(result)
        await self.session.flush()
        await self.session.refresh(result)
        return result
