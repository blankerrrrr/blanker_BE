# 055. 관심 정보 URL 최신순 정렬

## 작업 개요
- 작업명: 관심 정보 URL 목록 조회 결과 최신순 정렬
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `GET /api/interest-items/urls`
- 커밋 메시지: `fix: 관심 정보 URL 최신순 정렬`

## 변경한 파일
- `backend/app/services/interest_item_service.py`
- `backend/tests/unit/test_interest_item_service.py`
- `docs/api-spec/GET-api-interest-items-urls.md`
- `docs/task/055-order-interest-item-urls-by-latest.md`
- `TASK.next.md`

## 구체적인 구현 내용
- URL 목록 응답 생성 시 `discoveredAt` 기준 최신순으로 한 번 더 정렬한다.
- 날짜 그룹은 최신 날짜부터 반환하고, 같은 날짜 안의 항목도 최신 발견 시각부터 반환한다.
- API 문서 예시를 최신순 응답으로 수정했다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit\test_interest_item_service.py tests\unit\test_interest_item_api.py -q`
- 검증 결과: 6 passed
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: 72 passed
- 실행 명령: `.\.venv\Scripts\ruff.exe check app/services/interest_item_service.py tests/unit/test_interest_item_service.py --no-cache`
- 검증 결과: 통과
