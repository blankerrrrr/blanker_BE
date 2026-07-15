from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.client import AIClient, AIClientError, AIClientUnavailableError
from app.ai.content_classifier import RuleBasedContentClassifier
from app.ai.schemas import AnalysisInput, ClassificationResult
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
)

MAX_CONTENTS = 50
MAX_TEXT_LENGTH = 20_000


class AnalysisService:
    def __init__(
        self,
        session: AsyncSession,
        ai_client: AIClient | None = None,
    ) -> None:
        self.session = session
        self.analysis = AnalysisRepository(session)
        self.interest_targets = InterestTargetRepository(session)
        self.ai_client = ai_client or AIClient()
        self.classifier = RuleBasedContentClassifier()

    # 분석 요청을 저장하고 각 콘텐츠의 차단 판단 결과를 반환한다.
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

    # 요청 콘텐츠 개수와 전체 텍스트 길이가 허용 범위인지 검증한다.
    def _validate_request_size(self, request: AnalysisRequestCreate) -> None:
        if len(request.contents) > MAX_CONTENTS:
            raise AppException(ErrorCode.ANALYSIS_CONTENT_TOO_LARGE)

        total_length = sum(
            len(self._content_text(content)) for content in request.contents
        )
        if total_length > MAX_TEXT_LENGTH:
            raise AppException(ErrorCode.ANALYSIS_CONTENT_TOO_LARGE)

    # 사용자의 관심 대상 이름, 별칭, 키워드를 분석용 검색어로 불러온다.
    async def _load_interest_terms(self, user_id: str) -> set[str]:
        targets = await self.interest_targets.find_all_by_user_id(user_id)
        terms: set[str] = set()
        for target in targets:
            terms.add(target.name)
            terms.update(target.aliases)
            terms.update(target.keywords)
        return terms

    # 분석 요청에 포함된 개별 콘텐츠 원본을 저장한다.
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

    # 저장된 콘텐츠를 분류하고 분석 결과와 응답 DTO를 생성한다.
    async def _analyze_content(
        self,
        content: AnalysisContent,
        request: AnalysisContentRequest,
        interest_terms: set[str],
    ) -> AnalysisResultResponse:
        classification = await self._classify(request, interest_terms)
        should_block = classification.should_block

        await self.analysis.save_result(
            AnalysisResult(
                analysis_content_id=content.analysis_content_id,
                categories=[category.value for category in classification.categories],
                risk_level=classification.risk_level.value,
                relevance_level=classification.relevance_level.value,
                should_block=should_block,
                block_reason=classification.reason,
                related_topics=classification.related_topics,
            ),
        )

        return AnalysisResultResponse(
            client_content_id=request.client_content_id,
            categories=classification.categories,
            risk_level=classification.risk_level,
            relevance_level=classification.relevance_level,
            should_block=should_block,
            block_action=BlockActionResponse(
                unit_type=request.unit_type,
                reason=(
                    classification.reason
                    or "차단이 필요한 콘텐츠로 판단되었습니다."
                ),
                related_topics=classification.related_topics,
            )
            if should_block
            else None,
        )

    async def _classify(
        self,
        request: AnalysisContentRequest,
        interest_terms: set[str],
    ) -> ClassificationResult:
        analysis_input = AnalysisInput(
            client_content_id=request.client_content_id,
            unit_type=request.unit_type,
            text=request.text,
            image_url=request.image_url,
            alt_text=request.alt_text,
            context_text=request.context_text,
            selector=request.selector,
            interest_terms=interest_terms,
        )
        try:
            return await self.ai_client.classify_content(analysis_input)
        except (AIClientError, AIClientUnavailableError):
            categories, risk_level, relevance_level, related_topics, reason = (
                self.classifier.classify(analysis_input.content_text, interest_terms)
            )
            return ClassificationResult(
                categories=categories,
                risk_level=risk_level,
                relevance_level=relevance_level,
                related_topics=related_topics,
                reason=reason,
            )

    # 콘텐츠의 텍스트 필드를 분석 가능한 하나의 문자열로 합친다.
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
