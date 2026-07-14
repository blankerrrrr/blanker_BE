# 032. AI Provider 기술스택 정정

## 작업 개요
- 작업명: AI Provider 기술스택 정정
- 관련 TASK: 사용자 요청
- 관련 API/문서: `docs/tech-stack.md`, `backend/.env.example`, `TASK.next.md`
- 커밋 메시지: `feat: AI Provider 기술스택 정정`

## 변경한 파일
- `docs/tech-stack.md`
- `backend/.env.example`

## 구체적인 구현 내용
- 기술스택의 AI Provider를 OpenAI API에서 Anthropic API로 정정했다.
- `.env.example`에서 OpenAI 관련 예시 값을 제거했다.
- `.env.example`에 `ANTHROPIC_API_KEY`, `AI_REQUEST_TIMEOUT_SECONDS`만 남겼다.
- 모델명은 알 수 없고 env로 받지 않기로 했으므로 예시에서 제거했다.

## 검증 내용
- 문서 및 env 예시 변경 작업으로 별도 테스트는 수행하지 않았다.

## 추후 추가해야 할 사항
- 현재 `app/ai` 클라이언트 구현은 아직 OpenAI SDK 기준이므로 Anthropic API 기준으로 교체해야 한다.
