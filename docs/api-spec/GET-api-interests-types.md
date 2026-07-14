# 관심사 종류 목록 조회 API

`GET /api/interests/types`

## 설명

온보딩 관심사 목록 조회에 사용할 수 있는 관심사 종류 목록을 조회한다. 각 종류는 이름과 대표 이미지 URL을 제공한다.

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
        "name": "애니메이션",
        "imageUrl": "https://example.com/anime.jpg"
      }
    ]
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
