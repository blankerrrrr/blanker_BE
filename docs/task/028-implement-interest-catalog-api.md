# 028. 관심사 카탈로그 API 구현

## 작업 개요
- 작업명: 관심사 카탈로그 모델링 및 선택 API 구현
- 관련 TASK: catalog 테이블 모델링, 관심사 조회 및 개인 관심사 저장 API
- 관련 API/문서: `GET /api/interests`, `POST /api/interests/select`
- 커밋 메시지: `feat: 관심사 카탈로그 API 구현`

## 변경한 파일
- `backend/app/db/models/interest.py`
- `backend/app/db/repositories/interest_repository.py`
- `backend/app/services/interest_service.py`
- `backend/app/api/interests.py`
- `backend/alembic/versions/20260713_0008_create_interests.py`
- `docs/data-modeling.md`
- `docs/api-spec/GET-api-interests.md`
- `docs/api-spec/POST-api-interests-select.md`

## 구체적인 구현 내용
- `interests` 테이블을 추가하고 제목, 장르, 이미지 URL을 저장하도록 모델링했다.
- 관심사 목록 조회 API와 선택한 관심사를 개인 관심사로 저장하는 API를 추가했다.
- 선택 저장 시 기존 개인 관심사가 있으면 중복 생성하지 않고 기존 데이터를 응답한다.
- API 명세와 데이터 모델링 문서를 갱신했다.

## 변경된 플로우
- 요청: 클라이언트가 `GET /api/interests`로 온보딩 관심사 목록을 조회한다.
- 처리: 사용자가 선택한 `interestIds`를 `POST /api/interests/select`로 전달한다.
- 응답: 서버가 선택 항목을 `interest_targets`에 `WORK` 타입 개인 관심사로 저장하고 반환한다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit\test_public_id.py tests\unit\test_camel_model.py tests\test_health.py`
- 검증 결과: 테스트 7개 통과 출력 확인 후 pytest 종료 지연으로 타임아웃

## 추후 추가해야 할 사항
- 외부 interesting-item API 호출 결과를 `interests`에 적재하는 로직과 자동 insert 마이그레이션을 추가해야 한다.
