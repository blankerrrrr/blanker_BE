## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/interest-targets` 목록 조회
- 실패 및 수정이 필요한 API: 없음
- 테스트 불가 API: `PUT /api/interest-targets`

### 1. GET /api/interest-targets

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 현재 사용자가 선택한 카탈로그 관심사 목록 조회 성공
- 참고: 이 API는 `PUT /api/interest-targets`로 선택된 카탈로그 관심사만 반환하므로, `/api/interests/targets`로 직접 등록한 항목은 포함하지 않음

### 2. PUT /api/interest-targets

- 테스트 불가
- 원인: 요청에 필요한 `interestId`를 카탈로그 목록에서 얻지 못함
- 조치 필요: 카탈로그 seed/import 데이터 적재 후 재테스트 필요
