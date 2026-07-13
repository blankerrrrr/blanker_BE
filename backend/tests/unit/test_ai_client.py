from types import SimpleNamespace

import pytest

from app.ai.client import AIClient, AIClientResponseError, AIClientUnavailableError
from app.ai.schemas import AnalysisInput, DuplicateCandidate
from app.schemas.analysis import ContentUnitType, RelevanceLevel, RiskLevel


class FakeCompletions:
    def __init__(self, content: str | None) -> None:
        self.content = content
        self.last_request: dict[str, object] | None = None

    async def create(self, **kwargs: object) -> object:
        self.last_request = kwargs
        return SimpleNamespace(
            choices=[
                SimpleNamespace(message=SimpleNamespace(content=self.content)),
            ],
        )


class FakeOpenAIClient:
    def __init__(self, content: str | None) -> None:
        self.completions = FakeCompletions(content)
        self.chat = SimpleNamespace(completions=self.completions)


def test_ai_client_is_disabled_without_api_key() -> None:
    client = AIClient(api_key=None)

    assert client.is_enabled is False


def test_ai_client_is_enabled_with_api_key() -> None:
    client = AIClient(api_key="test-key")

    assert client.is_enabled is True


@pytest.mark.asyncio
async def test_classify_content_fails_when_api_key_is_missing() -> None:
    client = AIClient(api_key=None)

    with pytest.raises(AIClientUnavailableError, match="OPENAI_API_KEY"):
        await client.classify_content(
            AnalysisInput(
                client_content_id="content_1",
                unit_type=ContentUnitType.TEXT,
                text="본문",
            ),
        )


@pytest.mark.asyncio
async def test_classify_content_uses_openai_json_response() -> None:
    openai_client = FakeOpenAIClient(
        """
        {
          "categories": ["SPOILER"],
          "riskLevel": "MEDIUM",
          "relevanceLevel": "LOW",
          "relatedTopics": [],
          "reason": "스포일러 가능성이 있습니다."
        }
        """,
    )
    client = AIClient(api_key="test-key", openai_client=openai_client)

    result = await client.classify_content(
        AnalysisInput(
            client_content_id="content_1",
            unit_type=ContentUnitType.TEXT,
            text="본문",
        ),
    )

    assert result.risk_level == RiskLevel.MEDIUM
    assert result.relevance_level == RelevanceLevel.LOW
    assert result.related_topics == []
    assert openai_client.completions.last_request is not None
    assert openai_client.completions.last_request["response_format"] == {
        "type": "json_object",
    }


@pytest.mark.asyncio
async def test_detect_duplicate_uses_openai_json_response() -> None:
    openai_client = FakeOpenAIClient(
        """
        {
          "isDuplicate": true,
          "representativeId": "candidate",
          "score": 0.91,
          "reason": "같은 출처입니다."
        }
        """,
    )
    client = AIClient(api_key="test-key", openai_client=openai_client)

    result = await client.detect_duplicate(
        DuplicateCandidate(source_id="target", title="작품"),
        [DuplicateCandidate(source_id="candidate", title="작품")],
    )

    assert result.is_duplicate is True
    assert result.representative_id == "candidate"
    assert result.score == 0.91


@pytest.mark.asyncio
async def test_classify_content_fails_when_response_is_invalid() -> None:
    client = AIClient(
        api_key="test-key",
        openai_client=FakeOpenAIClient("""{"riskLevel": "UNKNOWN"}"""),
    )

    with pytest.raises(AIClientResponseError, match="Invalid classification"):
        await client.classify_content(
            AnalysisInput(
                client_content_id="content_1",
                unit_type=ContentUnitType.TEXT,
                text="본문",
            ),
        )
