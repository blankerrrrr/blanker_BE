## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/analyses`
- 실패 및 수정이 필요한 API: `/api/analyses/screenshot`

### 1. POST /api/analyses

- API 정상 작동
- 응답: 200 OK
- 확인 내용: 페이지 정보와 콘텐츠 단위 요청을 분석하고 `analysisRequestId`, 분석 결과 반환

### 2. POST /api/analyses/screenshot

- 정상 작동 안함
- 응답: 502 Bad Gateway
- 에러 코드: `SCREENSHOT_FAILED`
- 확인 내용:
  - 최초 확인 시 Playwright Chromium 브라우저 바이너리가 미설치 상태였음
  - `playwright install chromium` 실행 후 로컬 유틸리티 `take_screenshot("https://example.com")`는 성공
  - 하지만 현재 8000번 포트에서 실행 중인 API 서버는 계속 `SCREENSHOT_FAILED` 반환
- 조치 필요:
  - 현재 실행 중인 서버 프로세스가 사용하는 환경에 Playwright 브라우저가 설치되어 있는지 확인
  - 브라우저 설치 후 서버 재시작 후 재테스트
