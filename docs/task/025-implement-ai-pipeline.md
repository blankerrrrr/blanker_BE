# 025. AI 분석 파이프라인 구현

## 작업 개요
- AI placeholder 중 `backend/app/ai/pipeline.py`를 실제 분석 파이프라인 모듈로 구현했다.
- 규칙 기반 콘텐츠 분류와 중복 탐지를 하나의 진입점에서 사용할 수 있게 했다.

## 변경 파일
- `backend/app/ai/pipeline.py`
- `backend/tests/unit/test_ai_pipeline.py`

## 구현 내용
- `AnalysisPipeline.classify()`는 `AnalysisInput`을 받아 `ClassificationResult`를 반환한다.
- `AnalysisPipeline.detect_duplicate()`는 `DuplicateDetector`에 중복 탐지를 위임한다.
- 현재 API 서비스는 기존 `RuleBasedContentClassifier` 흐름을 유지하며, 이후 서비스 통합은 별도 변경으로 진행할 수 있다.

## 검증
- `uv --cache-dir D:\project\blanker\.uv-cache run ruff check . --no-cache`
- `uv --cache-dir D:\project\blanker\.uv-cache run pytest tests/unit/test_ai_pipeline.py -q`
- pytest는 테스트 2개 통과 출력까지 확인했으나 프로세스 종료 단계에서 타임아웃됐다.
