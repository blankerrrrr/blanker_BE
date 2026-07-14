# 060. 데이터 모델링 문서 구현 정합성 수정

## 작업 개요
- 작업명: `docs/data-modeling.md`를 현재 구현과 일치하도록 수정
- 관련 문서: `docs/data-modeling.md`
- 커밋 메시지: `docs: 데이터 모델링 문서 구현 정합성 수정`

## 변경한 파일
- `docs/data-modeling.md`
- `docs/task/060-align-data-modeling-with-implementation.md`

## 구체적인 수정 내용
- DB 테이블/컬럼명 표기를 snake_case로 통일했다.
- JSON 배열 컬럼 기본값 설명을 DB server default가 아닌 ORM `default=list` 기준으로 수정했다.
- `blocked_items.analysis_request_id`를 실제 FK가 아닌 논리 참조로 명시했다.
- Redis refresh token 저장 구조에서 구현에 없는 `auth:user-sessions:{user_id}` 설명을 제거했다.
- 전체 로그아웃 설명을 `auth:refresh:{user_id}:*` 패턴 삭제 방식으로 수정했다.

## 검증 내용
- 확인 파일: `backend/app/db/models/*`, `backend/app/cache/refresh_token_store.py`, `backend/app/services/token_service.py`
- 검증 결과: 문서의 테이블/컬럼/관계/Redis 설명을 현재 구현 기준으로 대조했다.
