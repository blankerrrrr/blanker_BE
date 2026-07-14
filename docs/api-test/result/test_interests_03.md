## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/interests/types`, `/api/interests`, `/api/interests/select`, `/api/interests/targets`
- 실패 및 수정이 필요한 API: 없음

### 1. GET /api/interests/types

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 게임, 기타, 드라마, 뮤지컬, 소설, 애니메이션, 영화, 웹툰과 preview image URL 반환

### 2. GET /api/interests

- API 정상 작동
- 응답: 200 OK
- 확인 내용: `interestType=영화` 조건으로 관심사 목록 조회
- 확인 데이터: `interestId=interest_5`

### 3. POST /api/interests/select

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 조회한 `interestId`를 현재 사용자의 관심 대상으로 선택

### 4. POST /api/interests/targets

- API 정상 작동
- 응답: 201 Created
- 확인 내용: 직접 관심 대상 등록 성공
