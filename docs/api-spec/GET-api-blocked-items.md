# 보관함 목록 조회 API

`GET /api/blocked-items?page=1&size=20&type=SPOILER`

## 설명

사용자가 나중에 보기 보관함에 저장한 차단 콘텐츠 목록을 조회한다. 페이지네이션과 유형 필터를 지원한다.

## REQUEST

```json
{}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "blockedItemId": "blocked_item_1",
        "summary": "차단된 콘텐츠 요약",
        "categories": ["SPOILER"],
        "relatedTopics": ["작품명"],
        "sourceUrl": "https://example.com/article",
        "foundAt": "2026-07-13T05:00:00Z"
      }
    ],
    "page": 1,
    "size": 20,
    "totalElements": 1,
    "totalPages": 1
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
