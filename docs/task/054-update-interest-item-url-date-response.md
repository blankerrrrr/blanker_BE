# 054. 관심 정보 URL 날짜별 응답 수정

## 작업 개요
- 작업명: 관심 정보 URL 목록 조회 API 응답 구조 수정
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `GET /api/interest-items/urls`
- 커밋 메시지: `fix: 관심 정보 URL 날짜별 응답 수정`

## 변경한 파일
- `backend/app/api/interest_items.py`
- `backend/app/schemas/interest_item.py`
- `backend/app/services/interest_item_service.py`
- `backend/tests/unit/test_interest_item_api.py`
- `docs/api-spec/GET-api-interest-items-urls.md`
- `TASK.next.md`

## 구체적인 구현 내용
- `GET /api/interest-items/urls` 응답을 `discoveredAt` 날짜별 배열 구조로 변경했다.
- 각 URL 항목은 기존 `interestItemId`, `sourceUrl`, `discoveredAt` 필드를 유지한다.
- 기존 인증 요구 사항은 유지한다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit\test_blocked_item_api.py tests\unit\test_interest_item_api.py -q`
- 검증 결과: 4 passed
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: 71 passed
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
