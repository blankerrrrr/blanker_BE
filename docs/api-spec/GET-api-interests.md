# 관심사 목록 조회 API

`GET /api/interests`

## 설명

온보딩에서 사용자가 선택할 수 있는 DB 저장 관심사 목록을 조회한다. 여기서 관심사는 서버가 제공하는 카탈로그 데이터이며, 사용자가 선택하면 개인 관심사로 저장된다.

## REQUEST

```json
{}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "interestId": "interest_1",
        "title": "작품명",
        "genre": "애니메이션",
        "imageUrl": "https://example.com/image.jpg",
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
