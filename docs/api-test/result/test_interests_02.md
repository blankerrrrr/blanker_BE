## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/interests/types`, `/api/interests`, `/api/interests/targets`
- 실패 및 수정이 필요한 API: 없음
- 테스트 불가 API: `/api/interests/select`

### 1. GET /api/interests/types

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 관심사 종류 목록 조회 성공
- 참고: 현재 서버 DB의 카탈로그 데이터가 비어 `items: []` 반환

### 2. GET /api/interests

- API 정상 작동
- 응답: 200 OK
- 확인 내용: `interestType=영화` 조건으로 관심사 목록 조회 성공
- 참고: 현재 서버 DB의 카탈로그 데이터가 비어 `items: []` 반환

### 3. POST /api/interests/select

- 테스트 불가
- 원인: 요청에 필요한 `interestId`를 카탈로그 목록에서 얻지 못함
- 조치 필요: 카탈로그 seed/import 데이터 적재 후 재테스트 필요

### 4. POST /api/interests/targets

- API 정상 작동
- 응답: 201 Created
- 확인 내용: 직접 관심 대상 등록 성공
