from app.ai.schemas import AnalysisInput, DuplicateCandidate

CLASSIFICATION_SYSTEM_PROMPT = """
You are a content safety assistant for a spoiler and harmful-content blocker.
Return only JSON with categories, riskLevel, relevanceLevel, relatedTopics, and reason.
Use the existing enum values: SPOILER, HARMFUL, INTEREST, LOW, MEDIUM, HIGH.
""".strip()

DUPLICATE_DETECTION_SYSTEM_PROMPT = """
You are a duplicate source detector.
Return only JSON with isDuplicate, representativeId, score, and reason.
Score must be a number from 0 to 1.
""".strip()


def build_classification_user_prompt(analysis_input: AnalysisInput) -> str:
    interest_terms = ", ".join(sorted(analysis_input.interest_terms)) or "없음"
    content_text = analysis_input.content_text or "없음"
    return "\n".join(
        (
            f"clientContentId: {analysis_input.client_content_id}",
            f"unitType: {analysis_input.unit_type.value}",
            f"interestTerms: {interest_terms}",
            "content:",
            content_text,
        ),
    )


def build_duplicate_detection_user_prompt(
    target: DuplicateCandidate,
    candidates: list[DuplicateCandidate],
) -> str:
    candidate_lines = [
        (
            f"- sourceId: {candidate.source_id}, "
            f"text: {candidate.searchable_text or '없음'}"
        )
        for candidate in candidates
    ]
    candidates_text = "\n".join(candidate_lines) or "없음"
    return "\n".join(
        (
            f"targetSourceId: {target.source_id}",
            f"targetText: {target.searchable_text or '없음'}",
            "candidates:",
            candidates_text,
        ),
    )
