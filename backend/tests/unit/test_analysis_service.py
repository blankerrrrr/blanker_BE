import pytest

from app.ai.client import AIClientUnavailableError
from app.ai.schemas import AnalysisInput, ClassificationResult
from app.schemas.analysis import (
    AnalysisContentRequest,
    BlockCategory,
    ContentUnitType,
    RelevanceLevel,
    RiskLevel,
)
from app.services.analysis_service import AnalysisService
from app.services.screenshot_analysis_service import ScreenshotAnalysisService


class FakeAIClient:
    def __init__(self) -> None:
        self.last_input: AnalysisInput | None = None

    async def classify_content(
        self,
        analysis_input: AnalysisInput,
    ) -> ClassificationResult:
        self.last_input = analysis_input
        return ClassificationResult(
            categories=[BlockCategory.SPOILER],
            risk_level=RiskLevel.HIGH,
            relevance_level=RelevanceLevel.HIGH,
            related_topics=["작품A"],
            reason="AI가 스포일러로 분류했습니다.",
        )


class UnavailableAIClient:
    async def classify_content(
        self,
        analysis_input: AnalysisInput,
    ) -> ClassificationResult:
        raise AIClientUnavailableError("AI unavailable")


@pytest.mark.asyncio
async def test_analysis_service_uses_ai_classification() -> None:
    ai_client = FakeAIClient()
    service = AnalysisService(object(), ai_client=ai_client)
    request = AnalysisContentRequest(
        client_content_id="content_1",
        unit_type=ContentUnitType.TEXT,
        text="본문",
        alt_text="대체 텍스트",
    )

    result = await service._classify(request, {"작품A"})

    assert result.risk_level == RiskLevel.HIGH
    assert ai_client.last_input is not None
    assert ai_client.last_input.text == "본문"
    assert ai_client.last_input.alt_text == "대체 텍스트"
    assert ai_client.last_input.interest_terms == {"작품A"}


@pytest.mark.asyncio
async def test_screenshot_analysis_service_uses_ai_classification() -> None:
    ai_client = FakeAIClient()
    service = ScreenshotAnalysisService(object(), ai_client=ai_client)

    result = await service._classify("OCR 본문", {"작품A"})

    assert result.should_block is True
    assert ai_client.last_input is not None
    assert ai_client.last_input.client_content_id == "screenshot"
    assert ai_client.last_input.text == "OCR 본문"


@pytest.mark.asyncio
async def test_analysis_service_falls_back_when_ai_is_unavailable() -> None:
    service = AnalysisService(object(), ai_client=UnavailableAIClient())
    request = AnalysisContentRequest(
        client_content_id="content_1",
        unit_type=ContentUnitType.TEXT,
        text="작품A 결말",
    )

    result = await service._classify(request, {"작품A"})

    assert result.categories == [BlockCategory.INTEREST, BlockCategory.SPOILER]
    assert result.should_block is True
