from app.schemas.analysis import BlockCategory, RelevanceLevel, RiskLevel


class RiskEvaluator:
    @staticmethod
    def evaluate_relevance(related_topics: list[str]) -> RelevanceLevel:
        if len(related_topics) >= 2:
            return RelevanceLevel.HIGH
        if related_topics:
            return RelevanceLevel.MEDIUM
        return RelevanceLevel.LOW

    @staticmethod
    def evaluate_risk(
            *,
        has_spoiler: bool,
        has_harmful: bool,
        relevance_level: RelevanceLevel,
    ) -> RiskLevel:
        if has_harmful or (has_spoiler and relevance_level != RelevanceLevel.LOW):
            return RiskLevel.HIGH
        if has_spoiler or relevance_level == RelevanceLevel.HIGH:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    @staticmethod
    def block_reason(
            categories: list[BlockCategory],
        related_topics: list[str],
    ) -> str | None:
        if BlockCategory.SPOILER in categories:
            return "등록한 관심 대상과 관련된 스포일러 가능성이 높습니다."
        if BlockCategory.HARMFUL in categories:
            return "유해하거나 민감한 콘텐츠로 판단되었습니다."
        if BlockCategory.INTEREST in categories and related_topics:
            return "등록한 관심 대상과 관련된 콘텐츠입니다."
        return None
