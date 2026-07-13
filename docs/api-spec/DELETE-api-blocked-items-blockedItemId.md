# 보관함 항목 삭제 API

`DELETE /api/blocked-items/{blockedItemId}`

## 설명

보관함에 저장된 차단 콘텐츠를 삭제한다. 삭제 대상은 현재 인증된 사용자의 항목이어야 한다.

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
| `BLOCKED_ITEM_NOT_FOUND` | 404 | 보관함 항목을 찾을 수 없음 |
