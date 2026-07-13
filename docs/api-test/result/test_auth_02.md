## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/auth/signup`, `/api/auth/login`, `/api/auth/me`
- 실패 및 수정이 필요한 API: 없음

### 1. /api/auth/signup

- API 정상 작동
- 응답: 201 Created
- 확인 내용: 이메일, 비밀번호, 약관 동의 값으로 신규 사용자 생성

### 2. /api/auth/login

- API 정상 작동
- 응답: 200 OK
- 확인 내용: access token 반환 및 refreshToken Cookie 설정

### 3. /api/auth/me

- API 정상 작동
- 응답: 200 OK
- 확인 내용: `Authorization: Bearer {accessToken}`으로 현재 사용자 조회

### 참고

- 기존 실패 원인인 Redis `HELLO` 오류는 Redis client protocol을 RESP2로 고정한 뒤 해결됨
