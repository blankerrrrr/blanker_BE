- 파일 명 규칙: test_domain_nn.md
- 자원 별로 나누어서 파일을 작성하도록 한다.
- 예시) test_auth_01.md
- 절대 test_all_00.md나 test_api_00.md로 한꺼번에 작성하지 않는다. 어길 시 결제 끊음

---
## API 테스트 결과

> API 테스트 요청 시

### 요약

- 환경: 로컬 서버 `http://127.0.0.1:8000`
- 정상 작동하는 API: `/api/interest-targets`, `/api/interest-targets/titles`
- 실패 및 수정이 필요한 API: 없음

### 1. GET /api/interest-targets

- 상태 코드: 200
- API 정상 작동

### 2. GET /api/interest-targets/titles

- 상태 코드: 200
- API 정상 작동

### 3. PUT /api/interest-targets

- 상태 코드: 200
- API 정상 작동
