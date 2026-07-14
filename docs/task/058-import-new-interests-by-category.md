# 058. 분류별 신규 관심사 수집

## 작업 개요
- 작업명: 외부 API에서 분류별 신규 관심사 수집
- 관련 스크립트: `scripts.import_interests`
- 커밋 메시지: `feat: 분류별 신규 관심사 수집 추가`

## 변경 내용
- DB에 저장된 `관심사 분류 + 작품명`을 수집 전에 조회한다.
- 외부 API 결과의 기존 작품과 같은 실행 내 중복 작품을 제외한다.
- 중복으로 수집량이 부족하면 다음 페이지를 조회해 분류별 `--limit`만큼 채운다.
- 영화, 드라마, 애니메이션은 TMDB에서 각각 독립적으로 최대 50개를 수집한다.

## 검증 내용
- 실행 명령: `uv --cache-dir .uv-cache run pytest tests/unit/test_import_interests.py -q --basetemp=.pytest-import`
- 검증 결과: 3 passed
- 실행 명령: `uv --cache-dir .uv-cache run ruff check scripts/import_interests.py app/db/repositories/interest_repository.py tests/unit/test_import_interests.py`
- 검증 결과: 통과
