# 059. 웹 검색 API SearXNG 전환

## 작업 개요
- 작업명: 웹 검색 API 무료 자체 호스팅 검색 엔진 전환
- 관련 API/문서: `GET /api/web-search`
- 커밋 메시지: `refactor: 웹 검색 API SearXNG 전환`

## 변경한 파일
- `backend/app/api/web_search.py`
- `backend/app/core/config.py`
- `backend/app/core/error_codes.py`
- `backend/app/services/web_search_service.py`
- `backend/tests/unit/test_web_search_api.py`
- `backend/tests/unit/test_web_search_service.py`
- `backend/.env.example`
- `backend/docker-compose.yml`
- `backend/docker-compose.search.yml`
- `backend/searxng/settings.yml`
- `.github/workflows/deploy.yml`
- `docs/api-spec/GET-api-web-search.md`
- `docs/api-test/http/web-search.http`
- `docs/task/058-implement-web-search-api.md`
- `docs/task/059-switch-web-search-to-searxng.md`

## 구체적인 구현 내용
- Brave Search API 키 기반 호출을 제거했다.
- SearXNG `/search?format=json` 호출로 웹 검색 공급자를 변경했다.
- `WEB_SEARCH_API_URL` 기본값을 `http://searxng:8080/search`로 변경했다.
- 메인 Compose에서 API 컨테이너의 검색 URL을 SearXNG 내부 주소로 덮어쓰도록 했다.
- SearXNG 별도 Compose 파일과 JSON 응답 허용 설정 파일을 추가했다.
- 배포 워크플로우가 SearXNG Compose와 설정 파일을 서버로 복사하도록 수정했다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit\test_web_search_api.py tests\unit\test_web_search_service.py -q`
- 검증 결과: 3 passed
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: 78 passed
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `docker compose config`
- 검증 결과: 통과
- 실행 명령: `docker compose -f docker-compose.search.yml config`
- 검증 결과: 통과
