# 024. AI 중복 탐지기 구현

## 작업 개요
- AI placeholder 중 `backend/app/ai/duplicate_detector.py`를 실제 중복 탐지 모듈로 구현했다.
- 외부 AI 호출 없이 URL과 텍스트 유사도로 중복 후보를 판단한다.

## 변경 파일
- `backend/app/ai/duplicate_detector.py`
- `backend/tests/unit/test_ai_duplicate_detector.py`

## 구현 내용
- 동일 URL은 점수 1.0의 중복으로 판단한다.
- URL이 다르면 제목, URL, 요약, 관련 토픽을 합친 검색 문자열을 정규화해 유사도를 계산한다.
- 기본 중복 기준값은 `0.86`으로 설정했다.

## 검증
- `uv --cache-dir D:\project\blanker\.uv-cache run ruff check . --no-cache`
- `uv --cache-dir D:\project\blanker\.uv-cache run pytest tests/unit/test_ai_duplicate_detector.py -q`
- pytest는 테스트 3개 통과 출력까지 확인했으나 프로세스 종료 단계에서 타임아웃됐다.
