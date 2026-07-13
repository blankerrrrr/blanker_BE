# 관심 대상 수정 API

`PATCH /api/interest-targets/{interestTargetId}`

## 설명

등록된 관심 대상의 이름, 별칭, 키워드를 수정한다. 수정된 정보는 이후 콘텐츠 분석과 관련도 판단에 반영된다.

## REQUEST

```json
{
  "name": "수정된 작품명",
  "aliases": ["새 별칭"],
  "keywords": ["수정 키워드"]
}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "interestTargetId": "interest_target_1",
    "type": "WORK",
    "name": "수정된 작품명",
    "aliases": ["새 별칭"],
    "keywords": ["수정 키워드"],
    "updatedAt": "2026-07-13T05:10:00Z"
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INTEREST_TARGET_NOT_FOUND` | 404 | 관심 대상을 찾을 수 없음 |
