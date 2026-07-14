## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/auth/signup`, `/api/auth/login`, `/api/auth/me`, `/api/auth/logout`
- 실패 및 수정이 필요한 API: 없음

### 1. POST /api/auth/signup

- API 정상 작동
- 응답: 201 Created
- 확인 내용: 신규 사용자 생성 확인

### 2. POST /api/auth/login

- API 정상 작동
- 응답: 200 OK
- 확인 내용: access token 반환 확인

### 3. GET /api/auth/me

- API 정상 작동
- 응답: 200 OK
- 확인 내용: `Authorization: Bearer {accessToken}`으로 현재 사용자 조회

### 4. POST /api/auth/logout

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 인증된 사용자의 로그아웃 요청 성공
