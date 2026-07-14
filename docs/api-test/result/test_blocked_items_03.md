## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/blocked-items` 목록/저장/삭제
- 실패 및 수정이 필요한 API: 없음

### 1. GET /api/blocked-items

- API 정상 작동
- 응답: 200 OK
- 확인 내용: `page=1`, `size=20`, `type=SPOILER` 조건으로 보관함 목록 조회

### 2. POST /api/blocked-items

- API 정상 작동
- 응답: 201 Created
- 확인 내용: 분석 요청 ID와 콘텐츠 정보를 사용해 보관함 저장 성공

### 3. DELETE /api/blocked-items/{blockedItemId}

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 저장된 보관함 항목 삭제 성공
