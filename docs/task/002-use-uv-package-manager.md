# 002-use-uv-package-manager

## 작업 개요
- 작업명: 백엔드 패키지 관리 도구 uv 적용
- 관련 TASK: 사용자 요청
- 관련 API/문서: `docs/tech-stack.md`, `backend/pyproject.toml`
- 커밋 메시지: `feat: uv 패키지 관리 적용`

## 변경한 파일
- `backend/pyproject.toml`
- `backend/Dockerfile`
- `backend/.python-version`
- `docs/tech-stack.md`

## 구체적인 구현 내용
- dev 의존성을 `uv`가 사용하는 `dependency-groups`로 이동했다.
- `tool.uv` 설정과 Python 버전 파일을 추가했다.
- Dockerfile을 `uv sync`, `uv run` 기반으로 변경했다.
- 기술 스택 문서에 `uv` 사용 방침과 실행 명령을 반영했다.

## 검증 내용
- 실행 명령: `python -c "import tomllib; tomllib.load(open('backend/pyproject.toml', 'rb'))"`
- 검증 결과: `pyproject.toml` 파싱 성공
- 실행 명령: `uv --version`
- 미검증 사유: 현재 로컬 환경에 `uv`가 설치되어 있지 않음
