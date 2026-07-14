# 관심사 선택 API

`POST /api/interests/select`

## 설명

온보딩에서 선택한 관심사를 현재 사용자의 개인 관심사로 저장한다. 이미 같은 제목의 개인 관심사가 있으면 새로 만들지 않고 기존 개인 관심사를 응답한다.

## REQUEST

```json
{
  "interestIds": ["interest_1", "interest_2"]
}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "interestTargetId": "interest_target_1",
        "type": "WORK",
        "name": "작품명",
        "aliases": [],
        "keywords": ["애니메이션"],
        "createdAt": "2026-07-14T05:00:00Z",
        "updatedAt": "2026-07-14T05:00:00Z"
      }
    ]
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INTEREST_NOT_FOUND` | 404 | 요청한 관심사를 찾을 수 없음 |
