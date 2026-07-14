- 파일 명 규칙: test_domain_nn.md
- 자원 별로 나누어서 파일을 작성하도록 한다.
- 예시) test_auth_01.md

---
## API 테스트 결과

> API 테스트 요청 시

### 요약

- 테스트 대상 host: `http://127.0.0.1:8000`
- 테스트 계정: `api-test-1784039344@example.com`
- 정상 작동하는 API: `POST /api/auth/signup`, `POST /api/auth/login`, `GET /api/auth/me`, `POST /api/auth/refresh`, `POST /api/auth/logout`, `DELETE /api/auth/me`, `GET /api/interests/types`, `GET /api/interests/genres`, `GET /api/interests`, `POST /api/interests/targets`, `GET /api/interest-targets`, `GET /api/interest-targets/titles`, `PUT /api/block-settings`, `GET /api/block-settings`, `POST /api/analyses`, `POST /api/blocked-items`, `GET /api/blocked-items`, `GET /api/interest-items`, `GET /api/interest-items/urls`, `POST /api/interest-items`, `GET /api/interest-items/{interestItemId}`, `DELETE /api/blocked-items/{blockedItemId}`
- 실패 및 수정이 필요한 API: `POST /api/interests/select`, `PUT /api/interest-targets`

### 1. 성공 API

- `POST /api/auth/signup`
  - 응답: `201 Created`
  - 확인 내용: 신규 사용자 생성 성공
- `POST /api/auth/login`
  - 응답: `200 OK`
  - 확인 내용: access token 발급, `refreshToken` Cookie 발급
- `GET /api/auth/me`
  - 응답: `200 OK`
  - 확인 내용: 인증된 사용자 조회 성공
- `POST /api/auth/refresh`
  - 응답: `200 OK`
  - 확인 내용: `refreshToken` Cookie로 access token 재발급 성공
- `POST /api/auth/logout`
  - 응답: `200 OK`
  - 확인 내용: 로그아웃 성공
- `DELETE /api/auth/me`
  - 응답: `200 OK`
  - 확인 내용: 회원탈퇴 성공
- `GET /api/interests/types`
  - 응답: `200 OK`
  - 확인 내용: 관심사 종류 목록 조회 성공
- `GET /api/interests/genres`
  - 응답: `200 OK`
  - 확인 내용: 관심사 장르 목록 조회 성공
- `GET /api/interests`
  - 응답: `200 OK`
  - 확인 내용: 관심사 목록 조회 성공
- `POST /api/interests/targets`
  - 응답: `201 Created`
  - 확인 내용: 관심사 직접 등록 성공
- `GET /api/interest-targets`
  - 응답: `200 OK`
  - 확인 내용: 선택한 관심사 목록 조회 성공
- `GET /api/interest-targets/titles`
  - 응답: `200 OK`
  - 확인 내용: 관심사 제목 목록 조회 성공
- `GET /api/block-settings`
  - 응답: `200 OK`
  - 확인 내용: 차단 설정 조회 성공
- `PUT /api/block-settings`
  - 응답: `200 OK`
  - 확인 내용: 차단 설정 수정 성공
- `POST /api/analyses`
  - 응답: `200 OK`
  - 확인 내용: 분석 요청 성공
- `POST /api/blocked-items`
  - 응답: `201 Created`
  - 확인 내용: 보관함 저장 성공
- `GET /api/blocked-items`
  - 응답: `200 OK`
  - 확인 내용: 보관함 목록 조회 성공
- `GET /api/interest-items`
  - 응답: `200 OK`
  - 확인 내용: 관심 정보 목록 조회 성공
- `GET /api/interest-items/urls`
  - 응답: `200 OK`
  - 확인 내용: 관심 정보 URL 목록 조회 성공
- `POST /api/interest-items`
  - 응답: `201 Created`
  - 확인 내용: 관심 정보 저장 성공
- `GET /api/interest-items/{interestItemId}`
  - 응답: `200 OK`
  - 확인 내용: 관심 정보 상세 조회 성공
- `DELETE /api/blocked-items/{blockedItemId}`
  - 응답: `200 OK`
  - 확인 내용: 보관함 삭제 성공

### 2. 실패 API

- `POST /api/interests/select`
  - 실패 원인: 로컬 DB에 카탈로그 관심사 데이터가 없어 테스트 대상 `interestId`를 확보하지 못함
- `PUT /api/interest-targets`
  - 실패 원인: 동기화에 사용할 카탈로그 관심사 2개를 확보하지 못함

