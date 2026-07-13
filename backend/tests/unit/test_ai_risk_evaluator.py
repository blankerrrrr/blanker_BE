from app.ai.content_classifier import RuleBasedContentClassifier
from app.ai.risk_evaluator import RiskEvaluator
from app.schemas.analysis import BlockCategory, RelevanceLevel, RiskLevel


def test_risk_evaluator_marks_multiple_related_topics_high_relevance() -> None:
    evaluator = RiskEvaluator()

    assert evaluator.evaluate_relevance(["작품A", "인물B"]) == RelevanceLevel.HIGH


def test_risk_evaluator_marks_related_spoiler_high_risk() -> None:
    evaluator = RiskEvaluator()

    assert (
        evaluator.evaluate_risk(
            has_spoiler=True,
            has_harmful=False,
            relevance_level=RelevanceLevel.MEDIUM,
        )
        == RiskLevel.HIGH
    )


def test_risk_evaluator_marks_unrelated_spoiler_medium_risk() -> None:
    evaluator = RiskEvaluator()

    assert (
        evaluator.evaluate_risk(
            has_spoiler=True,
            has_harmful=False,
            relevance_level=RelevanceLevel.LOW,
        )
        == RiskLevel.MEDIUM
    )


def test_risk_evaluator_returns_spoiler_reason_first() -> None:
    evaluator = RiskEvaluator()

    assert evaluator.block_reason(
        [BlockCategory.HARMFUL, BlockCategory.SPOILER],
        ["작품A"],
    ) == "등록한 관심 대상과 관련된 스포일러 가능성이 높습니다."


def test_rule_based_classifier_uses_risk_evaluator_result() -> None:
    classifier = RuleBasedContentClassifier()

    categories, risk_level, relevance_level, related_topics, reason = (
        classifier.classify("작품A 엔딩", {"작품A"})
    )

    assert categories == [BlockCategory.INTEREST, BlockCategory.SPOILER]
    assert risk_level == RiskLevel.HIGH
    assert relevance_level == RelevanceLevel.MEDIUM
    assert related_topics == ["작품A"]
    assert reason == "등록한 관심 대상과 관련된 스포일러 가능성이 높습니다."
