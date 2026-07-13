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
            client_content_id="content_1",
            unit_type=ContentUnitType.TEXT,
            text="작품A 결말",
            interest_terms={"작품A"},
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
        DuplicateCandidate(source_id="target", url="https://example.com/a"),
        [DuplicateCandidate(source_id="candidate", url="https://example.com/a")],
    )

    assert result.is_duplicate is True
    assert result.representative_id == "candidate"
