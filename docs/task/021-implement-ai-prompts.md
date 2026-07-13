# 021. AI 프롬프트 구현

## 작업 개요
- AI placeholder 중 `backend/app/ai/prompts.py`를 실제 프롬프트 정의 모듈로 구현했다.
- 콘텐츠 분류와 중복 탐지에 사용할 시스템 프롬프트와 유저 프롬프트 빌더를 추가했다.

## 변경 파일
- `backend/app/ai/prompts.py`
- `backend/tests/unit/test_ai_prompts.py`

## 구현 내용
- 콘텐츠 분류 프롬프트는 enum 값과 JSON 응답 형식을 명시한다.
- 중복 탐지 프롬프트는 중복 여부, 대표 ID, 점수, 사유를 JSON으로 받도록 정의한다.
- 유저 프롬프트 빌더는 관심사 목록을 정렬해 같은 입력에서 같은 문자열이 나오도록 했다.

## 검증
- `uv --cache-dir D:\project\blanker\.uv-cache run ruff check . --no-cache`
- `uv --cache-dir D:\project\blanker\.uv-cache run pytest tests/unit/test_ai_prompts.py -q`
- pytest는 테스트 4개 통과 출력까지 확인했으나 프로세스 종료 단계에서 타임아웃됐다.
