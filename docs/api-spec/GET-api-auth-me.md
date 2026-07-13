# 내 계정 조회 API

`GET /api/auth/me`

## 설명

현재 인증된 사용자의 계정 정보를 조회한다. 클라이언트가 로그인 상태를 확인하거나 계정 설정 화면을 구성할 때 사용한다.

## REQUEST

```json
{}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "userId": "user_01HZX...",
    "email": "user@example.com",
    "createdAt": "2026-07-13T05:00:00Z"
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `USER_NOT_FOUND` | 404 | 사용자를 찾을 수 없음 |
