# 038. 관심사 종류 기본 데이터 스크립트 동작 확인

## 작업 개요
- 작업명: 관심사 종류 기본 데이터 스크립트 동작 확인
- 관련 TASK: `TASK.md`
- 관련 API/문서: `GET /api/interests/types`
- 커밋 메시지: `feat: 관심사 종류 기본 데이터 스크립트 검증`

## 변경한 파일
- `docs/task/038-verify-default-interest-type-seed-script.md`
- `TASK.md`

## 구체적인 구현 내용
- `seed_default_interest_types.py`를 실행해 기본 관심사 종류 8개가 적재되는지 확인했다.
- 같은 스크립트를 재실행해 중복 적재 없이 `imported=0`으로 끝나는지 확인했다.
- 인증 토큰으로 `/api/interests/types`를 호출해 종류별 preview image URL이 반환되는지 확인했다.
- 완료된 `TASK.md` 항목을 체크했다.

## 검증 내용
- 실행 명령: `uv --cache-dir D:\project\blanker\.uv-cache run python scripts\seed_default_interest_types.py`
- 검증 결과: 최초 `default_interest_types=8 imported=8`, 재실행 `default_interest_types=8 imported=0`
- 실행 명령: `GET http://127.0.0.1:8000/api/interests/types`
- 검증 결과: 게임, 기타, 드라마, 뮤지컬, 소설, 애니메이션, 영화, 웹툰 및 각 preview image URL 반환
