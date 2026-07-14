# 045. 관심사 제목 목록 조회 API 추가

## 작업 개요
- 작업명: 관심사 제목 목록 조회 API
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `GET /api/interest-targets/titles`
- 커밋 메시지: `feat: 관심사 제목 목록 조회 API 추가`

## 변경한 파일
- `backend/app/api/interest_targets.py`
- `backend/app/schemas/interest_target.py`
- `backend/app/services/interest_target_service.py`
- `backend/tests/unit/test_interest_target_api.py`
- `docs/api-spec/GET-api-interest-targets-titles.md`
- `docs/api-spec/README.md`
- `docs/api-test/http/interest-targets.http`
- `docs/task/045-add-interest-target-title-list-api.md`

## 구체적인 구현 내용
- `GET /api/interest-targets/titles` 엔드포인트를 추가했다.
- 현재 사용자 관심 대상 목록에서 `interestTargetId`, `title`만 반환한다.
- 보관함 조회 API의 `interestTargetId` query string 선택지로 사용할 수 있다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: `63 passed`
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- API 확인: `GET /api/interest-targets/titles` 200 OK
