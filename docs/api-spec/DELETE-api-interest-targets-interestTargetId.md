# 관심 대상 삭제 API

`DELETE /api/interest-targets/{interestTargetId}`

## 설명

등록된 관심 대상을 삭제한다. 삭제 후 해당 관심 대상은 신규 콘텐츠 분석 기준에서 제외된다.

## REQUEST

```json
{}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": null
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INTEREST_TARGET_NOT_FOUND` | 404 | 관심 대상을 찾을 수 없음 |
