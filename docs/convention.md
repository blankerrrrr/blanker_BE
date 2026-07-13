# 컨벤션

본 문서는 Blanker 프로젝트의 작업, 문서, 코드 작성 규칙을 정의한다.

## 1. 기본 원칙

- 모든 문서와 작업 기록은 기본적으로 한국어로 작성한다.
- 지정된 작업 범위 외의 파일은 수정하지 않는다.
- 삭제, 초기화, 브랜치 변경, 원격 작업은 요청 또는 승인 없이 수행하지 않는다.
- 구현보다 기존 문서와 구조를 우선 확인한다.
- 불명확한 요구사항은 임의 확장하지 않고 필요한 범위만 구현한다.

## 2. 작업 진행 규칙

- 작업 전 `TASK.md`, 관련 `docs/` 문서, 기존 코드를 확인한다.
- 작업은 한 번에 하나의 기능 또는 하나의 문서 주제로 나누어 수행한다.
- 기능 구현 후에는 가능한 범위에서 테스트 또는 정적 검사를 실행한다.
- 검증하지 못한 경우 결과에 미검증 사유를 명시한다.
- 작업 완료 후 변경 파일과 변경 이유를 간단히 정리한다.

## 3. 문서 작성 규칙

- 문서는 Markdown으로 작성한다.
- 제목은 `#`, 주요 섹션은 `##`, 하위 섹션은 `###`를 사용한다.
- 표가 더 명확한 경우 Markdown 표를 사용한다.
- 명령어, 경로, API, 코드 식별자는 백틱으로 감싼다.
- 문서 내용은 현재 구현 또는 확정된 설계에 맞춘다.
- 추측성 내용은 확정 규칙처럼 작성하지 않는다.
- 작업 기록 문서는 `docs/task/000-task-template.md` 형식을 따른다.

## 4. API 규칙

API 상세 규칙은 `docs/api-spec/api-rule.md`를 따른다.

- 기본 prefix는 `/api`를 사용한다.
- URL은 소문자와 하이픈을 사용한다.
- 리소스명은 복수형을 사용한다.
- 요청과 응답 필드는 `camelCase`를 사용한다.
- 성공/실패 응답 형식은 공통 응답 포맷을 따른다.
- 에러 코드는 대문자 스네이크 케이스를 사용한다.
- 외부에 노출되는 ID는 DB 내부 ID가 아닌 public ID를 사용한다.
- 인증이 필요한 API는 `Authorization: Bearer {accessToken}`을 기준으로 한다.

## 5. 백엔드 코드 규칙

백엔드 구조는 `docs/backend-architecture.md`를 기준으로 한다.

| 계층 | 역할 |
| --- | --- |
| `api` | Router, 요청/응답 변환, 의존성 주입 |
| `services` | 비즈니스 로직 |
| `db/models` | SQLAlchemy ORM 모델 |
| `db/repositories` | DB 조회와 저장 로직 |
| `schemas` | Pydantic 요청/응답 DTO |
| `core` | 설정, 보안, 예외, 공통 응답, 유틸리티 |
| `ai` | AI 호출, 프롬프트, 분석 파이프라인 |

### Router

- Router는 얇게 유지한다.
- HTTP 상태, path/query/body, 인증 의존성만 다룬다.
- 비즈니스 판단은 service로 위임한다.
- ORM 모델을 그대로 응답하지 않는다.

### Service

- 주요 비즈니스 규칙은 service에 둔다.
- 여러 repository 또는 외부 모듈을 조합하는 흐름은 service가 담당한다.
- 인증, 분석, 차단, 관심 정보 처리 규칙은 service 계층에서 명확히 표현한다.

### Repository

- SQLAlchemy 쿼리는 repository에 둔다.
- API Router에서 직접 DB 쿼리를 작성하지 않는다.
- repository는 DB 모델 중심으로 동작하고, 응답 DTO 조립은 service 또는 schema 변환에서 처리한다.

### Schema

- 요청/응답 DTO는 Pydantic v2 모델을 사용한다.
- 외부 응답 필드는 `camelCase`를 사용한다.
- 내부 Python 필드는 `snake_case`를 사용한다.
- 요청 검증 규칙은 schema에 우선 배치한다.

## 6. Python 스타일

- Python 버전은 `3.12+`를 기준으로 한다.
- 패키지와 실행 환경은 `uv`를 사용한다.
- 포맷과 린트 기준은 `ruff` 설정을 따른다.
- 라인 길이는 `88`자를 기준으로 한다.
- import 정렬은 `ruff`의 `I` 규칙을 따른다.
- 타입 힌트를 사용한다.
- 불필요한 주석은 작성하지 않는다.
- 설명이 필요한 복잡한 흐름에만 짧은 주석을 추가한다.

## 7. 네이밍 규칙

| 대상 | 규칙 | 예시 |
| --- | --- | --- |
| Python 파일 | `snake_case.py` | `interest_target_service.py` |
| 변수/함수 | `snake_case` | `create_access_token` |
| 클래스 | `PascalCase` | `InterestTargetService` |
| 상수 | `UPPER_SNAKE_CASE` | `ACCESS_TOKEN_EXPIRE_MINUTES` |
| API path | 소문자 + 하이픈 | `/api/interest-targets` |
| 에러 코드 | 대문자 스네이크 케이스 | `USER_NOT_FOUND` |
| public ID prefix | 리소스 축약 접두사 | `user_`, `target_`, `analysis_` |

## 8. DB 및 마이그레이션 규칙

- 영속 데이터는 PostgreSQL에 저장한다.
- 세션성 refresh token hash는 Redis에 저장한다.
- DB 스키마 변경은 Alembic migration으로 관리한다.
- 시간 컬럼은 timezone을 포함하는 타입을 사용한다.
- 서버 응답 시간 값은 UTC 기준 ISO-8601 형식을 사용한다.
- public ID와 DB 내부 PK의 역할을 분리한다.

## 9. 인증 및 보안 규칙

- Access token은 `Authorization` header로 전달한다.
- Refresh token 원문은 HttpOnly Secure Cookie에 저장한다.
- Refresh token hash만 Redis에 저장한다.
- 클라이언트가 직접 보낸 사용자 ID는 신뢰하지 않는다.
- 비밀번호, 토큰, API key는 로그에 남기지 않는다.
- 환경 변수 예시는 `.env.example`에만 작성하고 실제 secret은 커밋하지 않는다.

## 10. 테스트 규칙

- 테스트 도구는 `pytest`를 사용한다.
- API 테스트는 `httpx` 기반 테스트를 사용한다.
- 단위 테스트는 `backend/tests/unit`에 둔다.
- 통합 테스트는 `backend/tests/integration`에 둔다.
- 신규 기능은 정상 케이스와 주요 실패 케이스를 함께 검증한다.
- 공통 응답 포맷, 인증 흐름, DB 변경 로직은 우선적으로 테스트한다.

## 11. 커밋 규칙

커밋 메시지는 다음 형식을 사용한다.

```text
feat: 한국어 메시지
```

권장 prefix는 다음과 같다.

| Prefix | 용도 |
| --- | --- |
| `feat` | 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | 문서 변경 |
| `test` | 테스트 추가 또는 수정 |
| `refactor` | 동작 변경 없는 구조 개선 |
| `chore` | 설정, 빌드, 기타 작업 |

- 커밋은 하나의 기능 또는 하나의 문서 변경 단위로 나눈다.
- 커밋 전 변경 파일을 확인한다.
- 관련 작업 기록이 필요한 경우 `docs/task/`에 변경 요약 문서를 작성한다.

## 12. 금지 사항

- 요청 범위 밖의 리팩터링
- 승인 없는 파일 삭제
- 승인 없는 원격 저장소 작업
- Router에 비즈니스 로직 작성
- ORM 모델을 API 응답으로 직접 반환
- 서비스마다 다른 응답 형식 사용
- 에러 코드 없이 메시지만 반환
- secret 또는 실제 운영 환경 값을 커밋
