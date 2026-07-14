# 보관함 목록 조회 API

`GET /api/blocked-items?interestTargetId=interest_target_1&page=1&size=20&type=SPOILER`

## 설명

사용자가 나중에 보기 보관함에 저장한 차단 콘텐츠 목록을 관심사별로 조회한다. 전체 조회는 제공하지 않으며 `interestTargetId` query string이 필수다. 페이지네이션과 유형 필터를 지원한다.

## REQUEST

```json
{}
```

### Query String

| 필드 | 필수 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `interestTargetId` | Yes | - | 조회할 관심 대상 ID |
| `page` | No | `1` | 페이지 번호 |
| `size` | No | `20` | 페이지 크기 |
| `type` | No | - | 차단 유형 필터. 예: `SPOILER`, `HARMFUL`, `INTEREST` |

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "blockedItemId": "blocked_item_1",
        "interestTargetId": "interest_target_1",
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
| `INVALID_REQUEST_BODY` | 422 | `interestTargetId` 누락 또는 요청 형식 오류 |
| `INTEREST_TARGET_NOT_FOUND` | 404 | 관심 대상을 찾을 수 없음 |
