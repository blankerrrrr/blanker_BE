# 006-implement-interest-item-api

## 작업 개요
- 작업명: 관심 정보 자동 수집 API 구현
- 관련 TASK: API 구현 - 관심 정보 자동 수집
- 관련 API/문서: `docs/api-spec/GET-api-interest-items.md`, `docs/api-spec/GET-api-interest-items-interestItemId.md`, `docs/api-spec/POST-api-interest-items.md`
- 커밋 메시지: `feat: 관심 정보 자동 수집 API 구현`

## 변경한 파일
- `backend/app/api/interest_items.py`
- `backend/app/services/interest_item_service.py`
- `backend/app/db/models/interest_item.py`
- `backend/app/db/repositories/interest_item_repository.py`
- `backend/app/schemas/interest_item.py`
- `backend/app/core/error_codes.py`
- `backend/alembic/versions/20260713_0003_create_interest_items.py`
- `TASK.md`

## 구체적인 구현 내용
- 관심 정보 목록 조회, 상세 조회, 수집 저장 API를 추가했다.
- 관심 대상과 relatedTopics를 비교해 관련성이 낮은 수집 요청을 거부한다.
- 동일 sourceUrl은 중복 저장하지 않고 기존 항목을 duplicate 응답으로 반환한다.
- 현재 구현에서는 `20260714_0012` 이후 관심 정보 그룹 테이블을 사용하지 않고 `interest_items` 원본 항목만 저장한다.

## 변경된 플로우
- 요청: 인증된 사용자가 확장 프로그램 또는 분석 서버에서 수집한 관심 정보를 저장한다.
- 처리: service가 관심 대상 관련성과 sourceUrl 중복을 확인한다.
- 응답: 저장된 관심 정보 ID와 중복 여부를 공통 응답 포맷으로 반환한다.

## 검증 내용
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m ruff check app alembic tests --no-cache`
- 검증 결과: ruff 검사 통과
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "import app.main; print('ok')"`
- 검증 결과: 앱 import 성공
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "from fastapi.testclient import TestClient; from app.main import app; r=TestClient(app).get('/health'); print(r.status_code); print(r.json())"`
- 검증 결과: `/health` 200 응답 확인
- 미검증 사유: DB 연동 API 시나리오는 로컬 PostgreSQL/Redis 준비 상태를 확인하지 못해 생략했다.

## 참고
-
