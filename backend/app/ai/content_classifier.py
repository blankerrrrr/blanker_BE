from app.schemas.analysis import BlockCategory, RelevanceLevel, RiskLevel

SPOILER_KEYWORDS = ("spoiler", "스포", "결말", "반전", "사망", "엔딩")
HARMFUL_KEYWORDS = ("혐오", "폭력", "자해", "살해", "잔인", "유해")


class RuleBasedContentClassifier:
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

        relevance_level = self._relevance_level(related_topics)
        risk_level = self._risk_level(has_spoiler, has_harmful, relevance_level)
        reason = self._block_reason(categories, related_topics)
        return categories, risk_level, relevance_level, related_topics, reason

    def _relevance_level(self, related_topics: list[str]) -> RelevanceLevel:
        if len(related_topics) >= 2:
            return RelevanceLevel.HIGH
        if related_topics:
            return RelevanceLevel.MEDIUM
        return RelevanceLevel.LOW

    def _risk_level(
        self,
        has_spoiler: bool,
        has_harmful: bool,
        relevance_level: RelevanceLevel,
    ) -> RiskLevel:
        if has_harmful or (has_spoiler and relevance_level != RelevanceLevel.LOW):
            return RiskLevel.HIGH
        if has_spoiler or relevance_level == RelevanceLevel.HIGH:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _block_reason(
        self,
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
