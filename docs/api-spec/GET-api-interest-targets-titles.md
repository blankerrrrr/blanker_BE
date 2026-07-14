# 관심사 제목 목록 조회 API

`GET /api/interest-targets/titles`

## 설명

현재 사용자의 관심 대상 ID와 제목만 조회한다. 보관함 조회 API의 `interestTargetId` query string 선택지를 제공하기 위한 API다.

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
        "title": "작품명"
      }
    ]
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
