> **이 엔드포인트는 제거되었습니다.**
> 사용자 주도 병합 흐름이 기획에서 제외되어 API를 제거했습니다.

# 중복 그룹 출처 추가 API (Deprecated)

`POST /api/interest-item-groups/{interestItemGroupId}/sources`

## 설명

기존 관심 정보 그룹에 새로운 출처 항목을 추가한다. 같은 이슈나 공지로 판단되는 관심 정보를 하나의 그룹으로 통합할 때 사용한다.

## REQUEST

```json
{
  "interestItemId": "interest_item_1",
  "duplicateScore": 0.92,
  "duplicateReason": "동일한 이슈로 판단됩니다."
}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "interestItemGroupId": "interest_item_group_1",
    "sourceCount": 4,
    "updatedAt": "2026-07-13T05:00:00Z"
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INTEREST_ITEM_GROUP_NOT_FOUND` | 404 | 중복 그룹을 찾을 수 없음 |
| `INTEREST_ITEM_NOT_FOUND` | 404 | 관심 정보를 찾을 수 없음 |
| `INTEREST_ITEM_ALREADY_GROUPED` | 409 | 이미 해당 그룹에 포함된 관심 정보 |
