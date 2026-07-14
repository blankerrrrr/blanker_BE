# 관심사 장르 목록 조회 API

`GET /api/interests/genres?interestType=게임`

## 설명

관심사 종류별로 저장된 장르 목록을 조회한다. 장르는 `interest_genres` 테이블과 `interest_genre_mappings` 매핑 테이블 기준으로 조회한다.

## REQUEST

### Header

| Header | 필수 | 설명 |
| --- | --- | --- |
| `Authorization` | Yes | `Bearer {accessToken}` |

### Query String

| 이름 | 필수 | 설명 |
| --- | --- | --- |
| `interestType` | Yes | 관심사 종류. 예: `게임`, `영화`, `소설` |

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "name": "Action"
      },
      {
        "name": "Adventure"
      }
    ]
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 없음 또는 유효하지 않음 |
| `INVALID_REQUEST_BODY` | 422 | 필수 query string 누락 또는 요청 형식 오류 |
