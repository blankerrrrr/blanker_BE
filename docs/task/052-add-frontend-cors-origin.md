# 052. 프론트엔드 CORS Origin 허용

## 작업 개요
- 작업명: 프론트엔드 도메인 CORS 허용 설정 추가
- 관련 API/문서: 전체 API
- 커밋 메시지: `feat: 프론트엔드 CORS 허용 추가`

## 변경한 파일
- `backend/app/core/config.py`
- `backend/app/main.py`
- `backend/tests/test_health.py`
- `docs/task/052-add-frontend-cors-origin.md`

## 구체적인 구현 내용
- FastAPI에 CORS 미들웨어를 추가했다.
- `CORS_ALLOW_ORIGINS` 환경 변수로 허용 Origin을 설정하도록 구성했다.
- 인증 정보를 포함한 교차 출처 요청을 허용했다.
- 해당 Origin의 사전 요청 응답을 검증하는 테스트를 추가했다.

## 검증 내용
- 실행 명령: `uv --cache-dir .uv-cache run pytest tests/test_health.py -q`
- 검증 결과: 2 passed
- 실행 명령: `uv --cache-dir .uv-cache run ruff check app/main.py app/core/config.py tests/test_health.py`
- 검증 결과: 통과
