## API 테스트 결과

### 요약

- 정상 작동하는 API: 재기동 환경의 `/api/analyses/screenshot`
- 실패 및 수정이 필요한 API: 현재 8000 포트 서버의 `/api/analyses/screenshot`

### 1. Tesseract 언어 데이터 확인

- `tesseract --list-langs` 결과:
  - `eng`
  - `kor`
  - `osd`

### 2. POST /api/analyses/screenshot - 현재 8000 포트 서버

- 정상 작동 안함
- 응답: 500 Internal Server Error
- 에러 코드: `OCR_FAILED`
- 요청 형식: `multipart/form-data`
  - `url=https://example.com/screenshot-test-kor`
  - `title=스크린샷 API 한국어 테스트`
  - `image=@blanker-screenshot-api-test-kor.png;type=image/png`

### 3. POST /api/analyses/screenshot - Tesseract 환경 명시 후 임시 8001 포트 서버

- 정상 작동
- 응답: 200 OK

```json
{
  "success": true,
  "data": {
    "analysisRequestId": "analysis_request_6",
    "extractedText": "테 스 트 스 포 일 러 결 말 내 용\n\ntest spoiler ending text",
    "categories": ["SPOILER"],
    "riskLevel": "MEDIUM",
    "relevanceLevel": "LOW",
    "shouldBlock": false,
    "blockAction": null
  }
}
```

### 확인 내용

- 한국어 언어 데이터 설치 자체는 정상임
- 로컬 직접 OCR도 실행됨
- `PATH`와 `TESSDATA_PREFIX`를 명시한 새 서버 프로세스에서는 API가 정상 동작함
- 현재 8000 포트 서버 프로세스는 Tesseract 언어 데이터 경로를 제대로 인식하지 못하는 상태로 보임

### 조치 필요

- 8000 포트 서버를 완전히 종료한 뒤 새 터미널에서 재실행
- 실행 전 환경 변수 확인:

```powershell
$env:PATH = "C:\Program Files\Tesseract-OCR;" + $env:PATH
$env:TESSDATA_PREFIX = "C:\Program Files\Tesseract-OCR\tessdata"
```
