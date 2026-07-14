# 스크린샷 분석 요청 API

`POST /api/screenshot-analysis-requests`

## 설명

서버가 지정된 URL의 스크린샷을 직접 캡처하고, Tesseract OCR로 텍스트를 추출하여 스포일러 및 유해 콘텐츠를 분석한다. 기존 DOM 기반 분석 방식의 대안으로, 클라이언트가 DOM을 분석할 필요 없이 URL만 제공하면 된다.

> **주의:** 서버에 Tesseract OCR 실행 파일과 Playwright 브라우저 바이너리가 설치되어 있어야 동작한다.

## REQUEST

### Header

| Header | 필수 | 설명 |
| --- | --- | --- |
| `Authorization` | Yes | `Bearer {accessToken}` |

### Body

```json
{
  "url": "https://example.com/article",
  "title": "페이지 제목"
}
```

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `url` | string | Yes | 분석할 페이지 URL |
| `title` | string | No | 페이지 제목 |

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
| `SCREENSHOT_FAILED` | 502 | 페이지 스크린샷 캡처 실패 (URL 접근 불가 등) |
| `OCR_FAILED` | 500 | 스크린샷에서 텍스트 추출 실패 |
