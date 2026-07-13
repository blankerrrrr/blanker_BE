from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.content_classifier import RuleBasedContentClassifier
from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.db.models.analysis import AnalysisContent, AnalysisRequest, AnalysisResult
from app.db.repositories.analysis_repository import AnalysisRepository
from app.db.repositories.interest_target_repository import InterestTargetRepository
from app.schemas.analysis import (
    AnalysisContentRequest,
    AnalysisRequestCreate,
    AnalysisRequestResponse,
    AnalysisResultResponse,
    BlockActionResponse,
    RelevanceLevel,
    RiskLevel,
)

MAX_CONTENTS = 50
MAX_TEXT_LENGTH = 20_000


class AnalysisService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.analysis = AnalysisRepository(session)
        self.interest_targets = InterestTargetRepository(session)
        self.classifier = RuleBasedContentClassifier()

    async def analyze(
        self,
        user_id: str,
        request: AnalysisRequestCreate,
    ) -> AnalysisRequestResponse:
        self._validate_request_size(request)
        interest_terms = await self._load_interest_terms(user_id)

        analysis_request = await self.analysis.save_request(
            AnalysisRequest(
                user_id=user_id,
                page_url=request.page.url,
                page_title=request.page.title,
            ),
        )

        responses: list[AnalysisResultResponse] = []
        for content_request in request.contents:
            content = await self._save_content(
                analysis_request.analysis_request_id,
                content_request,
            )
            response = await self._analyze_content(
                content,
                content_request,
                interest_terms,
            )
            responses.append(response)

        await self.session.commit()
        return AnalysisRequestResponse(
            analysis_request_id=analysis_request.analysis_request_id,
            results=responses,
        )

    def _validate_request_size(self, request: AnalysisRequestCreate) -> None:
        if len(request.contents) > MAX_CONTENTS:
            raise AppException(ErrorCode.ANALYSIS_CONTENT_TOO_LARGE)

        total_length = sum(
            len(self._content_text(content)) for content in request.contents
        )
        if total_length > MAX_TEXT_LENGTH:
            raise AppException(ErrorCode.ANALYSIS_CONTENT_TOO_LARGE)

    async def _load_interest_terms(self, user_id: str) -> set[str]:
        targets = await self.interest_targets.find_all_by_user_id(user_id)
        terms: set[str] = set()
        for target in targets:
            terms.add(target.name)
            terms.update(target.aliases)
            terms.update(target.keywords)
        return terms

    async def _save_content(
        self,
        analysis_request_id: str,
        request: AnalysisContentRequest,
    ) -> AnalysisContent:
        return await self.analysis.save_content(
            AnalysisContent(
                analysis_request_id=analysis_request_id,
                client_content_id=request.client_content_id,
                unit_type=request.unit_type.value,
                text=request.text,
                image_url=request.image_url,
                alt_text=request.alt_text,
                context_text=request.context_text,
                selector=request.selector,
            ),
        )

    async def _analyze_content(
        self,
        content: AnalysisContent,
        request: AnalysisContentRequest,
        interest_terms: set[str],
    ) -> AnalysisResultResponse:
        categories, risk_level, relevance_level, related_topics, reason = (
            self.classifier.classify(self._content_text(request), interest_terms)
        )
        should_block = risk_level == RiskLevel.HIGH or (
            risk_level == RiskLevel.MEDIUM
            and relevance_level != RelevanceLevel.LOW
        )

        await self.analysis.save_result(
            AnalysisResult(
                analysis_content_id=content.analysis_content_id,
                categories=[category.value for category in categories],
                risk_level=risk_level.value,
                relevance_level=relevance_level.value,
                should_block=should_block,
                block_reason=reason,
                related_topics=related_topics,
            ),
        )

        return AnalysisResultResponse(
            client_content_id=request.client_content_id,
            categories=categories,
            risk_level=risk_level,
            relevance_level=relevance_level,
            should_block=should_block,
            block_action=BlockActionResponse(
                unit_type=request.unit_type,
                reason=reason or "차단이 필요한 콘텐츠로 판단되었습니다.",
                related_topics=related_topics,
            )
            if should_block
            else None,
        )

    @staticmethod
    def _content_text(content: AnalysisContentRequest) -> str:
        return " ".join(
            value
            for value in (
                content.text,
                content.alt_text,
                content.context_text,
                content.image_url,
            )
            if value
        )
