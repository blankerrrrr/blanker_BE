## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/analyses/screenshot`
- 실패 및 수정이 필요한 API: 없음

### 1. POST /api/analyses/screenshot

- 재기동한 FastAPI 서버 기준 정상 작동
- 응답: 200 OK
- 요청 형식: `multipart/form-data`
  - `url=https://example.com/screenshot-test`
  - `title=스크린샷 API 테스트`
  - `image=@blanker-screenshot-api-test.png;type=image/png`

### 응답 확인

```json
{
  "success": true,
  "data": {
    "analysisRequestId": "analysis_request_5",
    "extractedText": "test spoiler ending text",
    "categories": ["SPOILER"],
    "riskLevel": "MEDIUM",
    "relevanceLevel": "LOW",
    "shouldBlock": false,
    "blockAction": null
  }
}
```

### 확인 내용

- `tesseract --version` 실행 성공: `tesseract v5.4.0.20240606`
- 직접 OCR 실행 성공: `test spoiler ending text`
- 기존 8000 포트 서버는 설치 전 PATH를 유지해 `OCR_FAILED`를 반환함
- Tesseract 경로를 포함한 새 서버 프로세스에서 API 호출 성공

### 참고

- 현재 `tesseract --list-langs` 결과는 `eng`, `osd`만 표시됨
- 한국어 스크린샷 분석까지 검증하려면 `kor.traineddata` 설치 후 한국어 이미지로 추가 테스트 필요
