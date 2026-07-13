# 011-update-exception-handling

## 작업 개요
- 작업명: 예외 처리 구조 수정
- 관련 TASK: exception 처리 수정
- 관련 API/문서: `TASK.md`
- 커밋 메시지: `feat: 예외 처리 구조 수정`

## 변경한 파일
- `backend/app/core/error_codes.py`
- `backend/app/core/exceptions.py`
- `backend/app/api/auth.py`
- `backend/app/api/deps.py`
- `backend/app/services/analysis_service.py`
- `backend/app/services/auth_service.py`
- `backend/app/services/blocked_item_service.py`
- `backend/app/services/duplicate_group_service.py`
- `backend/app/services/interest_item_service.py`
- `backend/app/services/interest_target_service.py`
- `TASK.md`

## 구체적인 구현 내용
- `ErrorCode`가 code, status_code, message를 갖도록 수정했다.
- `AppException` 생성자를 `AppException(ErrorCode.X)` 형태로 단순화했다.
- 전역 예외 핸들러가 `ErrorCode`에서 상태 코드와 메시지를 읽어 응답하도록 수정했다.
- 기존 예외 호출부에서 메시지와 status 인자 전달을 제거했다.

## 변경된 플로우
- 요청: 서비스 또는 API 의존성에서 `AppException(ErrorCode.X)`를 발생시킨다.
- 처리: 전역 예외 핸들러가 `ErrorCode`의 status_code, code, message를 읽는다.
- 응답: `{ "error_code": "...", "message": "..." }` 형식으로 반환한다.

## 검증 내용
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m ruff check . --no-cache`
- 검증 결과: ruff 검사 통과
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m pytest tests\\test_health.py -q`
- 검증 결과: health 테스트 통과 출력 후 프로세스 종료 지연으로 제한 시간 초과

## 참고
-
