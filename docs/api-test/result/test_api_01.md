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
- 실패 및 수정이 필요한 API: `POST /api/auth/signup`, `POST /api/auth/login`, `GET /api/auth/me`, `POST /api/auth/refresh`, `POST /api/auth/logout`, `DELETE /api/auth/me`, `GET /api/interests/types`, `GET /api/interests/genres`, `GET /api/interests`, `POST /api/interests/select`, `POST /api/interests/targets`, `GET /api/interest-targets`, `GET /api/interest-targets/titles`, `PUT /api/interest-targets`, `GET /api/block-settings`, `PUT /api/block-settings`, `POST /api/analyses`, `POST /api/blocked-items`, `GET /api/blocked-items`, `GET /api/interest-items`, `GET /api/interest-items/urls`, `POST /api/interest-items`, `GET /api/interest-items/{interestItemId}`, `DELETE /api/blocked-items/{blockedItemId}`

### 1. 실패 API

- `POST /api/auth/signup`
  - HTTP Status: `502 Bad Gateway`
- `POST /api/auth/login`
  - HTTP Status: `502 Bad Gateway`
- `GET /api/auth/me`
  - HTTP Status: `502 Bad Gateway`
- `POST /api/auth/refresh`
  - HTTP Status: `502 Bad Gateway`
- `POST /api/auth/logout`
  - HTTP Status: `502 Bad Gateway`
- `DELETE /api/auth/me`
  - HTTP Status: `502 Bad Gateway`
- `GET /api/interests/types`
  - HTTP Status: `502 Bad Gateway`
- `GET /api/interests/genres`
  - HTTP Status: `502 Bad Gateway`
- `GET /api/interests`
  - HTTP Status: `502 Bad Gateway`
- `POST /api/interests/select`
  - 테스트 제외: 배포 DB 관심사 카탈로그 데이터 확인 실패
- `POST /api/interests/targets`
  - HTTP Status: `502 Bad Gateway`
- `GET /api/interest-targets`
  - HTTP Status: `502 Bad Gateway`
- `GET /api/interest-targets/titles`
  - HTTP Status: `502 Bad Gateway`
- `PUT /api/interest-targets`
  - 테스트 제외: 배포 DB 관심사 카탈로그 데이터 확인 실패
- `GET /api/block-settings`
  - HTTP Status: `502 Bad Gateway`
- `PUT /api/block-settings`
  - HTTP Status: `502 Bad Gateway`
- `POST /api/analyses`
  - HTTP Status: `502 Bad Gateway`
- `POST /api/blocked-items`
  - 테스트 제외: `interestTargetId` 없음
- `GET /api/blocked-items`
  - 테스트 제외: `interestTargetId` 없음
- `GET /api/interest-items`
  - HTTP Status: `502 Bad Gateway`
- `GET /api/interest-items/urls`
  - HTTP Status: `502 Bad Gateway`
- `POST /api/interest-items`
  - HTTP Status: read timeout
- `GET /api/interest-items/{interestItemId}`
  - 테스트 제외: `interestItemId` 없음
- `DELETE /api/blocked-items/{blockedItemId}`
  - 테스트 제외: `blockedItemId` 없음

### 2. 실패 원인

- 배포 서버 전체가 `nginx/1.27.5` 기준 `502 Bad Gateway`를 반환했다.
- 개별 API 로직보다 배포 인프라/업스트림 장애를 먼저 확인해야 한다.

