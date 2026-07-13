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


class AIClientError(RuntimeError):
    pass


class AIClientUnavailableError(RuntimeError):
    pass


class AIClientResponseError(AIClientError):
    pass


class AIClient:
    def __init__(
        self,
        api_key: str | None = settings.openai_api_key,
        model: str = settings.openai_model,
        timeout_seconds: int = settings.openai_request_timeout_seconds,
        openai_client: object | None = None,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.openai_client = openai_client

    @property
    def is_enabled(self) -> bool:
        return bool(self.api_key)

    async def classify_content(
        self,
        analysis_input: AnalysisInput,
    ) -> ClassificationResult:
        self._ensure_enabled()
        response_content = await self._create_json_response(
            system_prompt=CLASSIFICATION_SYSTEM_PROMPT,
            user_prompt=build_classification_user_prompt(analysis_input),
        )
        try:
            return ClassificationResult.model_validate_json(response_content)
        except ValueError as exc:
            raise AIClientResponseError("Invalid classification response.") from exc

    async def detect_duplicate(
        self,
        target: DuplicateCandidate,
        candidates: list[DuplicateCandidate],
    ) -> DuplicateResult:
        self._ensure_enabled()
        response_content = await self._create_json_response(
            system_prompt=DUPLICATE_DETECTION_SYSTEM_PROMPT,
            user_prompt=build_duplicate_detection_user_prompt(target, candidates),
        )
        try:
            return DuplicateResult.model_validate_json(response_content)
        except ValueError as exc:
            raise AIClientResponseError(
                "Invalid duplicate detection response.",
            ) from exc

    def _ensure_enabled(self) -> None:
        if not self.is_enabled:
            raise AIClientUnavailableError("OPENAI_API_KEY is not configured.")

    async def _create_json_response(self, system_prompt: str, user_prompt: str) -> str:
        client = self._client()
        response = await client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        content = response.choices[0].message.content
        if not content:
            raise AIClientResponseError("OpenAI response content is empty.")
        return content

    def _client(self) -> object:
        if self.openai_client is not None:
            return self.openai_client

        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise AIClientUnavailableError("OpenAI SDK is not installed.") from exc

        self.openai_client = AsyncOpenAI(
            api_key=self.api_key,
            timeout=self.timeout_seconds,
        )
        return self.openai_client
