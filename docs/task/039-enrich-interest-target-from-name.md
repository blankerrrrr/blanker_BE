# 039. 관심사 직접 등록 AI 보강 적용

## 작업 개요
- 작업명: 관심사 직접 등록 AI 보강 적용
- 관련 TASK: 사용자 요청
- 관련 API/문서: `POST /api/interests/targets`
- 커밋 메시지: `feat: 관심사 직접 등록 AI 보강 적용`

## 변경한 파일
- `backend/app/ai/client.py`
- `backend/app/ai/prompts.py`
- `backend/app/ai/schemas.py`
- `backend/app/schemas/interest_target.py`
- `backend/app/services/interest_target_service.py`
- `backend/tests/unit/test_ai_client.py`
- `backend/tests/unit/test_ai_prompts.py`
- `backend/tests/unit/test_ai_schemas.py`
- `backend/tests/unit/test_interest_api.py`
- `docs/api-test/http/interests.http`

## 구체적인 구현 내용
- `/api/interests/targets` 요청을 `name`만 받도록 변경했다.
- Anthropic 설정이 있으면 `type`, `aliases`, `keywords`를 AI로 보강한다.
- AI 미설정 또는 실패 시 `WORK`, 빈 별칭, `name` 기반 키워드로 저장한다.
- 관련 AI 클라이언트, 프롬프트, 스키마, API 테스트 예시를 수정했다.

## 변경된 플로우
- 요청: `{ "name": "작품명" }`
- 처리: AI 보강 시도 후 실패하면 MVP fallback 적용
- 응답: 보강된 `type`, `aliases`, `keywords`를 포함한 관심 대상 반환

## 검증 내용
- 실행 명령: `uv --cache-dir D:\project\blanker\.uv-cache run ruff check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `uv --cache-dir D:\project\blanker\.uv-cache run pytest`
- 검증 결과: 55 passed
