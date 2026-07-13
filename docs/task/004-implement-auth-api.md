# 004-implement-auth-api

## 작업 개요
- 작업명: 로그인 및 회원가입 API 구현
- 관련 TASK: API 구현 - 로그인 및 회원가입
- 관련 API/문서: `docs/api-spec/POST-api-auth-signup.md`, `docs/api-spec/POST-api-auth-login.md`, `docs/api-spec/POST-api-auth-refresh.md`, `docs/api-spec/POST-api-auth-logout.md`, `docs/api-spec/GET-api-auth-me.md`
- 커밋 메시지: `feat: 로그인 및 회원가입 API 구현`

## 변경한 파일
- `backend/app/api/auth.py`
- `backend/app/api/deps.py`
- `backend/app/services/auth_service.py`
- `backend/app/core/security.py`
- `backend/app/cache/refresh_token_store.py`
- `backend/app/db/models/user.py`
- `backend/app/db/repositories/user_repository.py`
- `backend/app/schemas/auth.py`
- `backend/app/schemas/user.py`
- `backend/alembic/versions/20260713_0001_create_users.py`
- `TASK.md`

## 구체적인 구현 내용
- 회원가입, 로그인, 토큰 재발급, 로그아웃, 내 계정 조회 API를 추가했다.
- PBKDF2 기반 비밀번호 hash/검증과 JWT access token 발급/검증을 추가했다.
- Refresh token을 HttpOnly Cookie로 전달하고 Redis에는 hash만 저장하도록 구현했다.
- 사용자 ORM 모델, repository, Alembic migration을 추가했다.
- 인증 실패, 약관 미동의, 중복 이메일 등 인증 에러 코드를 추가했다.

## 변경된 플로우
- 요청: 클라이언트가 인증 API로 이메일, 비밀번호 또는 token을 전달한다.
- 처리: service가 사용자 DB와 Redis refresh token hash를 검증하고 token을 발급한다.
- 응답: 공통 응답 포맷으로 data를 반환하고 refresh token은 Cookie로 설정한다.

## 검증 내용
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "import app.main; print('ok')"`
- 검증 결과: 앱 import 성공
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "from fastapi.testclient import TestClient; from app.main import app; r=TestClient(app).get('/health'); print(r.status_code); print(r.json())"`
- 검증 결과: `/health` 200 응답 확인
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m pytest tests\\test_health.py -vv`
- 미검증 사유: 테스트는 PASSED까지 출력됐으나 pytest 프로세스가 종료되지 않아 timeout 발생

## 참고
-
