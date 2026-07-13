# 차단 설정 조회 API

`GET /api/block-settings`

## 설명

사용자의 정보 유형별 차단 활성화 여부와 민감도 설정을 조회한다. 확장 프로그램이 콘텐츠 분석 또는 차단 판단 전 설정을 동기화할 때 사용한다.

## REQUEST

```json
{}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
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
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
