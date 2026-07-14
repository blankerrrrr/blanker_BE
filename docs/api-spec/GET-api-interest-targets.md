# 선택한 관심사 목록 조회 API

`GET /api/interest-targets`

## 설명

현재 사용자가 선택한 카탈로그 관심사 목록을 조회한다. `PUT /api/interest-targets`로 선택된 항목만 포함된다.

## REQUEST

### Header

| Header | 필수 | 설명 |
| --- | --- | --- |
| `Authorization` | Yes | `Bearer {accessToken}` |

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "interestTargetId": "interest_target_1",
        "interestId": "interest_1",
        "interestType": "애니메이션",
        "interestTypeImageUrl": "https://example.com/type.jpg",
        "title": "작품명",
        "genre": "액션",
        "summary": "작품 설명",
        "imageUrl": "https://example.com/image.jpg",
        "createdAt": "2026-07-14T05:00:00Z"
      }
    ]
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
