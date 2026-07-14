## API 테스트 결과

### 요약

- 정상 작동하는 API: 없음
- 실패 및 수정이 필요한 API: `/api/analyses/screenshot`

### 1. POST /api/analyses/screenshot

- 정상 작동 안함
- 응답: 500 Internal Server Error
- 에러 코드: `OCR_FAILED`
- 요청 형식: `multipart/form-data`
  - `url=https://example.com/screenshot-test`
  - `title=스크린샷 API 테스트`
  - `image=@blanker-screenshot-api-test.png;type=image/png`

### 실패 원인

- 서버가 업로드된 이미지 요청은 받았으나 OCR 단계에서 실패함
- 이전 직접 확인 결과 로컬 환경에 Tesseract 실행 파일이 없거나 PATH에 등록되어 있지 않아 `TesseractNotFoundError`가 발생함

### 조치 필요

- Tesseract OCR 실행 파일 설치
- `tesseract --version` 명령 확인
- FastAPI 서버 재시작 후 재테스트
