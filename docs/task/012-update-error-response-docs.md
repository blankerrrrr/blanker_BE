# 012-update-error-response-docs

## 작업 개요
- 작업명: 공통 에러 응답 문서 수정
- 관련 TASK: 공통 에러 응답 문서 수정
- 관련 API/문서: `docs/api-spec/api-rule.md`, `docs/api-spec/api-spec-template.md`
- 커밋 메시지: `feat: 공통 에러 응답 문서 수정`

## 변경한 파일
- `docs/api-spec/api-rule.md`
- `docs/api-spec/api-spec-template.md`
- `docs/task/012-update-error-response-docs.md`

## 구체적인 구현 내용
- 공통 실패 응답 예시를 전역 예외 핸들러의 `error_code`, `message` 형식으로 수정했다.
- API 문서 템플릿의 성공 응답 예시에서 더 이상 사용하지 않는 `error: null`을 제거했다.
- 금지 사항에 정의되지 않은 중첩 error 객체 사용 금지를 추가했다.

## 변경된 플로우
- 요청: API에서 예외가 발생한다.
- 처리: 전역 예외 핸들러가 ErrorCode 기반 응답을 생성한다.
- 응답: `{ "error_code": "...", "message": "..." }` 형식으로 반환한다.

## 검증 내용
- 실행 명령: `rg -n 'success: false|"success": false|"error"|"timestamp"|error\.code|error\.status' docs\api-spec`
- 검증 결과: 기존 실패 응답 형식 잔존 여부 확인

## 참고
-
