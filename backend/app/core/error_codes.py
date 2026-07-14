from enum import StrEnum

from fastapi import status


class ErrorCode(StrEnum):
    INTERNAL_SERVER_ERROR = (
        "INTERNAL_SERVER_ERROR",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "서버 오류가 발생했습니다.",
    )
    INVALID_REQUEST_BODY = (
        "INVALID_REQUEST_BODY",
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        "요청 형식이 올바르지 않습니다.",
    )
    RESOURCE_NOT_FOUND = (
        "RESOURCE_NOT_FOUND",
        status.HTTP_404_NOT_FOUND,
        "리소스를 찾을 수 없습니다.",
    )
    UNAUTHORIZED = (
        "UNAUTHORIZED",
        status.HTTP_401_UNAUTHORIZED,
        "인증이 필요합니다.",
    )
    AUTH_EMAIL_ALREADY_EXISTS = (
        "AUTH_EMAIL_ALREADY_EXISTS",
        status.HTTP_409_CONFLICT,
        "이미 가입된 이메일입니다.",
    )
    AUTH_WEAK_PASSWORD = (
        "AUTH_WEAK_PASSWORD",
        status.HTTP_400_BAD_REQUEST,
        "비밀번호는 8자 이상이어야 합니다.",
    )
    AUTH_INVALID_CREDENTIALS = (
        "AUTH_INVALID_CREDENTIALS",
        status.HTTP_401_UNAUTHORIZED,
        "이메일 또는 비밀번호가 올바르지 않습니다.",
    )
    AUTH_ACCOUNT_DISABLED = (
        "AUTH_ACCOUNT_DISABLED",
        status.HTTP_403_FORBIDDEN,
        "비활성화된 계정입니다.",
    )
    AUTH_REFRESH_TOKEN_COOKIE_MISSING = (
        "AUTH_REFRESH_TOKEN_COOKIE_MISSING",
        status.HTTP_401_UNAUTHORIZED,
        "refresh token Cookie가 필요합니다.",
    )
    AUTH_INVALID_REFRESH_TOKEN = (
        "AUTH_INVALID_REFRESH_TOKEN",
        status.HTTP_401_UNAUTHORIZED,
        "유효하지 않은 refresh token입니다.",
    )
    AUTH_REFRESH_TOKEN_EXPIRED = (
        "AUTH_REFRESH_TOKEN_EXPIRED",
        status.HTTP_401_UNAUTHORIZED,
        "refresh token이 만료되었습니다.",
    )
    AUTH_UNAUTHORIZED = (
        "AUTH_UNAUTHORIZED",
        status.HTTP_401_UNAUTHORIZED,
        "인증 토큰이 필요합니다.",
    )
    USER_NOT_FOUND = (
        "USER_NOT_FOUND",
        status.HTTP_404_NOT_FOUND,
        "사용자를 찾을 수 없습니다.",
    )
    INTEREST_NOT_FOUND = (
        "INTEREST_NOT_FOUND",
        status.HTTP_404_NOT_FOUND,
        "관심사를 찾을 수 없습니다.",
    )
    INTEREST_TARGET_INVALID_TYPE = (
        "INTEREST_TARGET_INVALID_TYPE",
        status.HTTP_400_BAD_REQUEST,
        "관심 대상 타입이 올바르지 않습니다.",
    )
    INTEREST_TARGET_ALREADY_EXISTS = (
        "INTEREST_TARGET_ALREADY_EXISTS",
        status.HTTP_409_CONFLICT,
        "이미 등록된 관심 대상입니다.",
    )
    INTEREST_TARGET_NOT_FOUND = (
        "INTEREST_TARGET_NOT_FOUND",
        status.HTTP_404_NOT_FOUND,
        "관심 대상을 찾을 수 없습니다.",
    )
    INTEREST_ITEM_NOT_FOUND = (
        "INTEREST_ITEM_NOT_FOUND",
        status.HTTP_404_NOT_FOUND,
        "관심 정보를 찾을 수 없습니다.",
    )
    INTEREST_ITEM_NOT_RELEVANT = (
        "INTEREST_ITEM_NOT_RELEVANT",
        status.HTTP_400_BAD_REQUEST,
        "등록된 관심 대상과 관련성이 낮습니다.",
    )
    INTEREST_ITEM_GROUP_NOT_FOUND = (
        "INTEREST_ITEM_GROUP_NOT_FOUND",
        status.HTTP_404_NOT_FOUND,
        "중복 그룹을 찾을 수 없습니다.",
    )
    INTEREST_ITEM_ALREADY_GROUPED = (
        "INTEREST_ITEM_ALREADY_GROUPED",
        status.HTTP_409_CONFLICT,
        "이미 해당 그룹에 포함된 관심 정보입니다.",
    )
    ANALYSIS_CONTENT_TOO_LARGE = (
        "ANALYSIS_CONTENT_TOO_LARGE",
        status.HTTP_413_CONTENT_TOO_LARGE,
        "분석 요청 본문이 허용 크기를 초과했습니다.",
    )
    ANALYSIS_FAILED = (
        "ANALYSIS_FAILED",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "분석 처리에 실패했습니다.",
    )
    SCREENSHOT_FAILED = (
        "SCREENSHOT_FAILED",
        status.HTTP_502_BAD_GATEWAY,
        "스크린샷 캡처에 실패했습니다.",
    )
    OCR_FAILED = (
        "OCR_FAILED",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "텍스트 추출에 실패했습니다.",
    )
    BLOCK_SETTING_INVALID_SENSITIVITY = (
        "BLOCK_SETTING_INVALID_SENSITIVITY",
        status.HTTP_400_BAD_REQUEST,
        "차단 민감도 값이 올바르지 않습니다.",
    )
    BLOCKED_ITEM_ALREADY_EXISTS = (
        "BLOCKED_ITEM_ALREADY_EXISTS",
        status.HTTP_409_CONFLICT,
        "이미 저장된 보관함 항목입니다.",
    )
    BLOCKED_ITEM_NOT_FOUND = (
        "BLOCKED_ITEM_NOT_FOUND",
        status.HTTP_404_NOT_FOUND,
        "보관함 항목을 찾을 수 없습니다.",
    )

    def __new__(cls, code: str, status_code: int, message: str) -> "ErrorCode":
        obj = str.__new__(cls, code)
        obj._value_ = code
        return obj

    def __init__(self, code: str, status_code: int, message: str) -> None:
        self.code = code
        self.status_code = status_code
        self.message = message
