# 059. 관심사 다중 장르 조회

## 작업 개요
- 작업명: 관심사 목록 다중 장르 필터 추가
- 관련 API: `GET /api/interests`
- 커밋 메시지: `feat: 관심사 다중 장르 조회 추가`

## 변경 내용
- 반복되는 `genre` 쿼리스트링을 목록으로 수신한다.
- 지정한 장르 중 하나라도 포함된 관심사를 조회한다.
- 장르 생략 또는 `전체` 포함 시 기존처럼 장르 필터를 적용하지 않는다.
- API 테스트와 명세, HTTP 예시를 갱신했다.

## 검증 내용
- 실행 명령: `uv --cache-dir .uv-cache run pytest tests/unit/test_interest_api.py tests/unit/test_interest_repository.py tests/unit/test_query_cache.py -q --basetemp=.pytest-multi-genre`
- 검증 결과: 11 passed
- 실행 명령: `uv --cache-dir .uv-cache run ruff check app/api/interests.py app/services/interest_service.py app/db/repositories/interest_repository.py tests/unit/test_interest_api.py tests/unit/test_interest_repository.py`
- 검증 결과: 통과
