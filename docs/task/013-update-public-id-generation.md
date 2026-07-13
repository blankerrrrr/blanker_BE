# 013-update-public-id-generation

## 작업 개요
- 작업명: Public ID 생성 방식 수정
- 관련 TASK: id_generator를 삭제, uuid 기반 제거 후 응답에서 id 반환 시 {model}_{id} 형식으로 반환
- 관련 API/문서: `docs/api-spec/*`
- 커밋 메시지: `feat: Public ID 생성 방식 수정`

## 변경한 파일
- `backend/app/core/id_generator.py`
- `backend/app/core/security.py`
- `backend/app/db/models/*`
- `backend/app/db/repositories/*`
- `backend/app/services/*`
- `backend/alembic/versions/20260713_0007_allow_generated_public_ids.py`
- `docs/api-spec/*`

## 구체적인 구현 내용
- UUID 기반 `id_generator.py`를 삭제했다.
- repository 저장 시 내부 PK를 받은 뒤 `{model}_{id}` 형식의 public id를 채우도록 공통 저장 헬퍼를 추가했다.
- public id 컬럼이 insert 직후 채워질 수 있도록 nullable 변경 마이그레이션을 추가했다.
- service 계층의 UUID 기반 public id 생성 호출을 제거했다.
- refresh token의 token id도 UUID 대신 `secrets` 기반 난수로 변경했다.
- API 문서의 ID 예시를 `{model}_{id}` 형식으로 수정했다.

## 변경된 플로우
- 요청: 리소스 생성 요청이 들어온다.
- 처리: DB flush로 내부 PK를 생성한 뒤 repository가 public id 컬럼에 `{model}_{id}`를 저장한다.
- 응답: 저장된 public id를 사용해 `user_1`, `interest_target_1` 같은 값을 반환한다.

## 검증 내용
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m ruff check . --no-cache`
- 검증 결과: ruff 검사 통과
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "from app.main import app; from app.core.security import create_refresh_token; print(app.title); print(create_refresh_token('user_1')[0].startswith('user_1.'))"`
- 검증 결과: 앱 import 및 refresh token 생성 확인
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m pytest tests\\test_health.py -q`
- 검증 결과: 테스트 통과 출력 후 프로세스 종료 지연으로 제한 시간 초과

## 참고
-
