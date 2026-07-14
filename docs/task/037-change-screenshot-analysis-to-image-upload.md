# 037. 스크린샷 분석 API 이미지 업로드 방식 변경

## 작업 개요
- 작업명: 스크린샷 분석 API 이미지 업로드 방식 변경
- 관련 TASK: `TASK.md`
- 관련 API/문서: `POST /api/analyses/screenshot`
- 커밋 메시지: `feat: 스크린샷 분석 API 이미지 업로드 방식 변경`

## 변경한 파일
- `backend/app/api/screenshot_analysis_requests.py`
- `backend/app/schemas/screenshot_analysis.py`
- `backend/app/services/screenshot_analysis_service.py`
- `backend/tests/unit/test_analysis_api.py`
- `backend/pyproject.toml`
- `backend/uv.lock`
- `docs/api-spec/POST-api-analyses-screenshot.md`
- `TASK.md`

## 구체적인 구현 내용
- 스크린샷 분석 API 요청을 JSON URL 캡처 방식에서 `multipart/form-data` 이미지 업로드 방식으로 변경했다.
- 서버 캡처를 제거하고 업로드된 이미지 bytes를 OCR에 전달하도록 변경했다.
- multipart 파싱을 위해 `python-multipart` 의존성을 추가했다.
- 기존 분석 API 테스트를 multipart 요청 형식으로 수정했다.
- API 명세에서 Playwright 캡처 설명을 제거하고 이미지 업로드 예시를 추가했다.

## 변경된 플로우
- 요청: `url`, `title`, `image`를 `multipart/form-data`로 전송
- 처리: 서버가 업로드 이미지에서 OCR 텍스트 추출 후 기존 rule 기반 분석 수행
- 응답: 기존과 동일한 분석 결과 반환

## 검증 내용
- 실행 명령: `uv --cache-dir D:\project\blanker\.uv-cache run ruff check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `uv --cache-dir D:\project\blanker\.uv-cache run pytest`
- 검증 결과: 50 passed
