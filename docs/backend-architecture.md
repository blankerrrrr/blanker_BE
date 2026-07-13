# 백엔드 패키지 설계

본 문서는 FastAPI 기반 백엔드의 패키지 구조를 정의한다. 대상 범위는 인증, API, DB, AI 분석이다.

## 1. 설계 원칙

| 원칙 | 설명 |
| --- | --- |
| Router는 얇게 유지 | HTTP 요청/응답 변환과 의존성 주입만 담당한다. |
| 비즈니스 로직은 Service에 배치 | 인증, 분석, 보관함 저장, 중복 통합 판단은 service 계층에서 처리한다. |
| DB 접근은 Repository로 격리 | SQLAlchemy 쿼리는 repository 계층에 둔다. |
| DTO와 ORM 분리 | Pydantic schema와 SQLAlchemy model을 직접 섞지 않는다. |
| AI 분석은 독립 모듈화 | OpenAI 호출, 프롬프트, 후처리를 `ai` 패키지에 격리한다. |
| Refresh token은 Redis 전용 | refresh token 원문은 Cookie, hash는 Redis에만 저장한다. |

## 2. 전체 디렉터리 구조

```text
backend/
  app/
    main.py
    api/
      __init__.py
      deps.py
      router.py
      auth.py
      interest_targets.py
      block_settings.py
      analysis_requests.py
      blocked_items.py
      interest_items.py
      interest_item_groups.py
    core/
      __init__.py
      config.py
      security.py
      exceptions.py
      error_codes.py
      response.py
      pagination.py
      id_generator.py
      time.py
    db/
      __init__.py
      base.py
      session.py
      models/
        __init__.py
        user.py
        interest_target.py
        block_setting.py
        analysis.py
        blocked_item.py
        interest_item.py
      repositories/
        __init__.py
        user_repository.py
        interest_target_repository.py
        block_setting_repository.py
        analysis_repository.py
        blocked_item_repository.py
        interest_item_repository.py
    schemas/
      __init__.py
      auth.py
      user.py
      interest_target.py
      block_setting.py
      analysis.py
      blocked_item.py
      interest_item.py
      common.py
    services/
      __init__.py
      auth_service.py
      token_service.py
      interest_target_service.py
      block_setting_service.py
      analysis_service.py
      blocked_item_service.py
      interest_item_service.py
      duplicate_group_service.py
    ai/
      __init__.py
      client.py
      prompts.py
      schemas.py
      content_classifier.py
      risk_evaluator.py
      duplicate_detector.py
      pipeline.py
    cache/
      __init__.py
      redis.py
      refresh_token_store.py
    workers/
      __init__.py
      tasks.py
    tests/
      unit/
      integration/
  alembic/
  alembic.ini
  pyproject.toml
  Dockerfile
  docker-compose.yml
```

## 3. 패키지 역할

| 패키지 | 역할 | 포함 예시 |
| --- | --- | --- |
| `app.api` | FastAPI 라우터와 HTTP 의존성 | endpoint, auth dependency, router 등록 |
| `app.core` | 공통 설정과 유틸리티 | 환경 설정, JWT, 응답 형식, 에러 코드 |
| `app.db` | DB 연결, ORM 모델, repository | SQLAlchemy session, table model, query |
| `app.schemas` | Pydantic 요청/응답 DTO | request body, response data, pagination |
| `app.services` | 유스케이스와 비즈니스 로직 | 회원가입, 분석 요청 처리, 보관함 저장 |
| `app.ai` | AI 분석 파이프라인 | OpenAI 호출, 분류, 위험도 판단, 중복 판단 |
| `app.cache` | Redis 접근 | refresh token hash 저장, 세션 set 관리 |
| `app.workers` | 비동기 작업 확장 지점 | 추후 큐 기반 분석, 배치 작업 |

## 4. API 라우터 설계

| 파일 | Endpoint 범위 | 연결 Service |
| --- | --- | --- |
| `api/auth.py` | `/api/auth/*` | `AuthService`, `TokenService` |
| `api/interest_targets.py` | `/api/interest-targets` | `InterestTargetService` |
| `api/block_settings.py` | `/api/block-settings` | `BlockSettingService` |
| `api/analysis_requests.py` | `/api/analysis-requests` | `AnalysisService` |
| `api/blocked_items.py` | `/api/blocked-items` | `BlockedItemService` |
| `api/interest_items.py` | `/api/interest-items` | `InterestItemService` |
| `api/interest_item_groups.py` | `/api/interest-item-groups` | `DuplicateGroupService` |

`api/router.py`는 각 도메인 라우터를 모아 `/api` prefix로 등록한다.

## 5. 인증 패키지 설계

| 파일 | 책임 |
| --- | --- |
| `services/auth_service.py` | 회원가입, 로그인, 로그아웃 유스케이스 |
| `services/token_service.py` | access token 발급, refresh token 생성/검증 |
| `core/security.py` | 비밀번호 해시, JWT encode/decode |
| `cache/refresh_token_store.py` | Redis refresh token hash 저장/조회/삭제 |
| `schemas/auth.py` | 회원가입, 로그인, 토큰 응답 DTO |
| `api/deps.py` | 현재 사용자 인증 dependency |

### 인증 흐름

| 흐름 | 처리 |
| --- | --- |
| 회원가입 | `AuthService`가 이메일 중복 확인, 비밀번호 해시, 사용자 생성 |
| 로그인 | 비밀번호 검증 후 access token 발급, refresh token Cookie 설정 |
| 토큰 재발급 | Cookie의 refresh token 검증, Redis hash 비교, token rotation |
| 로그아웃 | Redis refresh token key 삭제, Cookie 만료 |
| 인증된 요청 | `api/deps.py`에서 Bearer access token 검증 후 `currentUser` 주입 |

## 6. DB 모델 설계

| ORM 파일 | 테이블 |
| --- | --- |
| `models/user.py` | `users` |
| `models/interest_target.py` | `interest_targets` |
| `models/block_setting.py` | `block_settings` |
| `models/analysis.py` | `analysis_requests`, `analysis_contents`, `analysis_results` |
| `models/blocked_item.py` | `blocked_items` |
| `models/interest_item.py` | `interest_item_groups`, `interest_items` |

`db/base.py`는 모든 SQLAlchemy 모델 metadata를 Alembic이 인식할 수 있도록 import한다.

## 7. Repository 설계

| Repository | 주요 메서드 |
| --- | --- |
| `UserRepository` | `findByEmail`, `findById`, `create` |
| `InterestTargetRepository` | `findAllByUserId`, `create`, `update`, `delete` |
| `BlockSettingRepository` | `findAllByUserId`, `upsertMany` |
| `AnalysisRepository` | `createRequestWithContents`, `saveResults`, `findResultById` |
| `BlockedItemRepository` | `findPageByUserId`, `create`, `deleteByIdAndUserId` |
| `InterestItemRepository` | `findPageByUserId`, `findByIdAndUserId`, `createItem`, `createGroup`, `addItemToGroup` |

Repository는 DB 예외를 그대로 외부로 노출하지 않고 service 계층에서 도메인 에러로 변환할 수 있는 최소 단위만 반환한다.

## 8. Service 설계

| Service | 책임 |
| --- | --- |
| `AuthService` | 회원가입, 로그인, 로그아웃 |
| `TokenService` | JWT, refresh token, Redis 세션 관리 |
| `InterestTargetService` | 관심 대상 CRUD, 중복 등록 검증 |
| `BlockSettingService` | 차단 설정 조회/수정, 기본 설정 생성 |
| `AnalysisService` | 분석 요청 저장, AI pipeline 호출, 결과 저장 |
| `BlockedItemService` | 보관함 조회/저장/삭제 |
| `InterestItemService` | 관심 정보 조회/저장 |
| `DuplicateGroupService` | 중복 그룹 조회, 출처 추가, 대표 항목 관리 |

## 9. AI 분석 패키지 설계

| 파일 | 책임 |
| --- | --- |
| `ai/client.py` | OpenAI API client 래핑 |
| `ai/prompts.py` | 분류/위험도/관련도 판단 프롬프트 |
| `ai/schemas.py` | AI 요청/응답 내부 schema |
| `ai/content_classifier.py` | 스포일러, 유해정보, 관심정보 분류 |
| `ai/risk_evaluator.py` | 위험도와 관련도 판단 |
| `ai/duplicate_detector.py` | 관심 정보 중복 여부 판단 |
| `ai/pipeline.py` | 콘텐츠 분석 전체 흐름 조합 |

### 분석 처리 흐름

| 단계 | 처리 |
| --- | --- |
| 1 | 확장 프로그램이 텍스트/이미지/영역 단위 콘텐츠를 서버로 전송 |
| 2 | `AnalysisService`가 분석 요청과 콘텐츠 원본을 DB에 저장 |
| 3 | `ai.pipeline`이 사용자 관심 대상과 차단 설정을 기준으로 분석 |
| 4 | 분류, 위험도, 관련도, 차단 여부, 차단 사유를 생성 |
| 5 | `AnalysisRepository`가 분석 결과를 저장 |
| 6 | API가 확장 프로그램에 `blockAction`을 반환 |

## 10. Schema 설계

| 파일 | DTO 범위 |
| --- | --- |
| `schemas/common.py` | 공통 응답, 페이지네이션, 에러 응답 |
| `schemas/auth.py` | 회원가입, 로그인, 토큰 응답 |
| `schemas/user.py` | 사용자 계정 응답 |
| `schemas/interest_target.py` | 관심 대상 요청/응답 |
| `schemas/block_setting.py` | 차단 설정 요청/응답 |
| `schemas/analysis.py` | 분석 요청/결과 응답 |
| `schemas/blocked_item.py` | 보관함 요청/응답 |
| `schemas/interest_item.py` | 관심 정보, 중복 그룹 요청/응답 |

## 11. 의존성 방향

```text
api -> services -> repositories -> db.models
api -> schemas
services -> ai
services -> cache
services -> core
repositories -> db.session
```

| 금지 방향 | 이유 |
| --- | --- |
| `repositories -> services` | DB 접근 계층이 비즈니스 로직에 의존하면 순환 참조가 생긴다. |
| `models -> schemas` | ORM 모델과 API DTO가 결합된다. |
| `ai -> api` | 분석 로직이 HTTP 계층에 묶인다. |
| `core -> services` | 공통 모듈이 도메인 로직에 의존하면 재사용성이 떨어진다. |

## 12. 에러 처리 설계

| 파일 | 책임 |
| --- | --- |
| `core/error_codes.py` | `AUTH_INVALID_CREDENTIALS`, `INTEREST_TARGET_NOT_FOUND` 등 에러 코드 정의 |
| `core/exceptions.py` | 도메인 예외 클래스 정의 |
| `core/response.py` | 성공/실패 응답 포맷 통일 |
| `main.py` | FastAPI exception handler 등록 |

에러 응답은 `api-spec/api-rule.md`의 공통 실패 응답 형식을 따른다.

## 13. 테스트 구조

```text
tests/
  unit/
    services/
    ai/
  integration/
    api/
    repositories/
```

| 테스트 | 대상 |
| --- | --- |
| Unit | service, token, AI 후처리, duplicate detector |
| Integration | API endpoint, repository, DB transaction |
| Auth | JWT 검증, refresh token Cookie, Redis session |
| Analysis | 분석 요청 저장, AI 응답 mapping, blockAction 생성 |

## 14. MVP 구현 순서

| 순서 | 작업 |
| --- | --- |
| 1 | `core`, `db`, `schemas/common` 기반 구성 |
| 2 | `users`, 인증 API, JWT, Redis refresh token 구현 |
| 3 | 관심 대상, 차단 설정 CRUD 구현 |
| 4 | 분석 요청 저장 모델과 API 구현 |
| 5 | AI pipeline 기본 구현 |
| 6 | 보관함 API 구현 |
| 7 | 관심 정보 저장과 중복 그룹 API 구현 |
| 8 | 테스트와 예외 처리 정리 |
