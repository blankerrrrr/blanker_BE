- 파일 명 규칙: test_domain_nn.md
- 자원 별로 나누어서 파일을 작성하도록 한다.
- 예시) test_auth_01.md
- 절대 test_all_00.md나 test_api_00.md로 한꺼번에 작성하지 않는다. 어길 시 결제 끊음

---
## API 테스트 결과

> API 테스트 요청 시

### 요약

- 환경: 배포 서버 `https://blanker-api.duckdns.org`
- 정상 작동하는 API: `/api/blocked-items`, `/api/blocked-items/{blockedItemId}`
- 실패 및 수정이 필요한 API: 없음

### 1. GET /api/blocked-items

- 상태 코드: 200
- `interestTargetId`, `page`, `size`, `type` 쿼리 조건 정상 작동

### 2. POST /api/blocked-items

- 상태 코드: 201
- API 정상 작동

### 3. DELETE /api/blocked-items/{blockedItemId}

- 상태 코드: 200
- API 정상 작동
