# 053. 보관함 목록 그룹 응답 수정

## 작업 개요
- 작업명: 보관함 목록 조회 API 응답 구조 수정
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `GET /api/blocked-items`
- 커밋 메시지: `fix: 보관함 목록 그룹 응답 수정`

## 변경한 파일
- `backend/app/api/blocked_items.py`
- `backend/app/db/repositories/blocked_item_repository.py`
- `backend/app/schemas/blocked_item.py`
- `backend/app/services/blocked_item_service.py`
- `backend/tests/unit/test_blocked_item_api.py`
- `docs/api-spec/GET-api-blocked-items.md`
- `docs/api-test/http/blocked-items.http`
- `TASK.next.md`

## 구체적인 구현 내용
- `GET /api/blocked-items` 응답을 관심 대상 제목별 배열 구조로 변경했다.
- `interestTargetId`를 선택 query string으로 변경해 전체 관심 대상 기준 그룹 조회를 지원한다.
- 보관함 항목이 없는 관심 대상도 빈 배열로 응답에 포함한다.
- 유형 필터는 기존 `type` query string을 유지한다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit\test_blocked_item_api.py tests\unit\test_interest_item_api.py -q`
- 검증 결과: 4 passed
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: 71 passed
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
