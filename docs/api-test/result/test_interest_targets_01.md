## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/interest-targets` 생성/목록/수정/삭제
- 실패 및 수정이 필요한 API: 없음

### 1. POST /api/interest-targets

- API 정상 작동
- 응답: 201 Created
- 확인 내용: 인증된 사용자 기준 관심 대상 생성

### 2. GET /api/interest-targets

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 생성된 관심 대상 목록 조회

### 3. PATCH /api/interest-targets/{interestTargetId}

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 관심 대상 이름, 별칭, 키워드 수정

### 4. DELETE /api/interest-targets/{interestTargetId}

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 인증된 사용자 소유 관심 대상 삭제
