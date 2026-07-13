# 007-implement-analysis-api

## 작업 개요
- 작업명: 웹 콘텐츠 분석 API 구현
- 관련 TASK: API 구현 - 웹 콘텐츠 분석
- 관련 API/문서: `docs/api-spec/POST-api-analysis-requests.md`
- 커밋 메시지: `feat: 웹 콘텐츠 분석 API 구현`

## 변경한 파일
- `backend/app/api/analysis_requests.py`
- `backend/app/services/analysis_service.py`
- `backend/app/ai/content_classifier.py`
- `backend/app/db/models/analysis.py`
- `backend/app/db/repositories/analysis_repository.py`
- `backend/app/schemas/analysis.py`
- `backend/app/core/error_codes.py`
- `backend/alembic/versions/20260713_0004_create_analysis_tables.py`
- `TASK.md`

## 구체적인 구현 내용
- 콘텐츠 분석 요청 API를 추가했다.
- 분석 요청, 콘텐츠 단위, 분석 결과 저장 모델과 migration을 추가했다.
- 등록된 관심 대상과 rule 기반 키워드 분류로 위험도, 관련도, 차단 여부를 계산한다.
- 요청 콘텐츠 개수와 전체 텍스트 크기 제한을 추가했다.

## 변경된 플로우
- 요청: 확장 프로그램이 페이지 정보와 콘텐츠 단위 목록을 전달한다.
- 처리: service가 요청/콘텐츠를 저장하고 관심 대상 기반 rule 분석 결과를 저장한다.
- 응답: 콘텐츠별 categories, riskLevel, relevanceLevel, shouldBlock, blockAction을 반환한다.

## 검증 내용
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m ruff check app alembic tests --no-cache`
- 검증 결과: ruff 검사 통과
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "import app.main; print('ok')"`
- 검증 결과: 앱 import 성공
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "from fastapi.testclient import TestClient; from app.main import app; r=TestClient(app).get('/health'); print(r.status_code); print(r.json())"`
- 검증 결과: `/health` 200 응답 확인
- 미검증 사유: DB 연동 API 시나리오는 로컬 PostgreSQL/Redis 준비 상태를 확인하지 못해 생략했다.

## 참고
-
