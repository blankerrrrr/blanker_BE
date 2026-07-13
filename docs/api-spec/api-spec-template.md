# {제목} API
# 회원탈퇴 API

> 파일명은 `METHOD-endpoint.md`

`DELETE /api/accounts/me`

## REQUEST

```json
{}
```

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
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `USER_NOT_FOUND` | 404 | 사용자를 찾을 수 없음 |
| `ACCOUNT_DELETE_NOT_ALLOWED` | 409 | 제출된 원서가 있어 회원탈퇴 불가 |
