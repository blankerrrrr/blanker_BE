# 029. 관심사 조회 조건 API 수정

## 작업 개요
- 작업명: 관심사 종류/장르/검색 기반 조회 API 수정
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `GET /api/interests`, `GET /api/interests/types`
- 커밋 메시지: `feat: 관심사 조회 조건 추가`

## 변경한 파일
- `backend/app/db/models/interest.py`
- `backend/app/db/repositories/interest_repository.py`
- `backend/app/services/interest_service.py`
- `backend/app/api/interests.py`
- `backend/alembic/versions/20260713_0009_add_interest_type.py`
- `docs/api-spec/GET-api-interests.md`
- `docs/api-spec/GET-api-interests-types.md`
- `docs/data-modeling.md`

## 구체적인 구현 내용
- `interests.interestType`과 `interestTypeImageUrl`을 추가해 관심사 종류, 대표 이미지, 장르를 분리했다.
- `GET /api/interests`에서 `interestType`을 필수 query string으로 받고 `genre` 기본값을 `전체`로 처리한다.
- `keyword`가 있으면 장르 필터를 적용하지 않고 같은 관심사 종류 안에서 제목을 검색한다.
- `GET /api/interests/types`로 저장된 관심사 종류 이름과 대표 이미지를 제공한다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\test_health.py`
- 검증 결과: 테스트 1개 통과 출력 확인 후 pytest 종료 지연으로 타임아웃
