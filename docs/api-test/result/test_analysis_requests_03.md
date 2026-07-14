## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/analyses`
- 실패 및 수정이 필요한 API: `/api/analyses/screenshot`

### 1. POST /api/analyses

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 페이지 정보와 콘텐츠 단위 요청 분석 성공
- 확인 결과: `INTEREST`, `SPOILER`, `riskLevel=HIGH`, `shouldBlock=true`

### 2. POST /api/analyses/screenshot

- 정상 작동 안함
- 응답: 500 Internal Server Error
- 에러 코드: `OCR_FAILED`
- 요청 형식: `multipart/form-data`로 `url`, `title`, `image` 전송
- 실패 원인: 로컬 서버 환경에 Tesseract 실행 파일이 설치되어 있지 않거나 PATH에 없어 OCR 실행 실패
- 추가 확인: 같은 이미지로 `extract_text(...)` 직접 실행 시 `TesseractNotFoundError` 발생
- 조치 필요: 로컬/서버 환경에 Tesseract OCR 실행 파일 설치 및 PATH 설정 후 재테스트
