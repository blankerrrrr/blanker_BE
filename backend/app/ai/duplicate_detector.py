import re
from difflib import SequenceMatcher

from app.ai.schemas import DuplicateCandidate, DuplicateResult

DUPLICATE_SCORE_THRESHOLD = 0.86


class DuplicateDetector:
    def detect(
        self,
        target: DuplicateCandidate,
        candidates: list[DuplicateCandidate],
    ) -> DuplicateResult:
        best_candidate: DuplicateCandidate | None = None
        best_score = 0.0

        for candidate in candidates:
            score = self._score(target, candidate)
            if score > best_score:
                best_candidate = candidate
                best_score = score

        if best_candidate is None or best_score < DUPLICATE_SCORE_THRESHOLD:
            return DuplicateResult(isDuplicate=False, score=best_score)

        return DuplicateResult(
            isDuplicate=True,
            representativeId=best_candidate.source_id,
            score=best_score,
            reason="유사한 제목, URL 또는 본문 요약이 이미 등록되어 있습니다.",
        )

    def _score(
        self,
        target: DuplicateCandidate,
        candidate: DuplicateCandidate,
    ) -> float:
        if target.url and candidate.url and target.url == candidate.url:
            return 1.0

        target_text = self._normalize(target.searchable_text)
        candidate_text = self._normalize(candidate.searchable_text)
        if not target_text or not candidate_text:
            return 0.0

        return SequenceMatcher(None, target_text, candidate_text).ratio()

    def _normalize(self, value: str) -> str:
        return re.sub(r"\s+", " ", value.casefold()).strip()
