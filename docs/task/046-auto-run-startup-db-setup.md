# 046. 서버 시작 시 DB 준비 자동 실행

## 작업 개요
- 작업명: 서버 시작 시 마이그레이션과 기본 관심사 시드 자동 실행
- 관련 이슈: VPS 배포 후 `interest_catalog` 기본 데이터가 비어 있는 문제
- 커밋 메시지: `feat: 서버 시작 시 DB 준비 자동 실행`

## 변경한 파일
- `backend/Dockerfile`
- `backend/scripts/start.py`
- `docs/task/046-auto-run-startup-db-setup.md`

## 구체적인 구현 내용
- API 컨테이너 시작 명령을 `uvicorn` 직접 실행에서 `scripts/start.py` 실행으로 변경했다.
- `scripts/start.py`에서 Alembic `upgrade head`를 먼저 실행하도록 했다.
- 기본 관심사 종류 시드 `seed_default_interest_types.py`를 서버 시작 전에 실행하도록 했다.
- DB 준비 지연에 대응하기 위해 마이그레이션과 시드에 재시도 로직을 추가했다.

## 변경된 플로우
- 기존: 컨테이너 시작 -> API 서버 실행
- 변경: 컨테이너 시작 -> DB 마이그레이션 -> 기본 관심사 종류 시드 -> API 서버 실행

## 검증 내용
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: 63 passed
