# 031. 개인 관심사 생성 API 명세 수정

## 작업 개요
- 작업명: 개인 관심사 생성 API 요청 계약 수정
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `POST /api/interest-targets`
- 커밋 메시지: `feat: 개인 관심사 생성 명세 수정`

## 변경한 파일
- `docs/api-spec/POST-api-interest-targets.md`

## 구체적인 구현 내용
- 클라이언트 요청을 `name`만 전달하는 구조로 문서화했다.
- 서버가 제목 기반 웹 검색 또는 AI 보강으로 `type`, `aliases`, `keywords`를 결정하는 흐름을 명시했다.
- 기존 클라이언트 입력 필드였던 `type`, `aliases`, `keywords`를 요청 명세에서 제거했다.

## 검증 내용
- 문서 변경 작업으로 별도 테스트는 수행하지 않았다.
