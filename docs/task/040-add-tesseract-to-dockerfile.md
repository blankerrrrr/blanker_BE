# 040. Dockerfile Tesseract 설치 추가

## 작업 개요
- 작업명: Dockerfile에 Tesseract OCR 설치 포함
- 관련 TASK: `TASK.md`
- 관련 API/문서: `POST /api/analyses/screenshot`, `backend/Dockerfile`
- 커밋 메시지: `feat: Docker 이미지에 Tesseract OCR 설치 추가`

## 변경한 파일
- `backend/Dockerfile`
- `docs/task/040-add-tesseract-to-dockerfile.md`

## 구체적인 구현 내용
- Debian bookworm 기반 이미지 빌드 시 `tesseract-ocr`를 설치하도록 추가했다.
- 영어/한국어 OCR을 위해 `tesseract-ocr-eng`, `tesseract-ocr-kor` 패키지를 함께 설치하도록 추가했다.
- apt 패키지 목록 캐시를 삭제해 이미지 레이어 크기 증가를 줄였다.

## 변경된 플로우
- 컨테이너 이미지 빌드 시 OCR 실행 파일과 `eng`, `kor` 언어 데이터가 함께 포함된다.
- `/api/analyses/screenshot` 실행 시 컨테이너 내부에서 Tesseract OCR을 바로 사용할 수 있다.

## 검증 내용
- Dockerfile 변경 내용 검토
- 실행 명령: `docker build -t blanker-api:tesseract-test .`
- 검증 결과: Docker Desktop Linux engine 데몬에 연결할 수 없어 빌드 검증은 수행하지 못했다.
