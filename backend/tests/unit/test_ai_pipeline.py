from app.ai.pipeline import AnalysisPipeline
from app.ai.schemas import AnalysisInput, DuplicateCandidate
from app.schemas.analysis import (
    BlockCategory,
    ContentUnitType,
    RelevanceLevel,
    RiskLevel,
)


def test_analysis_pipeline_classifies_content() -> None:
    pipeline = AnalysisPipeline()

    result = pipeline.classify(
        AnalysisInput(
            clientContentId="content_1",
            unitType=ContentUnitType.TEXT,
            text="작품A 결말",
            interestTerms={"작품A"},
        ),
    )

    assert result.categories == [BlockCategory.INTEREST, BlockCategory.SPOILER]
    assert result.risk_level == RiskLevel.HIGH
    assert result.relevance_level == RelevanceLevel.MEDIUM
    assert result.related_topics == ["작품A"]
    assert result.should_block is True


def test_analysis_pipeline_detects_duplicate() -> None:
    pipeline = AnalysisPipeline()

    result = pipeline.detect_duplicate(
        DuplicateCandidate(sourceId="target", url="https://example.com/a"),
        [DuplicateCandidate(sourceId="candidate", url="https://example.com/a")],
    )

    assert result.is_duplicate is True
    assert result.representative_id == "candidate"
