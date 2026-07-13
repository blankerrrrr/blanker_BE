# 008-implement-duplicate-group-api

## 작업 개요
- 작업명: 중복 콘텐츠 통합 API 구현
- 관련 TASK: API 구현 - 중복 콘텐츠 통합
- 관련 API/문서: `docs/api-spec/GET-api-interest-item-groups-interestItemGroupId.md`, `docs/api-spec/POST-api-interest-item-groups-interestItemGroupId-sources.md`
- 커밋 메시지: `feat: 중복 콘텐츠 통합 API 구현`

## 변경한 파일
- `backend/app/api/interest_item_groups.py`
- `backend/app/services/duplicate_group_service.py`
- `backend/app/db/repositories/interest_item_repository.py`
- `backend/app/schemas/interest_item.py`
- `backend/app/core/error_codes.py`
- `TASK.md`

## 구체적인 구현 내용
- 중복 그룹 상세 조회 API를 추가했다.
- 기존 그룹에 관심 정보 출처를 추가하는 API를 추가했다.
- 같은 그룹에 이미 포함된 관심 정보는 409 에러를 반환한다.
- 그룹 이동 시 기존 그룹과 대상 그룹의 sourceCount를 갱신한다.

## 변경된 플로우
- 요청: 인증된 사용자가 중복 그룹을 조회하거나 관심 정보 항목을 그룹에 추가한다.
- 처리: service가 그룹/항목 소유권과 중복 포함 여부를 검증하고 그룹 정보를 갱신한다.
- 응답: 대표 정보, 출처 목록 또는 갱신된 sourceCount를 반환한다.

## 검증 내용
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m ruff check app alembic tests --no-cache`
- 검증 결과: ruff 검사 통과
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "import app.main; print('ok')"`
- 검증 결과: 앱 import 성공
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "from fastapi.testclient import TestClient; from app.main import app; r=TestClient(app).get('/health'); print(r.status_code); print(r.json())"`
- 검증 결과: `/health` 200 응답 확인
- 미검증 사유: DB 연동 API 시나리오는 로컬 PostgreSQL/Redis 준비 상태를 확인하지 못해 생략했다.

## 참고
-
