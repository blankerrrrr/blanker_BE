- 파일 명 규칙: test_domain_nn.md
- 자원 별로 나누어서 파일을 작성하도록 한다.
- 예시) test_auth_01.md
- 절대 test_all_00.md나 test_api_00.md로 한꺼번에 작성하지 않는다. 어길 시 결제 끊음

---
## API 테스트 결과

> API 테스트 요청 시

### 요약

- 환경: 배포 서버 `https://blanker-api.duckdns.org`
- 정상 작동하는 API: `/api/interests/types`, `/api/interests/genres`, `/api/interests`, `/api/interests/select`, `/api/interests/targets`
- 실패 및 수정이 필요한 API: 없음

### 1. GET /api/interests/types

- 상태 코드: 200
- API 정상 작동

### 2. GET /api/interests/genres?interestType=게임

- 상태 코드: 200
- API 정상 작동

### 3. GET /api/interests?interestType=영화

- 상태 코드: 200
- API 정상 작동

### 4. POST /api/interests/select

- 상태 코드: 200
- API 정상 작동

### 5. POST /api/interests/targets

- 상태 코드: 201
- API 정상 작동
