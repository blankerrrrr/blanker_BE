# 018-implement-token-service

## 작업 개요
- 작업명: TokenService 구현
- 관련 TASK: `backend/app/services/token_service.py` 구현
- 관련 API/문서: `backend/app/services/auth_service.py`, `backend/app/core/security.py`
- 커밋 메시지: `feat: TokenService 구현`

## 변경한 파일
- `backend/app/services/token_service.py`
- `backend/app/services/auth_service.py`
- `backend/app/core/security.py`
- `backend/tests/unit/test_token_service.py`
- `TASK.md`

## 구체적인 구현 내용
- `TokenService`를 추가해 access token 발급, refresh token 발급/검증/회전/삭제를 담당하도록 했다.
- `AuthService`의 refresh token 저장/검증 헬퍼를 제거하고 `TokenService`를 사용하도록 변경했다.
- `core.security`에서 더 이상 사용하지 않는 `hmac` import를 제거했다.
- Redis 없이 검증 가능한 fake store 기반 TokenService 단위 테스트를 추가했다.

## 변경된 플로우
- 로그인: `AuthService`가 `TokenService`로 access token과 refresh token을 발급한다.
- 재발급: `TokenService`가 기존 refresh token을 검증/삭제한 뒤 새 refresh token을 발급한다.
- 로그아웃: `TokenService`가 refresh token을 파싱해 저장소에서 삭제한다.

## 검증 내용
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m ruff check . --no-cache`
- 검증 결과: ruff 검사 통과
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "from app.services.token_service import TokenService; print(TokenService.__name__)"`
- 검증 결과: TokenService import 확인
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m pytest tests\\unit\\test_token_service.py -q`
- 검증 결과: 테스트 통과 출력 후 프로세스 종료 지연으로 제한 시간 초과

## 참고
-
