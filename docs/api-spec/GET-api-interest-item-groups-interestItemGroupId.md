# 중복 그룹 상세 조회 API

`GET /api/interest-item-groups/{interestItemGroupId}`

## 설명

중복 통합된 관심 정보 그룹의 상세 내용을 조회한다. 대표 콘텐츠와 그룹에 포함된 추가 출처 목록을 함께 제공한다.

## REQUEST

```json
{}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "interestItemGroupId": "interest_item_group_1",
    "representative": {
      "interestItemId": "interest_item_1",
      "title": "대표 관심 정보 제목",
      "summary": "대표 요약"
    },
    "sources": [
      {
        "interestItemId": "interest_item_1",
        "sourceUrl": "https://example.com/article",
        "discoveredAt": "2026-07-13T05:00:00Z"
      }
    ],
    "duplicateReason": "제목과 핵심 문장이 유사합니다."
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INTEREST_ITEM_GROUP_NOT_FOUND` | 404 | 중복 그룹을 찾을 수 없음 |
