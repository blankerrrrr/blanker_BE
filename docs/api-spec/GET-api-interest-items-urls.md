# 관심 정보 URL 목록 조회 API

`GET /api/interest-items/urls`

## 설명

수집한 관심 정보의 원본 URL 목록을 조회한다. 현재 사용자가 저장한 관심 정보만 발견일별로 묶어 최신 발견순으로 반환한다.

## REQUEST

```json
{}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": [
    {
      "2026-07-14": [
        {
          "interestItemId": "interest_item_1",
          "sourceUrl": "https://example.com/article",
          "discoveredAt": "2026-07-14T01:02:03Z"
        }
      ]
    },
    {
      "2026-07-15": []
    }
  ]
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
