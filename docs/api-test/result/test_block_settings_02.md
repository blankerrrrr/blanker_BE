## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/block-settings` 조회/수정
- 실패 및 수정이 필요한 API: 없음

### 1. GET /api/block-settings

- API 정상 작동
- 응답: 200 OK
- 확인 내용: spoiler, harmful, interest 차단 설정 조회

### 2. PUT /api/block-settings

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 차단 설정 수정 요청 성공
