from app.ai.risk_evaluator import RiskEvaluator
from app.schemas.analysis import BlockCategory, RelevanceLevel, RiskLevel

SPOILER_KEYWORDS = ("spoiler", "스포", "결말", "반전", "사망", "엔딩")
HARMFUL_KEYWORDS = ("혐오", "폭력", "자해", "살해", "잔인", "유해")


class RuleBasedContentClassifier:
    def __init__(self, risk_evaluator: RiskEvaluator | None = None) -> None:
        self.risk_evaluator = risk_evaluator or RiskEvaluator()

    def classify(
        self,
        content_text: str,
        interest_terms: set[str],
    ) -> tuple[list[BlockCategory], RiskLevel, RelevanceLevel, list[str], str | None]:
        normalized_text = content_text.casefold()
        related_topics = [
            term
            for term in interest_terms
            if term and term.casefold() in normalized_text
        ]

        categories: list[BlockCategory] = []
        if related_topics:
            categories.append(BlockCategory.INTEREST)

        has_spoiler = any(keyword in normalized_text for keyword in SPOILER_KEYWORDS)
        has_harmful = any(keyword in normalized_text for keyword in HARMFUL_KEYWORDS)
        if has_spoiler:
            categories.append(BlockCategory.SPOILER)
        if has_harmful:
            categories.append(BlockCategory.HARMFUL)

        relevance_level = self.risk_evaluator.evaluate_relevance(related_topics)
        risk_level = self.risk_evaluator.evaluate_risk(
            has_spoiler=has_spoiler,
            has_harmful=has_harmful,
            relevance_level=relevance_level,
        )
        reason = self.risk_evaluator.block_reason(categories, related_topics)
        return categories, risk_level, relevance_level, related_topics, reason
