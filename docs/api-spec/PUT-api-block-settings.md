# 차단 설정 수정 API

`PUT /api/block-settings`

## 설명

스포일러, 유해정보, 관심정보 유형별 차단 여부와 민감도를 일괄 수정한다. 기존 설정은 요청 값으로 대체된다.

## REQUEST

```json
{
  "spoiler": {
    "enabled": true,
    "sensitivity": "HIGH"
  },
  "harmful": {
    "enabled": true,
    "sensitivity": "MEDIUM"
  },
  "interest": {
    "enabled": true,
    "sensitivity": "LOW"
  }
}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "updatedAt": "2026-07-13T05:00:00Z"
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `BLOCK_SETTING_INVALID_SENSITIVITY` | 400 | 지원하지 않는 민감도 |
