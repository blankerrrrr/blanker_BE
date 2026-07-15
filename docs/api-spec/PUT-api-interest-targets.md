# 관심사 선택 동기화 API

`PUT /api/interest-targets`

## 설명

사용자의 카탈로그 관심사 선택 목록을 동기화한다. 요청에 포함된 관심사는 추가되고, 기존에 선택되었으나 포함되지 않은 관심사는 제거된다.

관심 대상이 제거되어도 해당 관심 대상에 연결된 보관함 항목은 삭제되지 않으며, `interestTargetId`만 `NULL`로 변경된다.

## REQUEST

### Header

| Header | 필수 | 설명 |
| --- | --- | --- |
| `Authorization` | Yes | `Bearer {accessToken}` |

### Body

```json
{
  "interestIds": ["interest_1", "interest_2"]
}
```

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `interestIds` | string[] | Yes | 선택할 관심사 ID 목록 (최소 1개) |

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
| `INTEREST_NOT_FOUND` | 404 | 요청한 관심사 ID가 존재하지 않음 |
