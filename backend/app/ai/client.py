import asyncio
import json
import urllib.request
from typing import Any

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

DEFAULT_ANTHROPIC_MODEL = "claude-3-5-haiku-latest"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"


class AIClientError(RuntimeError):
    pass


class AIClientUnavailableError(RuntimeError):
    pass


class AIClientResponseError(AIClientError):
    pass


class AIClient:
    def __init__(
        self,
        api_key: str | None = settings.anthropic_api_key,
        timeout_seconds: int = settings.ai_request_timeout_seconds,
        anthropic_client: object | None = None,
    ) -> None:
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.anthropic_client = anthropic_client

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
            raise AIClientUnavailableError("ANTHROPIC_API_KEY is not configured.")

    async def _create_json_response(self, system_prompt: str, user_prompt: str) -> str:
        if self.anthropic_client is not None:
            response_content = await self.anthropic_client.create_message(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        else:
            response_content = await asyncio.to_thread(
                self._send_anthropic_request,
                system_prompt,
                user_prompt,
            )
        if not response_content:
            raise AIClientResponseError("Anthropic response content is empty.")
        return response_content

    def _send_anthropic_request(self, system_prompt: str, user_prompt: str) -> str:
        if self.api_key is None:
            raise AIClientUnavailableError("ANTHROPIC_API_KEY is not configured.")

        body = {
            "model": DEFAULT_ANTHROPIC_MODEL,
            "max_tokens": 1000,
            "temperature": 0,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"{user_prompt}\n\n"
                        "응답은 설명 없이 JSON 객체 문자열만 반환하세요."
                    ),
                },
            ],
        }
        request = urllib.request.Request(
            ANTHROPIC_API_URL,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": ANTHROPIC_VERSION,
                "content-type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=self.timeout_seconds,
            ) as response:
                response_body = json.loads(response.read().decode("utf-8"))
        except OSError as exc:
            raise AIClientUnavailableError("Anthropic API request failed.") from exc

        return self._extract_text(response_body)

    @staticmethod
    def _extract_text(response_body: dict[str, Any]) -> str:
        content_blocks = response_body.get("content")
        if not isinstance(content_blocks, list):
            raise AIClientResponseError("Anthropic response content is missing.")

        text_parts = [
            block.get("text", "")
            for block in content_blocks
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        return "".join(text_parts).strip()
