# 회원가입 API

`POST /api/auth/signup`

## 설명

이메일과 비밀번호로 신규 사용자 계정을 생성한다. 회원가입 시 필수 약관 동의와 개인정보 처리 동의 여부를 함께 검증한다.

## REQUEST

```json
{
  "email": "user@example.com",
  "password": "password123!",
  "termsAgreed": true,
  "privacyAgreed": true
}
```

## RESPONSE `201`

```json
{
  "success": true,
  "data": {
    "userId": "user_01HZX...",
    "email": "user@example.com",
    "createdAt": "2026-07-13T05:00:00Z"
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_EMAIL_ALREADY_EXISTS` | 409 | 이미 가입된 이메일 |
| `AUTH_WEAK_PASSWORD` | 400 | 비밀번호 정책 미충족 |
| `AUTH_REQUIRED_AGREEMENT_MISSING` | 400 | 필수 약관 미동의 |
