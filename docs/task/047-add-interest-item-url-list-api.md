# 047. 관심 정보 URL 목록 조회 API 추가

## 작업 개요
- 작업명: 수집한 관심 정보의 URL 조회 API
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `GET /api/interest-items/urls`
- 커밋 메시지: `feat: 관심 정보 URL 목록 조회 API 추가`

## 변경한 파일
- `backend/app/api/interest_items.py`
- `backend/app/schemas/interest_item.py`
- `backend/app/services/interest_item_service.py`
- `backend/app/db/repositories/interest_item_repository.py`
- `backend/tests/unit/test_interest_item_api.py`
- `backend/tests/unit/test_interest_item_service.py`
- `docs/api-spec/GET-api-interest-items-urls.md`
- `docs/api-spec/README.md`
- `docs/api-test/http/interest-items.http`
- `docs/backend-architecture.md`
- `docs/task/047-add-interest-item-url-list-api.md`

## 구체적인 구현 내용
- `GET /api/interest-items/urls` 엔드포인트를 추가했다.
- 현재 사용자의 관심 정보 `sourceUrl` 목록을 최신 발견순으로 반환하도록 했다.
- URL 목록 전용 응답 schema와 service/repository 조회 메서드를 추가했다.
- API 문서와 HTTP 테스트 문서를 갱신했다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: 통과
