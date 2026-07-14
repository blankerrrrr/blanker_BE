from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app, create_app


def test_health_check() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"success": True, "data": {"status": "ok"}}


def test_cors_allows_configured_origin(monkeypatch) -> None:
    origin = "https://frontend.example.test"
    monkeypatch.setattr(settings, "cors_allow_origins", (origin,))
    client = TestClient(create_app())

    response = client.options(
        "/api/interests/types",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
    assert response.headers["access-control-allow-credentials"] == "true"
