from app.ai.prompts import (
    CLASSIFICATION_SYSTEM_PROMPT,
    DUPLICATE_DETECTION_SYSTEM_PROMPT,
    build_classification_user_prompt,
    build_duplicate_detection_user_prompt,
)
from app.ai.schemas import AnalysisInput, DuplicateCandidate
from app.schemas.analysis import ContentUnitType


def test_classification_system_prompt_requires_json_enum_response() -> None:
    assert "Return only JSON" in CLASSIFICATION_SYSTEM_PROMPT
    assert "SPOILER" in CLASSIFICATION_SYSTEM_PROMPT
    assert "HIGH" in CLASSIFICATION_SYSTEM_PROMPT


def test_build_classification_user_prompt_sorts_interest_terms() -> None:
    prompt = build_classification_user_prompt(
        AnalysisInput(
            clientContentId="content_1",
            unitType=ContentUnitType.TEXT,
            text="엔딩 스포일러",
            interestTerms={"작품B", "작품A"},
        ),
    )

    assert "clientContentId: content_1" in prompt
    assert "unitType: TEXT" in prompt
    assert "interestTerms: 작품A, 작품B" in prompt
    assert "엔딩 스포일러" in prompt


def test_duplicate_system_prompt_requires_score_range() -> None:
    assert "Return only JSON" in DUPLICATE_DETECTION_SYSTEM_PROMPT
    assert "0 to 1" in DUPLICATE_DETECTION_SYSTEM_PROMPT


def test_build_duplicate_detection_user_prompt_lists_candidates() -> None:
    prompt = build_duplicate_detection_user_prompt(
        DuplicateCandidate(sourceId="target", title="작품"),
        [
            DuplicateCandidate(sourceId="candidate_1", title="작품", summary="같은 글"),
            DuplicateCandidate(sourceId="candidate_2", title="다른 작품"),
        ],
    )

    assert "targetSourceId: target" in prompt
    assert "- sourceId: candidate_1, text: 작품 같은 글" in prompt
    assert "- sourceId: candidate_2, text: 다른 작품" in prompt
