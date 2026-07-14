# Blanker Extension

Chrome Extension Manifest V3 기반 확장 프로그램입니다.

## 구조

- `manifest.json`: 확장 프로그램 진입 설정
- `src/background.js`: 백그라운드 서비스 워커
- `src/content.js`: 페이지 콘텐츠 분석 대상 수집
- `src/popup.html`: 팝업 UI
- `src/popup.js`: 팝업 상태 조회와 명령 처리
- `src/popup.css`: 팝업 스타일
- `src/config.js`: API host 기본값

## 로컬 실행

1. Chrome에서 `chrome://extensions` 접속
2. Developer mode 활성화
3. Load unpacked 선택
4. `extension/` 폴더 선택

## 백엔드 분리 원칙

- 백엔드 패키지, Python 환경, Docker 설정을 참조하지 않는다.
- 확장 프로그램은 빌드 없이 브라우저가 직접 읽는 정적 파일만 사용한다.
- API host는 `src/config.js`에서 확장 프로그램 전용 값으로 관리한다.
