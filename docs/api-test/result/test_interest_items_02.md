## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/interest-items` 생성/목록/상세
- 실패 및 수정이 필요한 API: 없음

### 1. GET /api/interest-items

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 페이지네이션된 관심 정보 목록 조회

### 2. POST /api/interest-items

- API 정상 작동
- 응답: 201 Created
- 확인 내용: 등록한 관심 대상 이름과 `relatedTopics`가 일치하는 관심 정보 저장
- 참고: 최초 테스트에서는 `relatedTopics`가 등록 관심 대상과 일치하지 않아 `400 INTEREST_ITEM_NOT_RELEVANT`가 반환되었고, 올바른 테스트 데이터로 재테스트하여 통과 확인

### 3. GET /api/interest-items/{interestItemId}

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 저장된 관심 정보 상세 조회
