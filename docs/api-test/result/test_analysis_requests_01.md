## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/analysis-requests`
- 실패 및 수정이 필요한 API: 없음

### 1. POST /api/analysis-requests

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 페이지 정보와 콘텐츠 단위 요청을 분석하고 결과 반환

### 참고

- rule 기반 분석 결과로 `categories`, `riskLevel`, `relevanceLevel`, `shouldBlock`, `blockAction` 반환 확인
