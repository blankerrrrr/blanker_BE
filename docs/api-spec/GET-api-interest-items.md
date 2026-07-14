# 관심 정보 목록 조회 API

`GET /api/interest-items?page=1&size=20`

## 설명

자동 수집된 관심 정보 목록을 페이지 단위로 조회한다.

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
        "interestItemId": "interest_item_1",
        "title": "관심 정보 제목",
        "summary": "관심 정보 요약",
        "relatedTopics": ["작품명"],
        "discoveredAt": "2026-07-13T05:00:00Z"
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
