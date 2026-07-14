## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/analyses/screenshot`
- 실패 및 수정이 필요한 API: 없음

### 1. 원인

- 기존 8000 포트 서버가 `C:\Python312\python.exe -m uvicorn app.main:app --reload`로 실행 중이었음
- 해당 전역 파이썬에는 `pytesseract`가 설치되어 있지 않아 스크린샷 분석 요청에서 `OCR_FAILED`가 발생했음
- 프로젝트 가상환경 `backend\.venv\Scripts\python.exe`에는 필요한 의존성이 설치되어 있음

### 2. 조치

- 기존 uvicorn reload 부모/자식 프로세스 종료
- 프로젝트 가상환경 파이썬으로 서버 재시작:

```text
D:\project\blanker\backend\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### 3. POST /api/analyses/screenshot

- API 정상 작동
- 응답: 200 OK
- 요청 형식: `multipart/form-data`
  - `url=https://example.com/screenshot-test-venv`
  - `title=스크린샷 API 가상환경 재테스트`
  - `image=@blanker-screenshot-api-test-20260714.png;type=image/png`

### 응답 확인

```json
{
  "success": true,
  "data": {
    "analysisRequestId": "analysis_request_7",
    "extractedText": "테 스 트 스 포 일 러 결 말 내 용\n\ntest spoiler ending text",
    "categories": ["SPOILER"],
    "riskLevel": "MEDIUM",
    "relevanceLevel": "LOW",
    "shouldBlock": false,
    "blockAction": null
  }
}
```

### 추가 검증

```text
.\.venv\Scripts\pytest.exe tests\unit\test_ocr.py tests\unit\test_analysis_api.py -q
9 passed
```
