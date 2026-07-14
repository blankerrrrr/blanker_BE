# 057. 보관함 관심사 분류 필터 및 개인 분류 조회

## 작업 개요
- 작업명: 보관함 관심사 분류 필터와 개인 관심사 분류 목록 API 추가
- 관련 TASK: `TASK.md`
- 관련 API/문서: `GET /api/blocked-items`, `GET /api/interest-targets/types`
- 커밋 메시지: `feat: 보관함 관심사 분류 필터 추가`

## 변경 내용
- 보관함 목록에 선택적 `interestType` 쿼리스트링을 추가했다.
- 관심 대상과 관심사, `interest_catalog`를 조인해 분류에 속한 보관함만 조회한다.
- 사용자가 선택한 관심사가 속한 분류 이름만 반환하는 API를 추가했다.
- HTTP 요청 예시와 API 명세를 갱신했다.

## 검증 내용
- 실행 명령: `uv --cache-dir .uv-cache run pytest tests/unit -q --basetemp=.pytest-tmp`
- 검증 결과: 75 passed
- 실행 명령: `uv --cache-dir .uv-cache run ruff check app tests/unit`
- 검증 결과: 통과
