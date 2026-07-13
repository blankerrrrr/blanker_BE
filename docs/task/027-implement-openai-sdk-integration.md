# 027. OpenAI SDK 연동 구현

## 작업 개요
- `AIClient`가 OpenAI SDK를 통해 JSON 응답을 요청하고 내부 AI 스키마로 파싱하도록 구현했다.
- 테스트에서는 fake OpenAI client를 주입해 실제 네트워크 호출 없이 요청 형태와 응답 파싱을 검증했다.

## 변경 파일
- `backend/app/ai/client.py`
- `backend/app/core/config.py`
- `backend/.env.example`
- `backend/pyproject.toml`
- `backend/uv.lock`
- `backend/tests/unit/test_ai_client.py`

## 구현 내용
- `openai>=1.0.0` 의존성을 추가했다.
- `OPENAI_MODEL` 설정을 추가하고 기본값은 `gpt-4o-mini`로 지정했다.
- `AIClient`는 `AsyncOpenAI`를 지연 생성하고 `chat.completions.create()`에 JSON 응답 형식을 요청한다.
- 분류 응답은 `ClassificationResult`, 중복 탐지 응답은 `DuplicateResult`로 검증한다.
- 응답이 비어 있거나 스키마에 맞지 않으면 `AIClientResponseError`를 발생시킨다.

## 검증
- `uv --cache-dir D:\project\blanker\.uv-cache lock`
- `.\.venv\Scripts\ruff.exe check . --no-cache`
- `.\.venv\Scripts\pytest.exe tests/unit/test_ai_client.py -q`

## 비고
- `uv lock`은 네트워크 승인 후 성공했다.
- `uv run` 기반 검증은 PyPI wheel 다운로드 DNS 실패로 진행하지 못해 기존 `.venv`의 ruff/pytest로 검증했다.
- pytest는 테스트 6개 통과 출력까지 확인했으나 프로세스 종료 단계에서 타임아웃됐다.
