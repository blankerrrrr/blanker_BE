# 017-update-data-modeling-and-ai-task

## 작업 개요
- 작업명: 데이터 모델링 문서 갱신 및 AI placeholder TASK 등록
- 관련 TASK: 사용자 요청
- 관련 API/문서: `TASK.md`, `docs/data-modeling.md`
- 커밋 메시지: `feat: 데이터 모델링 문서 갱신`

## 변경한 파일
- `docs/data-modeling.md`
- `TASK.md`

## 구체적인 구현 내용
- AI placeholder 파일 구현 작업을 `TASK.md`에 다음 작업으로 등록했다.
- 데이터 모델링 문서의 Public ID 규칙을 `{model}_{id}` 형식으로 수정했다.
- 사용자 모델에서 제거된 약관 동의 필드 설명을 삭제했다.
- 주요 테이블의 내부 PK와 Public ID 컬럼 설명을 현재 모델 구조에 맞게 정리했다.
- 보관함 관계 설명을 `analysis_requests` 기준으로 수정했다.

## 검증 내용
- 실행 명령: `rg -n "01HZX|termsAgreed|privacyAgreed|약관|개인정보 처리 동의" docs\data-modeling.md`
- 검증 결과: 구식 ID 예시와 제거된 signup 약관 필드 잔존 여부 확인

## 참고
- `TASK.md`는 `.gitignore` 대상이라 커밋에는 포함되지 않는다.
