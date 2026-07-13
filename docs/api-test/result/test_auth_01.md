## API 테스트 결과

### 요약

- 정상 작동하는 API: `/health`, `/api/auth/me` 인증 누락 응답, `/api/auth/signup` 약한 비밀번호 검증
- 실패 및 수정이 필요한 API: `/api/auth/signup`, `/api/auth/login`

### 1. /health

- API 정상 작동
- 응답: 200 OK

### 2. /api/auth/me

- 인증 토큰 누락 시 정상 작동
- 응답: 401 AUTH_UNAUTHORIZED

### 3. /api/auth/signup

- 약한 비밀번호 요청은 정상 작동
- 응답: 400 AUTH_WEAK_PASSWORD
- 정상 회원가입 요청은 500 Internal Server Error 발생
- 원인 추정: `alembic current` 실행 시 현재 revision이 출력되지 않아 DB migration 미적용 상태로 보임

### 4. /api/auth/login

- 정상 로그인 요청은 500 Internal Server Error 발생
- 원인 추정: 회원가입과 동일하게 DB migration 미적용 상태로 보임

### 5. migration 적용

- 실행 명령: `.\\.venv\\Scripts\\python.exe -m alembic upgrade head`
- 정상 작동 안함: `20260713_0004_create_analysis_tables.py` 적용 중 실패
- 원인: `analysis_results.analysis_content_id` FK가 `analysis_contents.analysis_content_id`를 참조하지만, 참조 대상 컬럼에 unique 제약이 없음

### 6. migration 수정 후 재테스트

- migration은 head까지 적용됨
- `/api/auth/signup`, `/api/auth/login`은 계속 500 Internal Server Error 발생
- 직접 service 호출은 회원가입 성공
- 원인: 서버 실행 위치에 따라 `.env`를 읽지 못하고 기본 DB URL을 사용하는 설정 문제로 판단

### 7. 설정 경로 수정 후 재테스트

- `backend/app/core/config.py`에서 `.env` 경로를 backend 디렉터리 기준으로 고정
- ruff 검사 통과
- 로컬 코드 기준 설정 로딩 확인 완료
- 8000 포트 서버는 `/api/auth/signup`, `/api/auth/login`이 계속 500 반환
- 판단: 실행 중인 서버 프로세스에 변경 사항이 반영되지 않은 상태로 보이며 서버 재시작 후 재테스트 필요

### 8. 서버 재시작 후 재테스트

- `/api/auth/signup` 정상 작동
- 응답: 201 Created
- `/api/auth/login`은 존재하는 계정에서 500 Internal Server Error 발생
- 없는 계정 로그인은 401 AUTH_INVALID_CREDENTIALS로 정상 작동
- 원인: Redis 연결 시 `unknown command 'HELLO'` 발생
- 조치: Redis client protocol을 RESP2로 고정

### 9. Redis 수정 후 전체 흐름 재테스트

- 정상 작동하는 API:
  - `/api/auth/signup`
  - `/api/auth/login`
  - `/api/auth/me`
  - `/api/interest-targets` 생성/목록/수정/삭제
  - `/api/block-settings` 조회/수정
  - `/api/analysis-requests`
  - `/api/interest-items` 생성/목록/상세
  - `/api/interest-item-groups/{interestItemGroupId}`
  - `/api/blocked-items` 저장/삭제
- 실패 및 수정이 필요한 API:
  - `GET /api/blocked-items?page=1&size=20&type=SPOILER`
- 원인: PostgreSQL JSON 컬럼에 `.contains()` 필터를 직접 적용해 500 발생
- 조치: `blocked_items.categories`를 쿼리에서 JSONB로 cast한 뒤 contains 필터를 적용하도록 수정
- 비고: 실행 중인 8000 서버에 repository 수정 사항 반영을 위해 재시작 필요

### 10. 보관함 목록 필터 수정 후 재테스트

- `GET /api/blocked-items?page=1&size=20&type=SPOILER` 정상 작동
- 응답: 200 OK
- 전체 API 테스트 대상 정상 작동 확인
