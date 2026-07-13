# 003-add-ai-env

## 작업 개요
- 작업명: AI 호출 환경 변수 추가
- 관련 TASK: AI 호출에 필요한 env 추가
- 관련 API/문서: `docs/tech-stack.md`
- 커밋 메시지: `feat: AI 호출 환경 변수 추가`

## 변경한 파일
- `backend/app/core/config.py`
- `backend/.env.example`
- `TASK.md`

## 구체적인 구현 내용
- OpenAI API key 설정 값을 추가했다.
- OpenAI 모델명 설정 값을 추가했다.
- OpenAI 요청 timeout 설정 값을 추가했다.
- 로컬 환경 변수 예시 파일에 AI 호출 관련 값을 반영했다.

## 검증 내용
- 실행 명령:
- 미검증 사유: 설정 값 추가만 수행하여 별도 실행 검증은 생략했다.

## 참고
-
