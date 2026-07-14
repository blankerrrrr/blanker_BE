# 048. 관심사 장르 목록 조회 API 추가

## 작업 개요
- 작업명: 관심사 장르 목록 조회 API
- 관련 TASK: `TASK.md`
- 관련 API/문서: `GET /api/interests/genres`
- 커밋 메시지: `feat: 관심사 장르 목록 조회 API 추가`

## 변경한 파일
- `backend/app/api/interests.py`
- `backend/app/db/models/interest.py`
- `backend/app/db/models/__init__.py`
- `backend/app/db/repositories/interest_repository.py`
- `backend/app/schemas/interest.py`
- `backend/app/services/interest_service.py`
- `backend/app/services/interest_catalog_import_service.py`
- `backend/scripts/import_interests.py`
- `backend/alembic/versions/20260714_0017_split_interest_genres.py`
- `backend/tests/unit/test_interest_api.py`
- `docs/api-spec/GET-api-interests-genres.md`
- `docs/api-spec/GET-api-interests.md`
- `docs/api-spec/README.md`
- `docs/api-test/http/interests.http`
- `docs/data-modeling.md`
- `docs/erd.md`
- `docs/backend-architecture.md`
- `docs/task/048-add-interest-genre-list-api.md`

## 구체적인 구현 내용
- `interest_genres`, `interest_genre_mappings` 테이블을 추가했다.
- `interests.genre` 컬럼을 제거하고 기존 장르 문자열은 장르 테이블과 매핑 테이블로 이관하도록 했다.
- 같은 관심사 제목이 장르별로 중복 저장된 경우 하나의 관심사로 병합하고 장르 매핑을 합치도록 했다.
- `GET /api/interests/genres?interestType=...` API를 추가했다.
- 외부 API import 시 영화/드라마/애니메이션은 TMDB 장르 목록 API로 장르명을 조회하고, 도서는 `>` 구분자로 장르를 분리 저장하도록 했다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: 67 passed
- 실행 명령: `.\.venv\Scripts\alembic.exe upgrade head`
- 검증 결과: `20260714_0017` 적용 성공
