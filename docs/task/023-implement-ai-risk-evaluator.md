# 023. AI 위험도 평가기 구현

## 작업 개요
- AI placeholder 중 `backend/app/ai/risk_evaluator.py`를 실제 위험도 평가 모듈로 구현했다.
- 기존 `RuleBasedContentClassifier`에 있던 관련도, 위험도, 차단 사유 계산 책임을 분리했다.

## 변경 파일
- `backend/app/ai/risk_evaluator.py`
- `backend/app/ai/content_classifier.py`
- `backend/tests/unit/test_ai_risk_evaluator.py`

## 구현 내용
- 관련 토픽 개수에 따라 `RelevanceLevel`을 계산한다.
- 스포일러/유해 콘텐츠 여부와 관련도에 따라 `RiskLevel`을 계산한다.
- 차단 사유 우선순위를 스포일러, 유해 콘텐츠, 관심 대상 순으로 유지한다.
- 규칙 기반 분류기는 키워드 탐지만 담당하고 위험도 판단은 `RiskEvaluator`에 위임한다.

## 검증
- `uv --cache-dir D:\project\blanker\.uv-cache run ruff check . --no-cache`
- `uv --cache-dir D:\project\blanker\.uv-cache run pytest tests/unit/test_ai_risk_evaluator.py -q`
- pytest는 테스트 5개 통과 출력까지 확인했으나 프로세스 종료 단계에서 타임아웃됐다.
