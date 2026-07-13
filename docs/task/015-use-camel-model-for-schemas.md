# 015-use-camel-model-for-schemas

## 작업 개요
- 작업명: 스키마 CamelModel 상속 적용
- 관련 TASK: request에 CamelModel를 상속하도록 변경하여 일일이 alias를 지정하는 코드 제거
- 관련 API/문서: `backend/app/schemas/common.py`
- 커밋 메시지: `feat: 스키마 CamelModel 상속 적용`

## 변경한 파일
- `backend/app/schemas/auth.py`
- `backend/app/schemas/analysis.py`
- `backend/app/schemas/blocked_item.py`
- `backend/app/schemas/block_setting.py`
- `backend/app/schemas/interest_item.py`
- `backend/app/schemas/interest_target.py`
- `backend/app/schemas/user.py`
- `backend/tests/unit/test_camel_model.py`
- `docs/task/015-use-camel-model-for-schemas.md`

## 구체적인 구현 내용
- request/response 스키마가 `CamelModel`을 상속하도록 변경했다.
- 반복되던 `ConfigDict(populate_by_name=True)`와 alias 전용 `Field(alias=...)`를 제거했다.
- 기본값과 `default_factory`가 필요한 필드만 `Field`를 유지했다.
- camelCase 요청 파싱과 응답 직렬화 테스트를 추가했다.

## 변경된 플로우
- 요청: 클라이언트는 camelCase 필드로 요청한다.
- 처리: `CamelModel` alias generator가 snake_case 모델 필드로 변환한다.
- 응답: `model_dump(by_alias=True)` 호출 시 camelCase 필드로 직렬화한다.

## 검증 내용
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m ruff check . --no-cache`
- 검증 결과: ruff 검사 통과
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "from app.schemas.auth import TokenResponse; print(TokenResponse(accessToken='a', expiresIn=1).model_dump(by_alias=True))"`
- 검증 결과: camelCase alias 직렬화 확인
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m pytest tests\\unit\\test_camel_model.py -q`
- 검증 결과: 테스트 통과 출력 후 프로세스 종료 지연으로 제한 시간 초과

## 참고
-
