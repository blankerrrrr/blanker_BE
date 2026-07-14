# 관심사 목록 조회 API

`GET /api/interests`

## 설명

온보딩에서 사용자가 선택할 수 있는 DB 저장 관심사 목록을 조회한다. 여기서 관심사는 서버가 제공하는 카탈로그 데이터이며, 사용자가 선택하면 개인 관심사로 저장된다.

관심사 종류는 필수이며, 장르는 기본값 `전체`를 사용한다. 검색어가 있으면 장르와 관계없이 해당 관심사 종류 안에서 제목을 검색한다.

## REQUEST

| Query String | 필수 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `interestType` | Yes | - | 관심사 종류. 예: `영화`, `드라마`, `애니메이션`, `소설`, `게임`, `웹툰`, `뮤지컬`, `기타` |
| `genre` | No | `전체` | 장르 필터. `전체`이면 장르 필터를 적용하지 않음 |
| `keyword` | No | - | 제목 검색어. 입력 시 장르와 관계없이 관심사 종류 안에서 검색 |

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "interestId": "interest_1",
        "interestType": "애니메이션",
        "interestTypeImageUrl": "https://example.com/type.jpg",
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
| `INVALID_REQUEST_BODY` | 422 | 필수 query string 누락 또는 요청 형식 오류 |
