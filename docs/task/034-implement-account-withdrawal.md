# 034. 회원탈퇴 기능 구현

## 작업 개요
- 작업명: 회원탈퇴 기능 구현
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `DELETE /api/auth/me`
- 커밋 메시지: `feat: 회원탈퇴 기능 구현`

## 변경한 파일
- `backend/app/cache/refresh_token_store.py`
- `backend/app/db/repositories/user_repository.py`
- `backend/app/services/token_service.py`
- `backend/app/services/auth_service.py`
- `backend/app/api/auth.py`
- `docs/api-spec/DELETE-api-auth-me.md`

## 구체적인 구현 내용
- `RefreshTokenStore.delete_all_by_user_id()`: Redis KEYS 패턴으로 해당 유저의 모든 리프레시 토큰 키를 조회 후 일괄 삭제.
- `UserRepository.delete()`: SQLAlchemy session.delete()로 유저 하드 삭제.
- `TokenService.delete_all_refresh_tokens()`: RefreshTokenStore의 전체 삭제를 래핑.
- `AuthService.withdraw()`: 유저 존재 확인 → 모든 토큰 삭제 → 유저 하드 삭제 → 커밋.
- `DELETE /api/auth/me`: AccessToken 인증 후 withdraw 호출, refreshToken 쿠키 제거.

## 검증 내용
- 실행 명령: (미실행)
- 검증 결과: (미실행)
