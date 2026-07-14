# 스크린샷 분석 요청 API

`POST /api/analyses/screenshot`

## 설명

클라이언트가 캡처한 스크린샷 이미지를 서버로 전송하면, 서버가 Tesseract OCR로 텍스트를 추출하여 스포일러 및 유해 콘텐츠를 분석한다. 확장 프로그램은 `chrome.tabs.captureVisibleTab()` 등으로 현재 탭 이미지를 캡처한 뒤 업로드한다.

> **주의:** 서버에 Tesseract OCR 실행 파일이 설치되어 있어야 동작한다.

## REQUEST

### Header

| Header | 필수 | 설명 |
| --- | --- | --- |
| `Authorization` | Yes | `Bearer {accessToken}` |

### Body `multipart/form-data`

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `url` | string | Yes | 이미지가 캡처된 페이지 URL |
| `title` | string | No | 페이지 제목 |
| `image` | file | Yes | 캡처된 스크린샷 이미지 파일. 예: PNG, JPEG |

### 예시

```bash
curl -X POST "http://localhost:8000/api/analyses/screenshot" \
  -H "Authorization: Bearer {accessToken}" \
  -F "url=https://example.com/article" \
  -F "title=페이지 제목" \
  -F "image=@screenshot.png;type=image/png"
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "analysisRequestId": "analysis_request_1",
    "extractedText": "스크린샷에서 추출된 텍스트 내용...",
    "categories": ["SPOILER"],
    "riskLevel": "HIGH",
    "relevanceLevel": "HIGH",
    "shouldBlock": true,
    "blockAction": {
      "unitType": "TEXT",
      "reason": "등록한 관심 작품과 관련된 스포일러 가능성이 높습니다.",
      "relatedTopics": ["작품명"]
    }
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 없음 또는 유효하지 않음 |
| `OCR_FAILED` | 500 | 스크린샷에서 텍스트 추출 실패 |
