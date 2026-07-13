from app.ai.content_classifier import RuleBasedContentClassifier
from app.ai.duplicate_detector import DuplicateDetector
from app.ai.schemas import (
    AnalysisInput,
    ClassificationResult,
    DuplicateCandidate,
    DuplicateResult,
)


class AnalysisPipeline:
    def __init__(
        self,
        classifier: RuleBasedContentClassifier | None = None,
        duplicate_detector: DuplicateDetector | None = None,
    ) -> None:
        self.classifier = classifier or RuleBasedContentClassifier()
        self.duplicate_detector = duplicate_detector or DuplicateDetector()

    def classify(self, analysis_input: AnalysisInput) -> ClassificationResult:
        categories, risk_level, relevance_level, related_topics, reason = (
            self.classifier.classify(
                analysis_input.content_text,
                analysis_input.interest_terms,
            )
        )
        return ClassificationResult(
            categories=categories,
            riskLevel=risk_level,
            relevanceLevel=relevance_level,
            relatedTopics=related_topics,
            reason=reason,
        )

    def detect_duplicate(
        self,
        target: DuplicateCandidate,
        candidates: list[DuplicateCandidate],
    ) -> DuplicateResult:
        return self.duplicate_detector.detect(target, candidates)
