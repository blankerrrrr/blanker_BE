from app.schemas.auth import SignupRequest, TokenResponse
from app.schemas.interest_item import InterestItemCreateRequest


def test_camel_model_accepts_camel_case_request_fields() -> None:
    request = SignupRequest.model_validate(
        {
            "email": "user@example.com",
            "password": "password123",
            "termsAgreed": True,
            "privacyAgreed": True,
        },
    )

    assert request.terms_agreed
    assert request.privacy_agreed


def test_camel_model_serializes_response_fields_as_camel_case() -> None:
    response = TokenResponse(access_token="token", expires_in=3600)

    assert response.model_dump(by_alias=True) == {
        "accessToken": "token",
        "tokenType": "Bearer",
        "expiresIn": 3600,
    }


def test_request_model_keeps_default_factory_without_alias_field() -> None:
    request = InterestItemCreateRequest.model_validate(
        {
            "title": "title",
            "summary": "summary",
            "sourceUrl": "https://example.com",
        },
    )

    assert request.related_topics == []
    assert request.source_url == "https://example.com"
