# 035. 스포일러 분석 캡처 방식 변경

## 작업 개요
- 작업명: 스포일러 분석 캡처 방식 변경
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `POST /api/screenshot-analysis-requests`
- 커밋 메시지: `feat: 스크린샷 기반 스포일러 분석 API 추가`

## 변경한 파일
- `backend/app/core/error_codes.py` — SCREENSHOT_FAILED, OCR_FAILED 에러 코드 추가
- `backend/app/core/screenshot.py` — Playwright 기반 스크린샷 캡처 유틸리티 (신규)
- `backend/app/core/ocr.py` — PyTesseract 기반 OCR 유틸리티 (신규)
- `backend/app/schemas/screenshot_analysis.py` — 요청/응답 스키마 (신규)
- `backend/app/services/screenshot_analysis_service.py` — 분석 서비스 (신규)
- `backend/app/api/screenshot_analysis_requests.py` — 라우터 (신규)
- `backend/app/api/router.py` — 라우터 등록
- `backend/pyproject.toml` — playwright, pytesseract, pillow 의존성 추가
- `docs/api-spec/POST-api-screenshot-analysis-requests.md` — API 명세 (신규)

## 구체적인 구현 내용
- 기존 `POST /api/analysis-requests`는 수정하지 않음.
- 새 엔드포인트 `POST /api/screenshot-analysis-requests`를 추가함.
- 클라이언트는 URL만 전달하면 서버가 Playwright로 스크린샷 캡처 → PyTesseract OCR → 기존 RuleBasedContentClassifier로 분석 → 결과 반환.
- 분석 결과는 기존 analysis_requests/analysis_contents/analysis_results 테이블에 저장됨.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\ruff.exe check ... --no-cache`
- 검증 결과: 통과

## 설치 필요 사항 (병목)
- **Tesseract OCR 실행 파일**: 로컬/서버에 별도 설치 필요
  - Windows: `choco install tesseract` 또는 공식 인스톨러 사용
  - Linux: `apt-get install tesseract-ocr tesseract-ocr-kor`
- **Playwright 브라우저 바이너리**: `playwright install chromium` 실행 필요
