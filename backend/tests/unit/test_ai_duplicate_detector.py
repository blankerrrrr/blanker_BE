from app.ai.duplicate_detector import DuplicateDetector
from app.ai.schemas import DuplicateCandidate


def test_duplicate_detector_matches_same_url() -> None:
    detector = DuplicateDetector()

    result = detector.detect(
        DuplicateCandidate(source_id="target", url="https://example.com/a"),
        [DuplicateCandidate(source_id="candidate", url="https://example.com/a")],
    )

    assert result.is_duplicate is True
    assert result.representative_id == "candidate"
    assert result.score == 1.0


def test_duplicate_detector_matches_similar_text() -> None:
    detector = DuplicateDetector()

    result = detector.detect(
        DuplicateCandidate(source_id="target", title="작품A 엔딩 해석", summary="요약"),
        [
            DuplicateCandidate(
                source_id="candidate",
                title="작품A 엔딩 해석",
                summary="요약",
            ),
        ],
    )

    assert result.is_duplicate is True
    assert result.representative_id == "candidate"


def test_duplicate_detector_ignores_low_similarity_text() -> None:
    detector = DuplicateDetector()

    result = detector.detect(
        DuplicateCandidate(source_id="target", title="작품A 엔딩"),
        [DuplicateCandidate(source_id="candidate", title="전혀 다른 글")],
    )

    assert result.is_duplicate is False
    assert result.representative_id is None
