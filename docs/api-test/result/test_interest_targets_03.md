## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/interest-targets` 목록 조회/동기화
- 실패 및 수정이 필요한 API: 없음

### 1. GET /api/interest-targets

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 현재 사용자가 선택한 카탈로그 관심사 목록 조회

### 2. PUT /api/interest-targets

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 선택 관심사 목록을 요청한 `interestId` 기준으로 동기화
