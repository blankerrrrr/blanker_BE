## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/interest-item-groups/{interestItemGroupId}`
- 실패 및 수정이 필요한 API: 없음

### 1. GET /api/interest-item-groups/{interestItemGroupId}

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 대표 관심 정보와 출처 목록 조회

### 2. POST /api/interest-item-groups/{interestItemGroupId}/sources

- 별도 추가 출처 병합 요청은 이번 흐름에서 실행하지 않음
- 미검증 사유: 병합 대상이 될 두 번째 관심 정보 항목을 별도로 생성하지 않았음
