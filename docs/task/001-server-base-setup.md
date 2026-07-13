# 001-server-base-setup

## 작업 개요
- 작업명: FastAPI 서버 기초 설정
- 관련 TASK: `backend-architecture.md` 문서를 보고 서버 기초 설정하기
- 관련 API/문서: `docs/backend-architecture.md`, `docs/tech-stack.md`, `docs/api-spec/api-rule.md`
- 커밋 메시지: `feat: 서버 기초 설정`

## 변경한 파일
- `backend/app/...`
- `backend/pyproject.toml`
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/Dockerfile`
- `backend/docker-compose.yml`
- `backend/.env.example`
- `backend/tests/test_health.py`
- `TASK.md`

## 구체적인 구현 내용
- FastAPI 앱 팩토리와 `/health` 엔드포인트를 추가했다.
- 문서 기준 패키지 구조와 빈 라우터를 연결했다.
- 공통 설정, 응답, 예외, 페이지네이션, ID/시간 유틸을 추가했다.
- SQLAlchemy 비동기 세션과 Alembic 기본 설정을 추가했다.
- 로컬 PostgreSQL, Redis, API Docker Compose 구성을 추가했다.

## 검증 내용
- 실행 명령: `python -m compileall backend`
- 검증 결과: Python 구문 컴파일 성공
- 실행 명령: `python -m pytest`
- 미검증 사유: 현재 Python 환경에 `pytest`가 설치되어 있지 않아 실행 불가
