# 토큰 재발급 API

`POST /api/auth/refresh`

## 설명

Cookie로 전달된 refresh token을 검증해 새로운 access token을 발급한다. refresh token rotation을 적용하며 새 refresh token은 다시 Cookie로 설정한다.

## REQUEST

```json
{}
```

요청 시 `refreshToken` Cookie를 함께 전송한다.

## RESPONSE `200`

Header:

```http
Set-Cookie: refreshToken={new-refresh-token}; HttpOnly; Secure; SameSite=Lax; Path=/api/auth; Max-Age=1209600
```

```json
{
  "success": true,
  "data": {
    "accessToken": "new-access-token",
    "tokenType": "Bearer",
    "expiresIn": 3600
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_REFRESH_TOKEN_COOKIE_MISSING` | 401 | refresh token Cookie 누락 |
| `AUTH_INVALID_REFRESH_TOKEN` | 401 | 유효하지 않은 refresh token |
| `AUTH_REFRESH_TOKEN_EXPIRED` | 401 | 만료된 refresh token |
