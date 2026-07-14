# 058. 웹 검색 API 구현

## 작업 개요
- 작업명: 서버 웹 검색 API 구현
- 관련 TASK: `TASK.md`
- 관련 API/문서: `GET /api/web-search`
- 커밋 메시지: `feat: 웹 검색 API 구현`

## 변경한 파일
- `backend/app/api/router.py`
- `backend/app/api/web_search.py`
- `backend/app/core/config.py`
- `backend/app/core/error_codes.py`
- `backend/app/schemas/web_search.py`
- `backend/app/services/web_search_service.py`
- `backend/docker-compose.search.yml`
- `backend/searxng/settings.yml`
- `backend/tests/unit/test_web_search_api.py`
- `backend/tests/unit/test_web_search_service.py`
- `backend/.env.example`
- `docs/api-spec/GET-api-web-search.md`
- `docs/api-spec/README.md`
- `docs/api-test/http/web-search.http`
- `docs/task/058-implement-web-search-api.md`

## 참고
- `TASK.md`는 gitignore 대상이라 커밋하지 않고 로컬 완료 체크만 반영했다.

## 구체적인 구현 내용
- `GET /api/web-search` 인증 API를 추가했다.
- SearXNG 검색 컨테이너 설정을 추가했다.
- 외부 검색 결과를 `query`, `results[].title/url/description` 형태로 정규화한다.
- 검색 API 키 없이 내부 SearXNG `/search?format=json` 응답을 사용한다.
- 외부 검색 실패를 전용 에러 코드로 구분한다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit\test_web_search_api.py tests\unit\test_web_search_service.py -q`
- 검증 결과: 4 passed
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: 79 passed
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
