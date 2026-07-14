# 042. 관심사 종류 테이블 분리

## 작업 개요
- 작업명: 관심사 종류와 관심사 테이블 분리
- 관련 TASK: `TASK.md`
- 관련 API/문서: `GET /api/interests/types`, `GET /api/interests`, `docs/data-modeling.md`
- 커밋 메시지: `feat: 관심사 종류 테이블 분리`

## 변경한 파일
- `backend/app/db/models/interest.py`
- `backend/app/db/models/__init__.py`
- `backend/app/db/repositories/interest_repository.py`
- `backend/app/services/interest_catalog_import_service.py`
- `backend/app/services/interest_service.py`
- `backend/scripts/seed_default_interest_types.py`
- `backend/alembic/versions/20260714_0014_split_interest_catalog.py`
- `docs/data-modeling.md`
- `docs/task/042-split-interest-catalog-table.md`

## 구체적인 구현 내용
- `interest_catalog` 테이블을 추가하고 `name`, `image_url`로 관심사 종류를 관리하도록 했다.
- `interests`가 `interest_catalog_id` FK를 통해 관심사 종류를 참조하도록 모델과 마이그레이션을 추가했다.
- 관심사 종류 조회는 `interest_catalog`를 직접 조회하도록 변경했다.
- 관심사 목록/선택 응답은 기존 API 필드(`interestType`, `interestTypeImageUrl`)를 유지하되 catalog 관계에서 값을 채우도록 변경했다.
- 기본 관심사 종류 seed 스크립트가 `interests`가 아니라 `interest_catalog`에 적재되도록 변경했다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: `56 passed`
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `.\.venv\Scripts\alembic.exe upgrade head`
- 검증 결과: `20260714_0013 -> 20260714_0014` 마이그레이션 성공
- 실행 명령: `.\.venv\Scripts\python.exe scripts\seed_default_interest_types.py`
- 검증 결과: `default_interest_types=8 imported=0`
- API 확인: `GET /api/interests/types` 200 OK, 기본 8개 종류와 preview image URL 반환
