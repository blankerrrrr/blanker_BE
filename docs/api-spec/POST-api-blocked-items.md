# 보관함 저장 API

`POST /api/blocked-items`

## 설명

차단된 콘텐츠를 나중에 보기 보관함에 저장한다. 원본 링크, 페이지 내 위치, 차단 유형, 관련 주제를 함께 기록한다.

## REQUEST

```json
{
  "analysisRequestId": "analysis_request_1",
  "clientContentId": "node_001",
  "interestTargetId": "interest_target_1",
  "summary": "차단된 콘텐츠 요약",
  "categories": ["SPOILER"],
  "relatedTopics": ["작품명"],
  "sourceUrl": "https://example.com/article",
  "selector": "article > p:nth-child(1)",
  "positionText": "본문 첫 번째 문단"
}
```

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `analysisRequestId` | string | No | 저장 근거가 된 분석 요청 ID |
| `clientContentId` | string | No | 분석 요청 내 콘텐츠 ID |
| `interestTargetId` | string | Yes | 보관함 항목이 연결될 관심 대상 ID |
| `summary` | string | Yes | 차단된 콘텐츠 요약 |
| `categories` | string[] | Yes | 차단 유형 목록 |
| `relatedTopics` | string[] | No | 관련 주제 |
| `sourceUrl` | string | Yes | 원본 링크 |
| `selector` | string | No | 페이지 내 위치 |
| `positionText` | string | No | 사람이 이해 가능한 위치 설명 |

## RESPONSE `201`

```json
{
  "success": true,
  "data": {
    "blockedItemId": "blocked_item_1",
    "savedAt": "2026-07-13T05:00:00Z"
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INTEREST_TARGET_NOT_FOUND` | 404 | 관심 대상을 찾을 수 없음 |
| `BLOCKED_ITEM_ALREADY_EXISTS` | 409 | 이미 저장된 보관함 항목 |
