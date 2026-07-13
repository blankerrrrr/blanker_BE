# 016-remove-signup-agreement-fields

## 작업 개요
- 작업명: 회원가입 약관 필드 제거
- 관련 TASK: signup api에 약관 동의 필드 2개 제거 후 문서 업데이트
- 관련 API/문서: `docs/api-spec/POST-api-auth-signup.md`
- 커밋 메시지: `feat: 회원가입 약관 필드 제거`

## 변경한 파일
- `backend/app/schemas/auth.py`
- `backend/app/services/auth_service.py`
- `backend/app/core/error_codes.py`
- `backend/tests/unit/test_camel_model.py`
- `docs/api-spec/POST-api-auth-signup.md`
- `docs/api-test/http/auth.http`
- `docs/erd.md`
- `docs/feat.md`
- `docs/task/016-remove-signup-agreement-fields.md`

## 구체적인 구현 내용
- 회원가입 요청에서 `termsAgreed`, `privacyAgreed` 필드를 제거했다.
- 회원가입 서비스의 약관 동의 검증을 제거했다.
- 더 이상 발생하지 않는 약관 미동의 에러 코드를 제거했다.
- 회원가입 API 문서와 HTTP 테스트 예시에서 약관 필드를 제거했다.
- ERD와 기능 명세의 회원가입 약관 필드 설명을 제거했다.

## 변경된 플로우
- 요청: 클라이언트가 이메일과 비밀번호만 전달한다.
- 처리: 서버는 비밀번호 정책과 이메일 중복만 검증한다.
- 응답: 기존 회원가입 성공 응답 형식을 유지한다.

## 검증 내용
- 실행 명령: `.\\.venv\\Scripts\\python.exe -m ruff check . --no-cache`
- 검증 결과: ruff 검사 통과
- 실행 명령: `.\\.venv\\Scripts\\python.exe -c "from app.schemas.auth import SignupRequest; print(SignupRequest.model_validate({'email':'a@b.com','password':'password123'}).model_dump())"`
- 검증 결과: 약관 필드 없이 SignupRequest 검증 확인

## 참고
- `docs/data-modeling.md`는 기존 대형 미커밋 변경이 있어 이번 커밋에 포함하지 않았다.
