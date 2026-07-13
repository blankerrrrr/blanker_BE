# 보관함 저장 API

`POST /api/blocked-items`

## 설명

차단된 콘텐츠를 나중에 보기 보관함에 저장한다. 원본 링크, 페이지 내 위치, 차단 유형, 관련 주제를 함께 기록한다.

## REQUEST

```json
{
  "analysisRequestId": "analysis_request_1",
  "clientContentId": "node_001",
  "summary": "차단된 콘텐츠 요약",
  "categories": ["SPOILER"],
  "relatedTopics": ["작품명"],
  "sourceUrl": "https://example.com/article",
  "selector": "article > p:nth-child(1)",
  "positionText": "본문 첫 번째 문단"
}
```

## RESPONSE `201`

```json
{
  "success": true,
  "data": {
    "blockedItemId": "blocked_item_1",
    "savedAt": "2026-07-13T05:00:00Z"
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `BLOCKED_ITEM_ALREADY_EXISTS` | 409 | 이미 저장된 보관함 항목 |
