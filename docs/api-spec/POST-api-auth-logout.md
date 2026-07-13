# 로그아웃 API

`POST /api/auth/logout`

## 설명

현재 세션의 refresh token을 폐기하고 refresh token Cookie를 만료시킨다. 서버에서는 Redis에 저장된 refresh token hash를 삭제한다.

## REQUEST

```json
{}
```

요청 시 `refreshToken` Cookie를 함께 전송한다.

## RESPONSE `200`

Header:

```http
Set-Cookie: refreshToken=; HttpOnly; Secure; SameSite=Lax; Path=/api/auth; Max-Age=0
```

```json
{
  "success": true,
  "data": null
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
