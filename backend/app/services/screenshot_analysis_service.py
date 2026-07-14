from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.content_classifier import RuleBasedContentClassifier
from app.core.ocr import extract_text
from app.db.models.analysis import AnalysisContent, AnalysisRequest, AnalysisResult
from app.db.repositories.analysis_repository import AnalysisRepository
from app.db.repositories.interest_target_repository import InterestTargetRepository
from app.schemas.analysis import (
    BlockActionResponse,
    ContentUnitType,
    RelevanceLevel,
    RiskLevel,
)
from app.schemas.screenshot_analysis import (
    ScreenshotAnalysisRequestCreate,
    ScreenshotAnalysisRequestResponse,
)

_SCREENSHOT_CLIENT_CONTENT_ID = "screenshot"


class ScreenshotAnalysisService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.analysis = AnalysisRepository(session)
        self.interest_targets = InterestTargetRepository(session)
        self.classifier = RuleBasedContentClassifier()

    async def analyze(
        self,
        user_id: str,
        request: ScreenshotAnalysisRequestCreate,
    ) -> ScreenshotAnalysisRequestResponse:
        extracted_text = await extract_text(request.image_bytes)

        interest_terms = await self._load_interest_terms(user_id)

        analysis_request = await self.analysis.save_request(
            AnalysisRequest(
                user_id=user_id,
                page_url=request.url,
                page_title=request.title,
            ),
        )

        content = await self.analysis.save_content(
            AnalysisContent(
                analysis_request_id=analysis_request.analysis_request_id,
                client_content_id=_SCREENSHOT_CLIENT_CONTENT_ID,
                unit_type=ContentUnitType.TEXT.value,
                text=extracted_text,
            ),
        )

        categories, risk_level, relevance_level, related_topics, reason = (
            self.classifier.classify(extracted_text, interest_terms)
        )
        should_block = risk_level == RiskLevel.HIGH or (
            risk_level == RiskLevel.MEDIUM and relevance_level != RelevanceLevel.LOW
        )

        await self.analysis.save_result(
            AnalysisResult(
                analysis_content_id=content.analysis_content_id,
                categories=[c.value for c in categories],
                risk_level=risk_level.value,
                relevance_level=relevance_level.value,
                should_block=should_block,
                block_reason=reason,
                related_topics=related_topics,
            ),
        )

        await self.session.commit()
        return ScreenshotAnalysisRequestResponse(
            analysis_request_id=analysis_request.analysis_request_id,
            extracted_text=extracted_text,
            categories=categories,
            risk_level=risk_level,
            relevance_level=relevance_level,
            should_block=should_block,
            block_action=BlockActionResponse(
                unit_type=ContentUnitType.TEXT,
                reason=reason or "차단이 필요한 콘텐츠로 판단되었습니다.",
                related_topics=related_topics,
            )
            if should_block
            else None,
        )

    async def _load_interest_terms(self, user_id: str) -> set[str]:
        targets = await self.interest_targets.find_all_by_user_id(user_id)
        terms: set[str] = set()
        for target in targets:
            terms.add(target.name)
            terms.update(target.aliases)
            terms.update(target.keywords)
        return terms
