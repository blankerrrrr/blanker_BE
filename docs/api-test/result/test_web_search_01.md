- 파일 명 규칙: test_domain_nn.md
- 자원 별로 나누어서 파일을 작성하도록 한다.
- 예시) test_auth_01.md
- 절대 test_all_00.md나 test_api_00.md로 한꺼번에 작성하지 않는다.

---
## API 테스트 결과

> API 테스트 요청 시

### 요약

- 환경: 로컬 서버 `http://127.0.0.1:8000`
- 정상 작동하는 API: 없음
- 실패 및 수정이 필요한 API: `GET /api/web-search`

### 사전 확인

- `curl -I http://127.0.0.1:8000/health`
- 상태 코드: 405
- 응답 헤더에 `server: uvicorn`, `allow: GET`가 있어 로컬 서버 실행 중임을 확인했다.

### 1. POST /api/auth/signup

- 상태 코드: 409
- 테스트 계정 `api-test-user@example.com`이 이미 존재함을 확인했다.

### 2. POST /api/auth/login

- 상태 코드: 200
- 테스트 계정 로그인 및 access token 발급 정상 작동

### 3. GET /api/web-search?query=테스트&count=5

- 상태 코드: 503
- 응답:

```json
{
  "error_code": "WEB_SEARCH_NOT_CONFIGURED",
  "message": "웹 검색 API 설정이 필요합니다."
}
```

- 인증은 통과했으나 로컬 서버에 `WEB_SEARCH_API_KEY`가 설정되어 있지 않아 검색 공급자 호출 전 설정 오류가 반환됐다.

### 4. GET /api/web-search?query=테스트&count=5 - 인증 누락

- 상태 코드: 401
- 응답:

```json
{
  "error_code": "AUTH_UNAUTHORIZED",
  "message": "인증 토큰이 필요합니다."
}
```

- 인증 누락 시 보호 API로 정상 차단된다.

### 원인 및 조치

- 로컬 `.env`에 `WEB_SEARCH_API_KEY`가 비어 있어 정상 검색 결과 테스트는 진행하지 못했다.
- Brave Search API 키를 `WEB_SEARCH_API_KEY`에 설정한 뒤 서버 재시작 후 재테스트가 필요하다.
