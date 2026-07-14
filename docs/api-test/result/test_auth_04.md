## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/auth/signup`, `/api/auth/login`, `/api/auth/me`, `/api/auth/refresh`, `/api/auth/logout`, `/api/auth/me` 탈퇴
- 실패 및 수정이 필요한 API: 없음

### 1. POST /api/auth/signup

- API 정상 작동
- 응답: 201 Created
- 확인 내용: 신규 사용자 생성

### 2. POST /api/auth/login

- API 정상 작동
- 응답: 200 OK
- 확인 내용: access token 반환 및 `refreshToken` Set-Cookie 반환

### 3. GET /api/auth/me

- API 정상 작동
- 응답: 200 OK
- 확인 내용: `Authorization: Bearer {accessToken}`으로 현재 사용자 조회

### 4. POST /api/auth/refresh

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 로그인 응답의 `refreshToken` Cookie를 직접 전송해 새 access token 발급 확인
- 참고: 로컬 HTTP 환경에서는 `Secure` Cookie가 자동 전송되지 않아 자동 쿠키 세션 요청은 `AUTH_REFRESH_TOKEN_COOKIE_MISSING` 반환

### 5. POST /api/auth/logout

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 인증된 사용자 로그아웃 성공

### 6. DELETE /api/auth/me

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 탈퇴용 계정 생성 후 회원탈퇴 성공
