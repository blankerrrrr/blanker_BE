# 062. 개인 관심사 직접 등록 안정성 개선

## 작업 개요
- 작업명: 개인 관심사 직접 등록의 입력 및 중복 처리 개선
- 관련 API: `POST /api/interests/targets`
- 커밋 메시지: `fix: 개인 관심사 등록 중복 처리 개선`

## 변경 내용
- 관심사 이름의 앞뒤 공백을 제거하고 1~200자로 검증한다.
- AI 호출 전에 대소문자와 앞뒤 공백을 무시해 사용자별 중복을 확인한다.
- 동일 기준의 DB 고유 인덱스를 추가해 동시 요청 중복을 방지한다.
- DB 중복 오류를 `INTEREST_TARGET_ALREADY_EXISTS` 409 응답으로 변환한다.

## 검증 내용
- 실행 명령: `uv --cache-dir .uv-cache run pytest tests/unit -q --basetemp=.pytest-all-target-hardening`
- 검증 결과: 88 passed
- 실행 명령: `uv --cache-dir .uv-cache run ruff check app alembic/versions/20260715_0020_add_interest_target_name_unique_index.py tests/unit/test_interest_api.py tests/unit/test_interest_target_service.py`
- 검증 결과: 통과
