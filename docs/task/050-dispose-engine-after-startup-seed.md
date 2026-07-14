# 050. 시작 시드 이후 비동기 엔진 정리

## 작업 개요
- 작업명: 시작 시드와 Uvicorn 간 이벤트 루프 충돌 수정
- 관련 TASK: `TASK.md`
- 관련 API/문서: 서버 시작 스크립트
- 커밋 메시지: `feat: 비동기 엔진 이벤트 루프 충돌 수정`

## 변경한 파일
- `backend/scripts/start.py`
- `backend/tests/unit/test_start_script.py`
- `docs/task/050-dispose-engine-after-startup-seed.md`

## 구체적인 구현 내용
- 기본 관심사 시드 실행 후 SQLAlchemy `AsyncEngine`을 폐기하도록 변경했다.
- 시드 실패 시에도 `finally`에서 엔진 커넥션 풀이 정리되도록 했다.
- Uvicorn의 새 이벤트 루프가 이전 루프에서 생성한 커넥션을 재사용하지 않게 했다.
- 엔진 정리 성공 및 시드 실패 상황을 검증하는 단위 테스트를 추가했다.

## 변경된 플로우
- 기존: 시드용 이벤트 루프 종료 -> 기존 커넥션 풀 유지 -> Uvicorn 이벤트 루프 시작
- 변경: 시드 실행 -> 엔진 커넥션 풀 폐기 -> 시드용 루프 종료 -> Uvicorn 시작

## 검증 내용
- 실행 명령: `uv --cache-dir .uv-cache run ruff check scripts/start.py tests/unit/test_start_script.py`
- 검증 결과: 통과
- 실행 명령: `uv --cache-dir .uv-cache run pytest tests/unit -q --basetemp=.pytest-tmp-loop-fix`
- 검증 결과: 71 passed
