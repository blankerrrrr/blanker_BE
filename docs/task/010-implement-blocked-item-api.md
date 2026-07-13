# 010-implement-blocked-item-api

## 작업 개요
- 작업명: 차단 콘텐츠 저장 API 구현
- 관련 TASK: API 구현 - 차단 콘텐츠 저장
- 관련 API/문서: `docs/api-spec/GET-api-blocked-items.md`, `docs/api-spec/POST-api-blocked-items.md`, `docs/api-spec/DELETE-api-blocked-items-blockedItemId.md`
- 커밋 메시지: `feat: 차단 콘텐츠 저장 API 구현`

## 변경한 파일
- `backend/app/api/blocked_items.py`
- `backend/app/services/blocked_item_service.py`
- `backend/app/db/models/blocked_item.py`
- `backend/app/db/repositories/blocked_item_repository.py`
- `backend/app/schemas/blocked_item.py`
- `backend/app/core/error_codes.py`
- `backend/alembic/versions/20260713_0006_create_blocked_items.py`
- `TASK.md`

## 구체적인 구현 내용
- 보관함 목록 조회, 저장, 삭제 API를 추가했다.
- 페이지네이션과 차단 유형 필터를 추가했다.
- 사용자, sourceUrl, selector 기준 중복 저장을 차단한다.
- 보관함 ORM 모델, repository, migration을 추가했다.

## 변경된 플로우
- 요청: 인증된 사용자가 차단 콘텐츠를 저장하거나 보관함을 조회/삭제한다.
- 처리: service가 소유권, 중복 여부, 페이지네이션 조건을 검증하고 DB를 갱신한다.
- 응답: 공통 응답 포맷으로 보관함 목록, 저장 ID, 삭제 결과를 반환한다.

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
