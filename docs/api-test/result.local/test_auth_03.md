- 파일 명 규칙: test_domain_nn.md
- 자원 별로 나누어서 파일을 작성하도록 한다.
- 예시) test_auth_01.md
- 절대 test_all_00.md나 test_api_00.md로 한꺼번에 작성하지 않는다. 어길 시 결제 끊음

---
## API 테스트 결과

> API 테스트 요청 시

### 요약

- 환경: 배포 서버 `https://blanker-api.duckdns.org`
- 정상 작동하는 API: `/api/auth/signup`, `/api/auth/login`, `/api/auth/me`, `/api/auth/refresh`, `/api/auth/logout`, `DELETE /api/auth/me`
- 실패 및 수정이 필요한 API: 없음

### 1. POST /api/auth/signup

- 상태 코드: 201
- API 정상 작동

### 2. POST /api/auth/login

- 상태 코드: 200
- API 정상 작동

### 3. GET /api/auth/me

- 상태 코드: 200
- API 정상 작동

### 4. POST /api/auth/refresh

- 상태 코드: 200
- refreshToken 쿠키 기반 재발급 정상 작동

### 5. POST /api/auth/logout

- 상태 코드: 200
- API 정상 작동

### 6. DELETE /api/auth/me

- 상태 코드: 200
- 테스트 계정 탈퇴 정상 작동
