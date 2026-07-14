# 보관함 목록 조회 API

`GET /api/blocked-items?interestType=애니메이션&type=SPOILER`

## 설명

사용자가 나중에 보기 보관함에 저장한 차단 콘텐츠 목록을 관심 대상 제목별로 조회한다. `interestType`을 전달하면 해당 관심사 분류에 속한 항목만 조회한다. 필터를 전달하지 않으면 사용자의 모든 관심 대상을 반환하며, 보관함 항목이 없는 관심 대상도 빈 배열로 포함한다.

## REQUEST

```json
{}
```

### Query String

| 필드 | 필수 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `interestTargetId` | No | - | 조회할 관심 대상 ID |
| `interestType` | No | - | `interest_catalog.name` 기준 관심사 분류 필터 |
| `type` | No | - | 차단 유형 필터. 예: `SPOILER`, `HARMFUL`, `INTEREST` |

## RESPONSE `200`

```json
{
  "success": true,
  "data": [
    {
      "귀멸의 칼날": [
        {
          "blockedItemId": "blocked_item_1",
          "interestTargetId": "interest_target_1",
          "summary": "최종국면 극장판 핵심 반전 및 사망 캐릭터 스포일러",
          "categories": ["SPOILER"],
          "relatedTopics": ["귀멸의 칼날", "극장판"],
          "sourceUrl": "https://example.com/article/demon-slayer-spoiler",
          "foundAt": "2026-07-13T05:00:00Z"
        },
        {
          "blockedItemId": "blocked_item_2",
          "interestTargetId": "interest_target_1",
          "summary": "원작 만화 결말 유출 관련 커뮤니티 글",
          "categories": ["SPOILER"],
          "relatedTopics": ["귀멸의 칼날", "결말"],
          "sourceUrl": "https://example.com/article/demon-slayer-ending",
          "foundAt": "2026-07-14T02:30:00Z"
        }
      ]
    },
    {
      "진격의 거인": []
    }
  ]
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INVALID_REQUEST_BODY` | 422 | 요청 형식 오류 |
| `INTEREST_TARGET_NOT_FOUND` | 404 | 관심 대상을 찾을 수 없음 |
