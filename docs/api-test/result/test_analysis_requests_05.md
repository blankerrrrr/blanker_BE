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

### 확인 내용

- Tesseract 실행 파일 설치 위치 확인: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- 직접 실행 확인: `tesseract v5.4.0.20240606`
- 현재 셸에서 임시 PATH 추가 후 `extract_text(...)` 직접 실행 성공
- 직접 OCR 결과: `testspollerending text`

### 실패 원인

- 현재 실행 중인 API 서버 프로세스가 `C:\Program Files\Tesseract-OCR` 경로를 PATH로 인식하지 못하는 상태로 보임
- 서버 프로세스 재시작 전까지 `/api/analyses/screenshot`은 계속 `OCR_FAILED`를 반환할 수 있음

### 조치 필요

- 시스템 PATH에 `C:\Program Files\Tesseract-OCR` 추가
- FastAPI 서버 재시작
- 재시작 후 `/api/analyses/screenshot` 재테스트
