from app.ai.schemas import AnalysisInput, ClassificationResult, DuplicateCandidate
from app.schemas.analysis import (
    BlockCategory,
    ContentUnitType,
    RelevanceLevel,
    RiskLevel,
)


def test_analysis_input_builds_content_text_from_available_fields() -> None:
    analysis_input = AnalysisInput(
        client_content_id="content_1",
        unit_type=ContentUnitType.TEXT,
        text="본문",
        alt_text="대체 텍스트",
        context_text="주변 문맥",
        image_url="https://example.com/image.png",
    )

    assert analysis_input.content_text == (
        "본문 대체 텍스트 주변 문맥 https://example.com/image.png"
    )


def test_classification_result_blocks_high_risk_content() -> None:
    result = ClassificationResult(
        categories=[BlockCategory.HARMFUL],
        risk_level=RiskLevel.HIGH,
        relevance_level=RelevanceLevel.LOW,
    )

    assert result.should_block is True


def test_classification_result_blocks_medium_risk_related_content() -> None:
    result = ClassificationResult(
        categories=[BlockCategory.SPOILER],
        risk_level=RiskLevel.MEDIUM,
        relevance_level=RelevanceLevel.MEDIUM,
    )

    assert result.should_block is True


def test_classification_result_does_not_block_medium_risk_unrelated_content() -> None:
    result = ClassificationResult(
        categories=[BlockCategory.SPOILER],
        risk_level=RiskLevel.MEDIUM,
        relevance_level=RelevanceLevel.LOW,
    )

    assert result.should_block is False


def test_duplicate_candidate_builds_searchable_text() -> None:
    candidate = DuplicateCandidate(
        source_id="source_1",
        title="작품 제목",
        summary="요약",
        related_topics=["주인공", "엔딩"],
    )

    assert candidate.searchable_text == "작품 제목 요약 주인공 엔딩"
