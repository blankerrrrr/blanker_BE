from collections.abc import AsyncGenerator

from fastapi.testclient import TestClient

from app.api.deps import get_current_user_id, get_db_session
from app.main import app
from app.schemas.analysis import (
    AnalysisRequestResponse,
    AnalysisResultResponse,
    BlockActionResponse,
    BlockCategory,
    ContentUnitType,
    RelevanceLevel,
    RiskLevel,
)
from app.schemas.screenshot_analysis import (
    ScreenshotAnalysisRequestCreate,
    ScreenshotAnalysisRequestResponse,
)


class FakeAnalysisService:
    def __init__(self, session: object) -> None:
        self.session = session

    async def analyze(self, user_id: str, request: object) -> AnalysisRequestResponse:
        return AnalysisRequestResponse(
            analysis_request_id="req_1",
            results=[
                AnalysisResultResponse(
                    client_content_id=request.contents[0].client_content_id,
                    categories=[],
                    risk_level=RiskLevel.LOW,
                    relevance_level=RelevanceLevel.LOW,
                    should_block=False,
                    block_action=None,
                ),
            ],
        )


class FakeScreenshotAnalysisService:
    def __init__(self, session: object) -> None:
        self.session = session

    async def analyze(
        self,
        user_id: str,
        request: ScreenshotAnalysisRequestCreate,
    ) -> ScreenshotAnalysisRequestResponse:
        return ScreenshotAnalysisRequestResponse(
            analysis_request_id="req_screenshot_1",
            extracted_text="추출된 텍스트",
            categories=[],
            risk_level=RiskLevel.LOW,
            relevance_level=RelevanceLevel.LOW,
            should_block=False,
            block_action=None,
        )


class FakeScreenshotAnalysisServiceBlocked:
    def __init__(self, session: object) -> None:
        self.session = session

    async def analyze(
        self,
        user_id: str,
        request: ScreenshotAnalysisRequestCreate,
    ) -> ScreenshotAnalysisRequestResponse:
        return ScreenshotAnalysisRequestResponse(
            analysis_request_id="req_screenshot_2",
            extracted_text="스포일러 포함 텍스트",
            categories=[BlockCategory.SPOILER],
            risk_level=RiskLevel.HIGH,
            relevance_level=RelevanceLevel.HIGH,
            should_block=True,
            block_action=BlockActionResponse(
                unit_type=ContentUnitType.TEXT,
                reason="스포일러 콘텐츠",
                related_topics=["작품명"],
            ),
        )


async def fake_db_session() -> AsyncGenerator[object, None]:
    yield object()


async def fake_current_user_id() -> str:
    return "user_1"


def test_create_analysis_request_returns_results(monkeypatch) -> None:
    from app.api import analysis_requests

    monkeypatch.setattr(analysis_requests, "AnalysisService", FakeAnalysisService)
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.post(
        "/api/analyses",
        json={
            "page": {"url": "https://example.com", "title": "테스트 페이지"},
            "contents": [
                {
                    "clientContentId": "content_1",
                    "unitType": "TEXT",
                    "text": "일반 텍스트",
                },
            ],
        },
    )

    app.dependency_overrides.clear()
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["analysisRequestId"] == "req_1"
    assert len(data["results"]) == 1
    assert data["results"][0]["clientContentId"] == "content_1"
    assert data["results"][0]["shouldBlock"] is False


def test_create_analysis_request_requires_auth() -> None:
    client = TestClient(app, raise_server_exceptions=False)

    response = client.post(
        "/api/analyses",
        json={
            "page": {"url": "https://example.com"},
            "contents": [],
        },
    )

    assert response.status_code == 401


def test_create_analysis_request_requires_body() -> None:
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app, raise_server_exceptions=False)

    response = client.post("/api/analyses", json={})

    app.dependency_overrides.clear()
    assert response.status_code == 422


def test_create_screenshot_analysis_returns_extracted_text(monkeypatch) -> None:
    from app.api import screenshot_analysis_requests

    monkeypatch.setattr(
        screenshot_analysis_requests,
        "ScreenshotAnalysisService",
        FakeScreenshotAnalysisService,
    )
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.post(
        "/api/analyses/screenshot",
        json={"url": "https://example.com", "title": "스크린샷 테스트"},
    )

    app.dependency_overrides.clear()
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["analysisRequestId"] == "req_screenshot_1"
    assert data["extractedText"] == "추출된 텍스트"
    assert data["shouldBlock"] is False
    assert data["blockAction"] is None


def test_create_screenshot_analysis_blocked_includes_block_action(monkeypatch) -> None:
    from app.api import screenshot_analysis_requests

    monkeypatch.setattr(
        screenshot_analysis_requests,
        "ScreenshotAnalysisService",
        FakeScreenshotAnalysisServiceBlocked,
    )
    app.dependency_overrides[get_db_session] = fake_db_session
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app)

    response = client.post(
        "/api/analyses/screenshot",
        json={"url": "https://example.com"},
    )

    app.dependency_overrides.clear()
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["shouldBlock"] is True
    assert data["categories"] == ["SPOILER"]
    assert data["blockAction"]["reason"] == "스포일러 콘텐츠"


def test_create_screenshot_analysis_requires_auth() -> None:
    client = TestClient(app, raise_server_exceptions=False)

    response = client.post(
        "/api/analyses/screenshot",
        json={"url": "https://example.com"},
    )

    assert response.status_code == 401


def test_create_screenshot_analysis_requires_url() -> None:
    app.dependency_overrides[get_current_user_id] = fake_current_user_id
    client = TestClient(app, raise_server_exceptions=False)

    response = client.post("/api/analyses/screenshot", json={})

    app.dependency_overrides.clear()
    assert response.status_code == 422
