# 066. 관심 대상 동기화 중복 충돌 수정

## 작업 개요

- `PUT /api/interest-targets`에서 직접 등록 관심 대상과 카탈로그 관심사의 이름이 같을 때 발생하는 500 오류를 수정했다.

## 원인

- 동기화 로직이 `interest_id IS NOT NULL`인 카탈로그 대상만 재사용했다.
- 같은 사용자·타입·이름의 직접 등록 대상은 찾지 못해 새 행을 insert했고, `uk_interest_targets_user_type_name` 제약조건에 걸렸다.

## 변경 내용

- 기존 카탈로그 대상이 없으면 공통 `_find_or_create_target()`을 사용한다.
- 동일 이름의 직접 등록 대상이 있으면 새로 만들지 않고 카탈로그 `interest_id`를 연결한다.
- 중복 충돌 상황을 검증하는 단위 테스트를 추가했다.

## 검증

- `pytest tests\\unit\\test_interest_service.py`: 통과
- 관련 관심사·관심 대상 테스트: 통과
