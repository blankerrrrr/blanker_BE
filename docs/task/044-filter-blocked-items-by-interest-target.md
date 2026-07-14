# 044. 보관함 관심사별 조회 필터 추가

## 작업 개요
- 작업명: 보관함 조회 API에 관심사 쿼리 스트링 추가
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `GET /api/blocked-items`, `POST /api/blocked-items`
- 커밋 메시지: `feat: 보관함 관심사별 조회 필터 추가`

## 변경한 파일
- `backend/app/api/blocked_items.py`
- `backend/app/db/models/blocked_item.py`
- `backend/app/db/repositories/blocked_item_repository.py`
- `backend/app/schemas/blocked_item.py`
- `backend/app/services/blocked_item_service.py`
- `backend/alembic/versions/20260714_0016_add_interest_target_to_blocked_items.py`
- `backend/tests/unit/test_blocked_item_api.py`
- `docs/api-spec/GET-api-blocked-items.md`
- `docs/api-spec/POST-api-blocked-items.md`
- `docs/api-test/http/blocked-items.http`
- `docs/data-modeling.md`
- `docs/task/044-filter-blocked-items-by-interest-target.md`

## 구체적인 구현 내용
- `blocked_items.interest_target_id` FK를 추가했다.
- `POST /api/blocked-items` 요청에 `interestTargetId`를 필수로 추가하고 사용자 소유 관심 대상인지 검증한다.
- `GET /api/blocked-items`에 필수 query string `interestTargetId`를 추가해 전체 조회를 막고 관심 대상별 조회만 제공한다.
- 보관함 중복 기준을 사용자+관심대상+원본 URL+selector 단위로 변경했다.
- 목록 응답에 `interestTargetId`를 포함했다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: `61 passed`
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `.\.venv\Scripts\alembic.exe upgrade head`
- 검증 결과: `20260714_0015 -> 20260714_0016` 마이그레이션 성공
- API 확인: `POST /api/blocked-items` 201 Created
- API 확인: `GET /api/blocked-items?interestTargetId={id}&page=1&size=20&type=SPOILER` 200 OK
