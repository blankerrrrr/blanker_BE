from app.ai.prompts import (
    CLASSIFICATION_SYSTEM_PROMPT,
    DUPLICATE_DETECTION_SYSTEM_PROMPT,
    build_classification_user_prompt,
    build_duplicate_detection_user_prompt,
)
from app.ai.schemas import (
    AnalysisInput,
    ClassificationResult,
    DuplicateCandidate,
    DuplicateResult,
)
from app.core.config import settings


class AIClientUnavailableError(RuntimeError):
    pass


class AIClient:
    def __init__(
        self,
        api_key: str | None = settings.openai_api_key,
        timeout_seconds: int = settings.openai_request_timeout_seconds,
    ) -> None:
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    @property
    def is_enabled(self) -> bool:
        return bool(self.api_key)

    async def classify_content(
        self,
        analysis_input: AnalysisInput,
    ) -> ClassificationResult:
        self._ensure_enabled()
        _ = (
            CLASSIFICATION_SYSTEM_PROMPT,
            build_classification_user_prompt(analysis_input),
        )
        raise AIClientUnavailableError("OpenAI SDK integration is not implemented.")

    async def detect_duplicate(
        self,
        target: DuplicateCandidate,
        candidates: list[DuplicateCandidate],
    ) -> DuplicateResult:
        self._ensure_enabled()
        _ = (
            DUPLICATE_DETECTION_SYSTEM_PROMPT,
            build_duplicate_detection_user_prompt(target, candidates),
        )
        raise AIClientUnavailableError("OpenAI SDK integration is not implemented.")

    def _ensure_enabled(self) -> None:
        if not self.is_enabled:
            raise AIClientUnavailableError("OPENAI_API_KEY is not configured.")
