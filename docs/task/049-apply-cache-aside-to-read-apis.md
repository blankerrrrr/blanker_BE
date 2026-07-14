# 049. 자주 호출하는 조회 API cache-aside 적용

## 작업 개요
- 작업명: 자주 호출하는 조회 API에 cache-aside 기법 적용
- 관련 TASK: `TASK.md`
- 관련 API/문서: `GET /api/interests`, `GET /api/interests/types`, `GET /api/interests/genres`
- 커밋 메시지: `feat: 조회 API cache-aside 적용`

## 변경한 파일
- `backend/app/cache/query_cache.py`
- `backend/app/api/deps.py`
- `backend/app/api/interests.py`
- `backend/app/services/interest_service.py`
- `backend/tests/unit/test_interest_api.py`
- `backend/tests/unit/test_query_cache.py`
- `docs/cache.md`
- `docs/backend-architecture.md`
- `TASK.md`
- `docs/task/049-apply-cache-aside-to-read-apis.md`

## 구체적인 구현 내용
- Redis 기반 `QueryCache`를 추가했다.
- 관심사 목록/종류/장르 조회 API에 cache-aside 흐름을 적용했다.
- 요청 파라미터를 JSON 정규화 후 SHA-256 hash로 key를 생성하도록 했다.
- Redis 조회/저장 실패 시 DB 조회로 fallback하도록 했다.
- 캐시 적용 API 목록을 `docs/cache.md`에 표로 문서화했다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: 69 passed
