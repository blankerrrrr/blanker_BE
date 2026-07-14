# API Summary

Base URL: `/api`

공통 응답 형식은 [api-rule.md](./api-rule.md)의 성공/실패 응답 규칙을 따른다.

| ID | 기능 | API | Method | Endpoint | Auth | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| API-001 | 로그인 및 회원가입 | 회원가입 | POST | `/api/auth/signup` | No | [POST-api-auth-signup.md](./POST-api-auth-signup.md) |
| API-002 | 로그인 및 회원가입 | 로그인 | POST | `/api/auth/login` | No | [POST-api-auth-login.md](./POST-api-auth-login.md) |
| API-003 | 로그인 및 회원가입 | 토큰 재발급 | POST | `/api/auth/refresh` | No | [POST-api-auth-refresh.md](./POST-api-auth-refresh.md) |
| API-004 | 로그인 및 회원가입 | 로그아웃 | POST | `/api/auth/logout` | Yes | [POST-api-auth-logout.md](./POST-api-auth-logout.md) |
| API-005 | 로그인 및 회원가입 | 내 계정 조회 | GET | `/api/auth/me` | Yes | [GET-api-auth-me.md](./GET-api-auth-me.md) |
| API-006 | 로그인 및 회원가입 | 회원탈퇴 | DELETE | `/api/auth/me` | Yes | [DELETE-api-auth-me.md](./DELETE-api-auth-me.md) |
| API-007 | 관심 대상 설정 | 선택한 관심사 목록 조회 | GET | `/api/interest-targets` | Yes | [GET-api-interest-targets.md](./GET-api-interest-targets.md) |
| API-008 | 관심 대상 설정 | 관심사 선택 동기화 | PUT | `/api/interest-targets` | Yes | [PUT-api-interest-targets.md](./PUT-api-interest-targets.md) |
| API-009 | 관심 대상 설정 | 관심사 제목 목록 조회 | GET | `/api/interest-targets/titles` | Yes | [GET-api-interest-targets-titles.md](./GET-api-interest-targets-titles.md) |
| API-011 | 차단 유형 및 민감도 설정 | 차단 설정 조회 | GET | `/api/block-settings` | Yes | [GET-api-block-settings.md](./GET-api-block-settings.md) |
| API-012 | 차단 유형 및 민감도 설정 | 차단 설정 수정 | PUT | `/api/block-settings` | Yes | [PUT-api-block-settings.md](./PUT-api-block-settings.md) |
| API-013 | 웹 콘텐츠 분석 | 콘텐츠 분석 요청 | POST | `/api/analyses` | Yes | [POST-api-analyses.md](./POST-api-analyses.md) |
| API-014 | 웹 콘텐츠 분석 | 스크린샷 분석 요청 | POST | `/api/analyses/screenshot` | Yes | [POST-api-analyses-screenshot.md](./POST-api-analyses-screenshot.md) |
| API-015 | 차단 콘텐츠 저장 | 보관함 목록 조회 | GET | `/api/blocked-items` | Yes | [GET-api-blocked-items.md](./GET-api-blocked-items.md) |
| API-016 | 차단 콘텐츠 저장 | 보관함 저장 | POST | `/api/blocked-items` | Yes | [POST-api-blocked-items.md](./POST-api-blocked-items.md) |
| API-017 | 차단 콘텐츠 저장 | 보관함 항목 삭제 | DELETE | `/api/blocked-items/{blockedItemId}` | Yes | [DELETE-api-blocked-items-blockedItemId.md](./DELETE-api-blocked-items-blockedItemId.md) |
| API-018 | 관심 정보 자동 수집 | 관심 정보 목록 조회 | GET | `/api/interest-items` | Yes | [GET-api-interest-items.md](./GET-api-interest-items.md) |
| API-019 | 관심 정보 자동 수집 | 관심 정보 상세 조회 | GET | `/api/interest-items/{interestItemId}` | Yes | [GET-api-interest-items-interestItemId.md](./GET-api-interest-items-interestItemId.md) |
| API-020 | 관심 정보 자동 수집 | 관심 정보 수집 저장 | POST | `/api/interest-items` | Yes | [POST-api-interest-items.md](./POST-api-interest-items.md) |
| API-021 | 관심 정보 자동 수집 | 관심 정보 URL 목록 조회 | GET | `/api/interest-items/urls` | Yes | [GET-api-interest-items-urls.md](./GET-api-interest-items-urls.md) |
| API-023 | 온보딩 관심사 | 관심사 목록 조회 | GET | `/api/interests` | Yes | [GET-api-interests.md](./GET-api-interests.md) |
| API-024 | 온보딩 관심사 | 관심사 종류 목록 조회 | GET | `/api/interests/types` | Yes | [GET-api-interests-types.md](./GET-api-interests-types.md) |
| API-025 | 온보딩 관심사 | 관심사 선택 | POST | `/api/interests/select` | Yes | [POST-api-interests-select.md](./POST-api-interests-select.md) |
| API-026 | 온보딩 관심사 | 관심사 검색 및 생성 | POST | `/api/interests/targets` | Yes | [POST-api-interests-targets.md](./POST-api-interests-targets.md) |
| API-027 | 온보딩 관심사 | 관심사 장르 목록 조회 | GET | `/api/interests/genres` | Yes | [GET-api-interests-genres.md](./GET-api-interests-genres.md) |
| API-028 | 관심 대상 설정 | 개인 관심사 분류 목록 조회 | GET | `/api/interest-targets/types` | Yes | [GET-api-interest-targets-types.md](./GET-api-interest-targets-types.md) |
| API-029 | 웹 검색 | 웹 검색 | GET | `/api/web-search` | Yes | [GET-api-web-search.md](./GET-api-web-search.md) |
