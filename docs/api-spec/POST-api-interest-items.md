# 관심 정보 수집 저장 API

`POST /api/interest-items`

## 설명

확장 프로그램 또는 분석 서버가 감지한 관심 주제 관련 정보를 저장한다. 같은 출처 URL이 이미 존재하면 중복으로 처리한다.

## REQUEST

```json
{
  "title": "관심 정보 제목",
  "summary": "관심 정보 요약",
  "contentText": "수집된 원문 또는 핵심 본문",
  "relatedTopics": ["작품명"],
  "sourceUrl": "https://example.com/article",
  "selector": "article"
}
```

## RESPONSE `201`

```json
{
  "success": true,
  "data": {
    "interestItemId": "interest_item_1",
    "duplicate": false,
    "savedAt": "2026-07-13T05:00:00Z"
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INTEREST_ITEM_NOT_RELEVANT` | 400 | 등록된 관심 대상과 관련성이 낮음 |
