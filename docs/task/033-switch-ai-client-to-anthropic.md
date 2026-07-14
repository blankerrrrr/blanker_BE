# 033. AI Client Anthropic 전환

## 작업 개요
- 작업명: AI Client Anthropic 전환
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `app/ai/client.py`
- 커밋 메시지: `feat: AI Client Anthropic 전환`

## 변경한 파일
- `backend/app/ai/client.py`
- `backend/app/core/config.py`
- `backend/pyproject.toml`
- `backend/tests/unit/test_ai_client.py`
- `docs/backend-architecture.md`

## 구체적인 구현 내용
- OpenAI SDK 의존과 `OPENAI_*` 설정을 제거했다.
- `ANTHROPIC_API_KEY`, `AI_REQUEST_TIMEOUT_SECONDS` 설정을 사용하도록 변경했다.
- Anthropic Messages API를 표준 라이브러리 HTTP 호출로 요청하도록 구현했다.
- 모델명은 env로 받지 않고 클라이언트 내부 기본값으로 처리했다.
- AI client 단위 테스트를 Anthropic 응답 더블 기준으로 수정했다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit\test_ai_client.py -q`
- 검증 결과: 테스트 6개 통과 출력 확인 후 pytest 종료 지연으로 타임아웃
