# 기술 스택

본 문서는 MVP 구현 기준 기술 스택을 정의한다.

## 1. 전체 스택 요약

| 영역 | 기술 | 용도 |
| --- | --- | --- |
| Backend API | FastAPI | 인증, 사용자 설정, 보관함, 관심 정보 API |
| Language | Python 3.12+ | 백엔드 및 AI 분석 로직 구현 |
| Python Package Manager | uv | 백엔드 의존성 설치, 가상환경, 실행 관리 |
| Database | PostgreSQL | 사용자, 관심 대상, 분석 결과, 보관함, 관심 정보 저장 |
| Cache / Session | Redis | refresh token hash 저장, 세션 관리 |
| Authentication | JWT | access token 기반 인증 |
| Refresh Token | HttpOnly Secure Cookie + Redis | 클라이언트는 Cookie, 서버는 Redis hash 저장 |
| ORM | SQLAlchemy 2.0 | DB 모델 및 쿼리 작성 |
| Migration | Alembic | DB schema migration |
| Validation | Pydantic v2 | 요청/응답 DTO 검증 |
| AI Analysis | Anthropic API | 텍스트/이미지 콘텐츠 분석 |
| Browser Extension | WXT + TypeScript | 웹 콘텐츠 감지, DOM 분석, 블러 처리 |
| Extension UI | React | 팝업, 설정 화면, 보관함 UI |
| Test | pytest | 백엔드 단위/통합 테스트 |
| API Docs | OpenAPI / Swagger UI | FastAPI 자동 API 문서 |

## 2. 백엔드

| 항목 | 선택 |
| --- | --- |
| Framework | FastAPI |
| Runtime | Python 3.12 이상 |
| Package / Env Manager | uv |
| ASGI Server | Uvicorn |
| DTO / Schema | Pydantic v2 |
| ORM | SQLAlchemy 2.0 |
| Migration | Alembic |
| Password Hash | Argon2 또는 bcrypt |
| API 문서 | FastAPI OpenAPI, Swagger UI |

FastAPI는 API 서버와 AI 분석 로직을 Python 기반으로 통합하기 좋다. 콘텐츠 분석, 유사도 계산, 중복 판단, Anthropic API 연동을 하나의 Python 백엔드에서 다루기 위해 MVP에서는 백엔드와 분석 서버를 하나의 FastAPI 애플리케이션으로 시작한다.

백엔드 의존성 설치와 실행은 `uv`를 기준으로 한다. 로컬 개발 환경은 `backend` 디렉터리에서 `uv sync`로 구성하고, 서버 실행은 `uv run uvicorn app.main:app --reload`를 사용한다.

## 3. 인증

| 항목 | 방식 |
| --- | --- |
| 로그인 인증 | 이메일 + 비밀번호 |
| Access Token | JWT |
| Access Token 전달 | `Authorization: Bearer {accessToken}` |
| Refresh Token 저장 | HttpOnly Secure Cookie |
| Refresh Token 서버 저장 | Redis에 hash만 저장 |
| Refresh Token DB 저장 | 사용하지 않음 |
| 로그아웃 | Redis refresh token key 삭제 + Cookie 만료 |

Access token은 짧은 만료 시간을 가진 JWT로 발급한다. Refresh token 원문은 클라이언트의 JavaScript에서 접근하지 못하도록 HttpOnly Cookie에 저장하고, 서버에는 검증용 hash만 Redis에 저장한다.

## 4. 데이터베이스

| 항목 | 선택 |
| --- | --- |
| DB | PostgreSQL |
| 주요 저장 데이터 | 사용자, 관심 대상, 차단 설정, 분석 요청/결과, 보관함, 관심 정보 |
| 시간 타입 | `timestamp with time zone` |
| 배열 데이터 | PostgreSQL `text[]` 또는 JSON 배열 |
| Public ID | 문자열 ID 사용. 예: `user_`, `target_`, `analysis_` |

PostgreSQL은 관계형 데이터와 검색/필터링이 필요한 보관함, 관심 정보, 분석 결과 저장에 사용한다.

## 5. Redis

| 용도 | 설명 |
| --- | --- |
| Refresh Token 검증 | `auth:refresh:{userId}:{tokenId}`에 refresh token hash 저장 |
| 사용자 세션 관리 | `auth:user-sessions:{userId}`에 tokenId 목록 저장 |
| TTL 관리 | refresh token 만료 시간과 동일하게 Redis TTL 설정 |

Redis는 인증 세션성 데이터에만 사용하고, 영속 데이터는 PostgreSQL에 저장한다.

## 6. AI 분석

| 항목 | 선택 |
| --- | --- |
| Provider | Anthropic API |
| 분석 대상 | 텍스트, 이미지 URL, 주변 문맥 |
| 주요 결과 | 분류, 위험도, 관련도, 차단 여부, 차단 사유 |
| 후처리 | Python 기반 규칙/유사도 처리 |

AI 분석은 `POST /api/analysis-requests`에서 수행한다. 브라우저 확장은 DOM에서 분석 대상 콘텐츠를 수집하고, 서버는 사용자 관심 대상과 차단 설정을 함께 고려해 분석 결과를 반환한다.

## 7. 브라우저 확장

| 항목 | 선택 |
| --- | --- |
| Framework | WXT |
| Language | TypeScript |
| UI | React |
| 주요 역할 | DOM 감지, 동적 콘텐츠 감지, 분석 요청, 블러 처리 |
| 저장소 | `chrome.storage` 또는 browser storage |

웹페이지 DOM 접근과 블러 처리는 브라우저 확장 content script에서 수행한다. 서버는 분석 결과와 저장 기능을 제공하고, 실제 화면 차단은 확장 프로그램이 담당한다.

## 8. 테스트

| 영역 | 도구 |
| --- | --- |
| Backend Unit Test | pytest |
| API Test | pytest + httpx |
| DB Test | pytest fixture + test PostgreSQL |
| Extension E2E | Playwright |

## 9. 배포

| 영역 | 후보 |
| --- | --- |
| API Server | Docker 기반 배포 |
| Database | Managed PostgreSQL |
| Redis | Managed Redis |
| Extension | Chrome Web Store 배포 |

MVP 단계에서는 Docker Compose로 로컬 개발 환경을 구성하고, 배포 시 FastAPI, PostgreSQL, Redis를 분리 운영한다.
