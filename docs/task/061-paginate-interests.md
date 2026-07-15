# 061. 관심사 목록 페이지네이션

## 작업 개요
- 작업명: 관심사 목록 조회 페이지네이션 추가
- 관련 API: `GET /api/interests`
- 커밋 메시지: `feat: 관심사 목록 페이지네이션 추가`

## 변경 내용
- `page`, `size` 쿼리스트링을 추가했다.
- 관심사 종류, 다중 장르, 검색어 필터가 적용된 전체 개수를 계산한다.
- 응답에 현재 페이지, 페이지 크기, 전체 항목 수, 전체 페이지 수를 포함한다.

## 검증 내용
- 실행 명령: `uv --cache-dir .uv-cache run pytest tests/unit -q --basetemp=.pytest-all-interest-pagination`
- 검증 결과: 84 passed
- 실행 명령: `uv --cache-dir .uv-cache run ruff check app/api/interests.py app/schemas/interest.py app/services/interest_service.py app/db/repositories/interest_repository.py tests/unit/test_interest_api.py tests/unit/test_interest_repository.py`
- 검증 결과: 통과
