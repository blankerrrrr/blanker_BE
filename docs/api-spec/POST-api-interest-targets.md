# 관심 대상 생성 API

`POST /api/interest-targets`

## 설명

새 관심 대상을 등록한다. 관심 대상은 작품, 인물, 주제로 구분되며 별칭과 키워드를 함께 저장할 수 있다.

## REQUEST

```json
{
  "type": "WORK",
  "name": "작품명",
  "aliases": ["별칭"],
  "keywords": ["주요 키워드"]
}
```

## RESPONSE `201`

```json
{
  "success": true,
  "data": {
    "interestTargetId": "interest_target_1",
    "type": "WORK",
    "name": "작품명",
    "aliases": ["별칭"],
    "keywords": ["주요 키워드"],
    "createdAt": "2026-07-13T05:00:00Z"
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INTEREST_TARGET_INVALID_TYPE` | 400 | 지원하지 않는 관심 대상 유형 |
| `INTEREST_TARGET_ALREADY_EXISTS` | 409 | 이미 등록된 관심 대상 |
