# 019-replace-auth-user-response-helper

## 작업 개요
- 작업명: auth_service 사용자 응답 헬퍼 제거
- 관련 TASK: `auth_service._user_response()`를 Pydantic 응답 스키마로 대체
- 관련 API/문서: `backend/app/services/auth_service.py`, `backend/app/schemas/common.py`
- 커밋 메시지: `feat: 사용자 응답 스키마 변환 적용`

## 변경한 파일
- `backend/app/schemas/common.py`
- `backend/app/services/auth_service.py`
- `backend/tests/unit/test_camel_model.py`
- `docs/task/019-replace-auth-user-response-helper.md`

## 구체적인 구현 내용
- `CamelModel`에 `from_attributes=True` 설정을 추가했다.
- `AuthService`에서 `_user_response()` dict 변환 헬퍼를 제거했다.
- `SignupResponse`, `UserResponse`, `LoginUserResponse`가 ORM 객체를 직접 검증하도록 변경했다.
- attribute 기반 Pydantic 응답 검증 테스트를 추가했다.

## 변경된 플로우
- 처리: `User` ORM 객체를 Pydantic 응답 스키마에 바로 전달한다.
- 응답: `CamelModel`이 ORM 속성을 읽고 camelCase alias로 직렬화한다.

## 검증 내용
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m ruff check . --no-cache`
- 검증 결과: ruff 검사 통과
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "from app.services.auth_service import AuthService; print(AuthService.__name__)"`
- 검증 결과: AuthService import 확인
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m pytest tests\\unit\\test_camel_model.py -q`
- 검증 결과: 테스트 통과 출력 후 프로세스 종료 지연으로 제한 시간 초과

## 참고
-
