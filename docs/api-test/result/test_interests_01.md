## API 테스트 결과

> 새로 추가된 관심사 조회 API 로컬 테스트

### 요약

- 정상 작동하는 API: `/api/interests`, `/api/interests/types`, `/api/interests/select`
- 실패 및 수정이 필요한 API: 없음

### 1. GET /api/interests

- API 정상 작동
- 확인 내용: `interestType` query string을 필수로 받고, `genre` 기본값을 `전체`로 처리함
- 확인 내용: `interestType`, `interestTypeImageUrl`, `title`, `genre`, `imageUrl` 응답 필드 반환

### 2. GET /api/interests 누락 요청

- API 정상 작동
- 확인 내용: `interestType` 누락 시 422 반환

### 3. GET /api/interests/types

- API 정상 작동
- 확인 내용: 관심사 종류의 `name`, `imageUrl` 응답 필드 반환

### 4. POST /api/interests/select

- API 정상 작동
- 확인 내용: 선택한 관심사를 인증된 사용자의 개인 관심사 응답 형태로 반환

### 검증 명령

- `.\.venv\Scripts\ruff.exe check . --no-cache`
- `.\.venv\Scripts\pytest.exe tests\unit\test_interest_api.py -q`

### 비고

- pytest는 테스트 4개 통과 출력까지 확인했으나 프로세스 종료 단계에서 타임아웃됨
