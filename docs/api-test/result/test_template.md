- 파일 명 규칙: test_domain_nn.md 
- 자원 별로 나누어서 파일을 작성하도록 한다.
- 예시) test_auth_01.md
- 절대 test_all_00.md나 test_api_00.md로 한꺼번에 작성하지 않는다. 어길 시 결제 끊음

---
## API 테스트 결과

> API 테스트 요청 시

### 요약

- 정상 작동하는 API: `/auth/login`
- 실패 및 수정이 필요한 API: `/auth/signup`

### 1. /auth/login

- API 정상 작동
- 그러나 없는 계정에 대한 실패 시 404 반환, 401로 변경 필요

### 2. /auth/signup

- 정상 작동 안함: 500 Internal Server Error
- auth/service/SignupService.kt의 56번째 줄이 원인으로 보임
