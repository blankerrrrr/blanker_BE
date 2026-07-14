# 회원탈퇴 API

`DELETE /api/auth/me`

## 설명

현재 로그인한 사용자의 계정을 탈퇴 처리한다. 모든 리프레시 토큰을 비활성화하고 유저 데이터를 하드 삭제한다.

## REQUEST

### Header

| Header | 필수 | 설명 |
| --- | --- | --- |
| `Authorization` | Yes | `Bearer {accessToken}` |

## RESPONSE `200`

```json
{
  "success": true,
  "data": null
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 없음 또는 유효하지 않음 |
| `USER_NOT_FOUND` | 404 | 사용자를 찾을 수 없음 |
