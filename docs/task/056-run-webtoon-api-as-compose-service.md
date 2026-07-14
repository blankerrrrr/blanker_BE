# 056. 웹툰 API Compose 서비스 구성

## 작업 개요
- 작업명: 웹툰 API를 별도 Docker 컨테이너로 구성
- 관련 TASK: `TASK.next.md`
- 관련 스크립트/문서: `backend/scripts/import_interests.py`, `backend/docker-compose.yml`, `docs/interests-api/WEBTOON.md`
- 커밋 메시지: `feat: 웹툰 API Compose 서비스 구성`

## 변경한 파일
- `backend/docker-compose.yml`
- `backend/docker-compose.webtoon.yml`
- `backend/.env.example`
- `backend/webtoon-api/Dockerfile`
- `backend/scripts/import_interests.py`
- `backend/tests/unit/test_import_interests.py`
- `docs/interests-api/WEBTOON.md`
- `docs/task/056-run-webtoon-api-as-compose-service.md`
- `TASK.next.md`

## 구체적인 구현 내용
- Compose에 `webtoon-api` 서비스를 추가했다.
- 웹툰 API 빌드와 실행은 `docker-compose.webtoon.yml`로 분리했다.
- API 컨테이너에서 `KOREA_WEBTOON_API_URL=http://webtoon-api:3000`로 내부 서비스에 접근하도록 설정했다.
- `webtoon-api` 컨테이너는 `korea-webtoon-api` 오픈소스 프로젝트를 빌드해 3000번 포트로 실행한다.
- 메인 API Compose와 웹툰 API Compose는 `blanker-network` 네트워크를 공유한다.
- 관심사 가져오기 스크립트에서 웹툰 썸네일 배열을 첫 번째 문자열 URL로 정규화한다.

## 실행 방법
- 메인 Compose가 먼저 `blanker-network`를 생성한다.
- 웹툰 API는 `docker compose -f docker-compose.webtoon.yml up -d`로 별도 실행한다.
- 웹툰 API만 먼저 실행해야 할 경우 `docker network create blanker-network`를 선행한다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit\test_import_interests.py -q`
- 검증 결과: 2 passed
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: 74 passed
- 실행 명령: `.\.venv\Scripts\ruff.exe check scripts/import_interests.py tests/unit/test_import_interests.py --no-cache`
- 검증 결과: 통과
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `docker compose config`
- 검증 결과: 통과. 로컬 미설정 환경 변수 경고는 발생했으나 Compose 설정 렌더링은 성공했다.
- 실행 명령: `docker compose -f docker-compose.webtoon.yml config`
- 검증 결과: 통과
- 실행 명령: `docker compose build webtoon-api`
- 검증 결과: 실패. Docker Hub 인증 설정 문제로 `node:20-bookworm-slim` base image 토큰 조회 단계에서 401이 발생했다.
