# 022. AI 클라이언트 구현

## 작업 개요
- AI placeholder 중 `backend/app/ai/client.py`를 실제 클라이언트 계약 모듈로 구현했다.
- 현재 의존성에 OpenAI SDK가 없으므로 네트워크 호출은 만들지 않고, 설정과 실패 처리를 명확히 했다.

## 변경 파일
- `backend/app/ai/client.py`
- `backend/tests/unit/test_ai_client.py`

## 구현 내용
- `AIClient`는 `OPENAI_API_KEY`, `OPENAI_REQUEST_TIMEOUT_SECONDS` 설정을 사용한다.
- API 키가 없으면 `AIClientUnavailableError`를 발생시킨다.
- SDK 연동이 아직 없는 호출은 명시적으로 미구현 예외를 발생시킨다.
- 분류/중복 탐지 호출 시 사용할 프롬프트 빌더 연결 지점을 만들었다.

## 검증
- `uv --cache-dir D:\project\blanker\.uv-cache run ruff check . --no-cache`
- `uv --cache-dir D:\project\blanker\.uv-cache run pytest tests/unit/test_ai_client.py -q`
- pytest는 테스트 4개 통과 출력까지 확인했으나 프로세스 종료 단계에서 타임아웃됐다.

## 비고
- 현재 API 분석 흐름은 기존 `RuleBasedContentClassifier`를 계속 사용한다.
- OpenAI 실제 호출은 SDK 의존성 추가와 응답 파싱 정책이 정해진 뒤 별도 작업으로 붙이는 것이 맞다.
