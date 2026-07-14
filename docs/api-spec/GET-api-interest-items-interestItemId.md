# 관심 정보 상세 조회 API

`GET /api/interest-items/{interestItemId}`

## 설명

수집된 관심 정보의 상세 내용을 조회한다. 원본 링크, 페이지 내 위치, 관련 주제, 발견 시각을 확인할 수 있다.

## REQUEST

```json
{}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "interestItemId": "interest_item_1",
    "title": "관심 정보 제목",
    "summary": "관심 정보 요약",
    "imageUrl": "https://blanker-storage.s3.ap-northeast-2.amazonaws.com/interest-items/user_1/interest_item_1/image.png",
    "relatedTopics": ["작품명"],
    "sourceUrl": "https://example.com/article",
    "selector": "article",
    "discoveredAt": "2026-07-13T05:00:00Z"
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INTEREST_ITEM_NOT_FOUND` | 404 | 관심 정보를 찾을 수 없음 |
