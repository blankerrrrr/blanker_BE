# 051. 관심사 종류 조회 ID 정렬

## 작업 개요
- 작업명: 관심사 종류 목록을 카탈로그 ID 오름차순으로 조회
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `GET /api/interests/types`
- 커밋 메시지: `feat: 관심사 종류 조회 정렬 변경`

## 변경한 파일
- `TASK.next.md`
- `backend/app/db/repositories/interest_repository.py`
- `backend/tests/unit/test_interest_repository.py`
- `docs/task/051-order-interest-types-by-catalog-id.md`

## 구체적인 구현 내용
- 관심사 종류 조회 쿼리의 정렬 기준을 이름순에서 카탈로그 ID 오름차순으로 변경했다.
- 생성 순서가 응답 순서에 유지되는지 SQL 정렬 조건을 검증하는 단위 테스트를 추가했다.
- 웹툰 API 독립 컨테이너 구성 작업을 다음 TASK에 등록했다.

## 검증 내용
- 실행 명령: `uv --cache-dir .uv-cache run pytest tests/unit/test_interest_repository.py tests/unit/test_interest_api.py -q`
- 검증 결과: 7 passed
- 실행 명령: `uv --cache-dir .uv-cache run ruff check app/db/repositories/interest_repository.py tests/unit/test_interest_repository.py`
- 검증 결과: 통과
