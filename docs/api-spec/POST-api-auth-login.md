# 로그인 API

`POST /api/auth/login`

## 설명

사용자 이메일과 비밀번호를 검증해 access token을 발급한다. refresh token은 응답 본문에 포함하지 않고 HttpOnly Secure Cookie로 설정한다.

## REQUEST

```json
{
  "email": "user@example.com",
  "password": "password123!"
}
```

## RESPONSE `200`

Header:

```http
Set-Cookie: refreshToken={refresh-token}; HttpOnly; Secure; SameSite=Lax; Path=/api/auth; Max-Age=1209600
```

```json
{
  "success": true,
  "data": {
    "accessToken": "access-token",
    "tokenType": "Bearer",
    "expiresIn": 3600,
    "user": {
      "userId": "user_1",
      "email": "user@example.com"
    }
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_INVALID_CREDENTIALS` | 401 | 이메일 또는 비밀번호 불일치 |
| `AUTH_ACCOUNT_DISABLED` | 403 | 비활성화된 계정 |
