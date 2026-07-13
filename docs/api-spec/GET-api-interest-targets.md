# 관심 대상 목록 조회 API

`GET /api/interest-targets`

## 설명

현재 사용자가 등록한 관심 작품, 인물, 주제 목록을 조회한다. 콘텐츠 분석과 관련도 판단의 기준 데이터를 제공한다.

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
        "interestTargetId": "target_01HZX...",
        "type": "WORK",
        "name": "작품명",
        "aliases": ["별칭"],
        "keywords": ["주요 키워드"],
        "createdAt": "2026-07-13T05:00:00Z"
      }
    ]
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
