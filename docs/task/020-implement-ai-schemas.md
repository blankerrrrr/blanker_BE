# 020. AI 내부 스키마 구현

## 작업 개요
- AI placeholder 중 `backend/app/ai/schemas.py`를 실제 내부 계약 모델로 구현했다.
- 분석 입력, 분류 결과, 중복 후보, 중복 결과 모델을 추가했다.

## 변경 파일
- `backend/app/ai/schemas.py`
- `backend/tests/unit/test_ai_schemas.py`

## 구현 내용
- `AnalysisInput`은 콘텐츠 본문, 이미지 URL, 대체 텍스트, 문맥을 하나의 `content_text`로 합친다.
- `ClassificationResult`는 위험도와 관련도 기준으로 `should_block`을 계산한다.
- `DuplicateCandidate`는 중복 탐지용 검색 문자열을 제공한다.
- `DuplicateResult`는 중복 여부, 대표 항목, 점수, 사유를 표현한다.

## 검증
- `uv run ruff check .`
- `uv run pytest tests/unit/test_ai_schemas.py`
- 홈 디렉터리 `uv`/`ruff` 캐시 권한 문제로 워크스페이스 캐시와 `--no-cache`를 사용했다.
- pytest는 테스트 5개 통과 출력까지 확인했으나 프로세스 종료 단계에서 타임아웃됐다.

## 비고
- 기존 API 응답 스키마의 enum을 재사용해 내부 AI 스키마와 외부 분석 응답의 값이 어긋나지 않도록 했다.
