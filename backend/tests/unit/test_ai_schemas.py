from app.ai.schemas import AnalysisInput, ClassificationResult, DuplicateCandidate
from app.schemas.analysis import (
    BlockCategory,
    ContentUnitType,
    RelevanceLevel,
    RiskLevel,
)


def test_analysis_input_builds_content_text_from_available_fields() -> None:
    analysis_input = AnalysisInput(
        clientContentId="content_1",
        unitType=ContentUnitType.TEXT,
        text="본문",
        altText="대체 텍스트",
        contextText="주변 문맥",
        imageUrl="https://example.com/image.png",
    )

    assert analysis_input.content_text == (
        "본문 대체 텍스트 주변 문맥 https://example.com/image.png"
    )


def test_classification_result_blocks_high_risk_content() -> None:
    result = ClassificationResult(
        categories=[BlockCategory.HARMFUL],
        riskLevel=RiskLevel.HIGH,
        relevanceLevel=RelevanceLevel.LOW,
    )

    assert result.should_block is True


def test_classification_result_blocks_medium_risk_related_content() -> None:
    result = ClassificationResult(
        categories=[BlockCategory.SPOILER],
        riskLevel=RiskLevel.MEDIUM,
        relevanceLevel=RelevanceLevel.MEDIUM,
    )

    assert result.should_block is True


def test_classification_result_does_not_block_medium_risk_unrelated_content() -> None:
    result = ClassificationResult(
        categories=[BlockCategory.SPOILER],
        riskLevel=RiskLevel.MEDIUM,
        relevanceLevel=RelevanceLevel.LOW,
    )

    assert result.should_block is False


def test_duplicate_candidate_builds_searchable_text() -> None:
    candidate = DuplicateCandidate(
        sourceId="source_1",
        title="작품 제목",
        summary="요약",
        relatedTopics=["주인공", "엔딩"],
    )

    assert candidate.searchable_text == "작품 제목 요약 주인공 엔딩"
