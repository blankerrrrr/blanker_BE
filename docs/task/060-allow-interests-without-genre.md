# 060. 장르 없는 관심사 저장

## 작업 개요
- 작업명: `전체` 장르 생성을 제거하고 장르 없음 허용
- 관련 테이블: `interest_genres`, `interest_genre_mappings`
- 커밋 메시지: `fix: 전체 장르 자동 생성 제거`

## 변경 내용
- 외부 API에 장르가 없으면 import 데이터의 `genres`를 `null`로 처리한다.
- 장르가 없는 관심사는 장르 및 매핑 행을 생성하지 않는다.
- 기존 `전체` 장르와 관련 매핑을 제거하는 마이그레이션을 추가한다.

## 검증 내용
- 실행 명령: `uv --cache-dir .uv-cache run pytest tests/unit -q --basetemp=.pytest-all-no-all-genre`
- 검증 결과: 83 passed
- 실행 명령: `uv --cache-dir .uv-cache run ruff check app/services/interest_catalog_import_service.py scripts/import_interests.py alembic/versions/20260715_0019_remove_all_genre.py tests/unit/test_import_interests.py`
- 검증 결과: 통과
