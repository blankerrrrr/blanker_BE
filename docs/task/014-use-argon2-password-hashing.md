# 014-use-argon2-password-hashing

## 작업 개요
- 작업명: 비밀번호 해싱 Argon2 적용
- 관련 TASK: 비밀번호 해싱을 argon2 라이브러리를 사용하도록 변경
- 관련 API/문서: `backend/app/core/security.py`
- 커밋 메시지: `feat: 비밀번호 해싱 Argon2 적용`

## 변경한 파일
- `backend/app/core/security.py`
- `backend/pyproject.toml`
- `backend/uv.lock`
- `backend/tests/unit/test_security.py`

## 구체적인 구현 내용
- `argon2-cffi` 의존성을 추가했다.
- 신규 비밀번호 해시는 Argon2 해시로 생성하도록 변경했다.
- 기존 PBKDF2 해시는 로그인 검증이 가능하도록 호환 검증 경로를 유지했다.
- Argon2 해시 생성과 비밀번호 검증 단위 테스트를 추가했다.

## 변경된 플로우
- 요청: 회원가입 시 비밀번호가 전달된다.
- 처리: `hash_password`가 Argon2 해시를 생성해 저장한다.
- 검증: 로그인 시 Argon2 해시는 Argon2 검증기를 사용하고, 기존 PBKDF2 해시는 레거시 경로로 검증한다.

## 검증 내용
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m ruff check . --no-cache`
- 검증 결과: ruff 검사 통과
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "from app.core.security import hash_password, verify_password; h=hash_password('pw'); print(h.startswith('$argon2')); print(verify_password('pw', h)); print(verify_password('x', h))"`
- 검증 결과: Argon2 해시 생성, 정상 비밀번호 true, 오답 false 확인
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m pytest tests\\unit\\test_security.py -q`
- 검증 결과: 테스트 통과 출력 후 프로세스 종료 지연으로 제한 시간 초과

## 참고
-
