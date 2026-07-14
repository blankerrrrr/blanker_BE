# 관심 대상 생성 API

`POST /api/interest-targets`

## 설명

새 개인 관심사를 등록한다. 클라이언트는 사용자가 입력한 제목만 전달하고, 서버는 제목을 기준으로 웹 검색 또는 AI 보강을 수행해 관심 대상 유형, 별칭, 키워드를 결정한 뒤 저장한다.

MVP에서는 제목 기반 보강 결과가 부족하면 `WORK` 타입과 빈 별칭, 제목 기반 키워드로 저장할 수 있다.

## REQUEST

```json
{
  "name": "작품명"
}
```

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `name` | string | Yes | 사용자가 검색하거나 직접 입력한 관심사 제목 |

## RESPONSE `201`

```json
{
  "success": true,
  "data": {
    "interestTargetId": "interest_target_1",
    "type": "WORK",
    "name": "작품명",
    "aliases": ["검색 또는 AI가 보강한 별칭"],
    "keywords": ["검색 또는 AI가 보강한 키워드"],
    "createdAt": "2026-07-13T05:00:00Z"
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INVALID_REQUEST_BODY` | 422 | 제목 누락 또는 요청 형식 오류 |
| `INTEREST_TARGET_ALREADY_EXISTS` | 409 | 이미 등록된 관심 대상 |
