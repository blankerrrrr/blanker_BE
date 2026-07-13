# 026. 내부 스키마 생성 인자 snake_case 정리

## 작업 개요
- 요청/응답 JSON alias를 제외한 Python 내부 객체 생성 인자를 snake_case로 정리했다.
- 서비스 계층에서 응답 스키마 생성 시 camelCase 키워드를 넘기던 문제를 수정했다.

## 변경 파일
- `backend/app/services/auth_service.py`
- `backend/app/services/analysis_service.py`
- `backend/app/services/blocked_item_service.py`
- `backend/app/services/block_setting_service.py`
- `backend/app/services/duplicate_group_service.py`
- `backend/app/services/interest_item_service.py`
- `backend/app/services/interest_target_service.py`
- `backend/app/ai/duplicate_detector.py`
- `backend/app/ai/pipeline.py`
- `backend/tests/unit/test_ai_client.py`
- `backend/tests/unit/test_ai_duplicate_detector.py`
- `backend/tests/unit/test_ai_pipeline.py`
- `backend/tests/unit/test_ai_prompts.py`
- `backend/tests/unit/test_ai_schemas.py`

## 구현 내용
- `CamelModel`의 alias 기능은 유지하고, Python 코드에서는 필드명 기준의 snake_case를 사용하게 했다.
- AI 내부 스키마와 테스트도 camelCase alias 입력 대신 snake_case 필드명으로 정리했다.
- 서비스 응답 생성 코드는 `access_token`, `total_elements`, `interest_item_id` 등 내부 필드명으로 통일했다.

## 검증
- `rg "[A-Za-z0-9]+[A-Z][A-Za-z0-9]*=" backend/app backend/tests -g "*.py"`
- `uv --cache-dir D:\project\blanker\.uv-cache run ruff check . --no-cache`
- `uv --cache-dir D:\project\blanker\.uv-cache run pytest tests/unit/test_ai_schemas.py tests/unit/test_ai_prompts.py tests/unit/test_ai_client.py tests/unit/test_ai_duplicate_detector.py tests/unit/test_ai_pipeline.py -q`

## 비고
- pytest는 영향 테스트 18개 통과 출력까지 확인했으나 프로세스 종료 단계에서 타임아웃됐다.
