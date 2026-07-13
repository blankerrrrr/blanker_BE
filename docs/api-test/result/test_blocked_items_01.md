## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/blocked-items` 목록/저장/삭제
- 실패 및 수정이 필요한 API: 없음

### 1. POST /api/blocked-items

- API 정상 작동
- 응답: 201 Created
- 확인 내용: 차단 콘텐츠 보관함 저장

### 2. GET /api/blocked-items?page=1&size=20&type=SPOILER

- 최초 테스트 실패: 500 Internal Server Error
- 원인: PostgreSQL JSON 컬럼에 `.contains()` 필터를 직접 적용
- 수정: `blocked_items.categories`를 JSONB로 cast한 뒤 contains 필터 적용
- 재테스트 결과: 200 OK

### 3. DELETE /api/blocked-items/{blockedItemId}

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 인증된 사용자 소유 보관함 항목 삭제
