# 036. 관심사 종류 기본 데이터 스크립트 추가

## 작업 개요
- 작업명: 관심사 종류 기본 데이터 스크립트 추가
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `GET /api/interests/types`
- 커밋 메시지: `feat: 관심사 종류 기본 데이터 스크립트 추가`

## 변경한 파일
- `backend/scripts/seed_default_interest_types.py`
- `TASK.next.md`

## 구체적인 구현 내용
- 관심사 종류별 preview image URL을 `PreviewImage` enum으로 정의했다.
- 외부 API 키 없이 실행 가능한 기본 관심사 종류 seed 스크립트를 추가했다.
- `InterestCatalogImportService`를 재사용해 중복 없이 기본 행을 저장하도록 했다.
- 완료된 `TASK.next.md` 항목을 체크했다.

## 변경된 플로우
- 요청: `GET /api/interests/types`
- 처리: `interests` 테이블에 저장된 관심사 종류와 `interest_type_image_url`을 그룹 조회
- 응답: 기본 seed 실행 후 영화, 드라마, 애니메이션, 소설, 게임, 뮤지컬, 웹툰, 기타 종류와 대표 이미지 반환

## 검증 내용
- 실행 명령: `uv --cache-dir D:\project\blanker\.uv-cache run ruff check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `uv --cache-dir D:\project\blanker\.uv-cache run pytest`
- 검증 결과: 50 passed
