import pytest

from app.ai.client import AIClient, AIClientUnavailableError
from app.ai.schemas import AnalysisInput, DuplicateCandidate
from app.schemas.analysis import ContentUnitType


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
                clientContentId="content_1",
                unitType=ContentUnitType.TEXT,
                text="본문",
            ),
        )


@pytest.mark.asyncio
async def test_detect_duplicate_fails_when_sdk_is_not_implemented() -> None:
    client = AIClient(api_key="test-key")

    with pytest.raises(AIClientUnavailableError, match="SDK integration"):
        await client.detect_duplicate(
            DuplicateCandidate(sourceId="target", title="작품"),
            [DuplicateCandidate(sourceId="candidate", title="작품")],
        )
