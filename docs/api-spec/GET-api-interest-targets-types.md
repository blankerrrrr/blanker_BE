# 개인 관심사 분류 목록 조회 API

`GET /api/interest-targets/types`

## 설명

현재 사용자가 선택한 관심사가 속한 관심사 분류 목록을 조회한다. 사용자가 선택하지 않은 관심사의 분류는 반환하지 않으며, 분류는 `interest_catalog.id` 오름차순으로 정렬한다.

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "name": "애니메이션"
      }
    ]
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
