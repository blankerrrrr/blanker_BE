# 064. 분석 API에 AI 분류 적용

## 작업 개요
- `POST /api/analyses`, `POST /api/analyses/screenshot`의 규칙 기반 분류를 Anthropic AI 우선 흐름으로 변경했다.
- AI를 사용할 수 없을 때 기존 규칙 기반 분류기로 폴백하도록 구성했다.

## 변경 파일
- `backend/app/services/analysis_service.py`
- `backend/app/services/screenshot_analysis_service.py`
- `backend/tests/unit/test_analysis_service.py`
- `docs/task/064-use-ai-for-analysis-apis.md`
- `TASK.md`

## 구현 내용
- 일반 분석 API는 각 콘텐츠와 사용자 관심어를 `AnalysisInput`으로 구성해 `AIClient.classify_content()`에 전달한다.
- 스크린샷 분석 API는 업로드 이미지의 OCR 텍스트와 사용자 관심어를 AI에 전달한다.
- AI의 카테고리, 위험도, 관련도, 관련 주제, 사유를 분석 결과로 저장하고 차단 응답 생성에 사용한다.
- AI API 키 누락, 통신 오류, 잘못된 응답은 기존 `RuleBasedContentClassifier`로 처리한다.
- 서비스 생성자에 AI 클라이언트를 주입할 수 있게 해 외부 호출 없이 흐름을 검증한다.

## 검증
- `uv --cache-dir D:\project\blanker\.uv-cache run ruff check . --no-cache`: 통과
- `uv --cache-dir D:\project\blanker\.uv-cache run pytest tests\unit -q --basetemp=C:\tmp\blanker-pytest-ai-analysis`: 91개 통과, 기존 Starlette 경고 1개
