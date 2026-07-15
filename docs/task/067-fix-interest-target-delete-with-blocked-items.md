# 067. 차단 항목이 연결된 관심 대상 삭제 오류 수정

## 작업 개요

- `PUT /api/interest-targets` 동기화 중 차단 항목이 연결된 관심 대상을 삭제할 때 발생하는 `ForeignKeyViolationError`를 수정했다.
- `DELETE /api/interest-targets/{interestTargetId}`에도 동일한 삭제 정책을 적용했다.

## 원인

- 관심 대상 동기화는 요청에 포함되지 않은 기존 카탈로그 관심 대상을 삭제한다.
- `blocked_items.interest_target_id`가 해당 관심 대상을 참조하고 있는데 FK에 삭제 동작이 지정되어 있지 않았다.
- 따라서 참조 중인 `interest_targets` 행을 삭제할 수 없었다.

## 변경 내용

- `blocked_items.interest_target_id` FK에 `ON DELETE SET NULL`을 적용했다.
- 관심 대상 삭제 시 차단 항목은 보존하고 `interest_target_id`만 `NULL`로 변경한다.
- SQLAlchemy 모델과 기존 데이터베이스를 위한 Alembic 마이그레이션을 추가했다.
- 관심 대상 삭제 정책을 데이터 모델 문서에 명시했다.
- FK 삭제 동작을 검증하는 단위 테스트를 추가했다.

## 변경된 플로우

1. `PUT /api/interest-targets` 요청 목록에서 제외된 카탈로그 관심 대상을 삭제한다.
2. 해당 관심 대상을 참조하던 차단 항목의 `interest_target_id`가 자동으로 `NULL`이 된다.
3. 차단 항목 자체는 보관함에 계속 남는다.

## 검증

- `pytest tests\\unit\\test_blocked_item_model.py`
- 관련 관심 대상 및 관심사 서비스 테스트
