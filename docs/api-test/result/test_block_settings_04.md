- 파일 명 규칙: test_domain_nn.md
- 자원 별로 나누어서 파일을 작성하도록 한다.
- 예시) test_auth_01.md

---
## API 테스트 결과

> API 테스트 요청 시

### 요약

- 테스트 대상 host: `https://blanker-api.duckdns.org/`
- 테스트 계정: `api-test-1784039465@example.com`
- 정상 작동하는 API: 없음
- 실패 및 수정이 필요한 API: `GET /api/block-settings`, `PUT /api/block-settings`

### 1. 실패 API

- 전부 `502 Bad Gateway`

