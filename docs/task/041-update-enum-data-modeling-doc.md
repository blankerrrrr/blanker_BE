# 041. 데이터 모델링 Enum 정의 문서 갱신

## 작업 개요
- 작업명: 현재 구현 기준 Enum 정의 문서화
- 관련 TASK: `TASK.md`
- 관련 API/문서: `docs/data-modeling.md`
- 커밋 메시지: `docs: 데이터 모델링 Enum 정의 갱신`

## 변경한 파일
- `docs/data-modeling.md`
- `docs/task/041-update-enum-data-modeling-doc.md`

## 구체적인 구현 내용
- `InterestType` enum 값을 현재 구현 기준으로 추가했다.
- `BlockSettingCategory`와 `BlockCategory`를 별도 enum으로 구분해 문서화했다.
- enum 값이 DB native enum이 아니라 문자열 컬럼에 저장되고, API 계층에서 Pydantic `StrEnum`으로 검증된다는 내용을 추가했다.

## 검증 내용
- `backend/app/schemas/interest.py`
- `backend/app/schemas/interest_target.py`
- `backend/app/schemas/block_setting.py`
- `backend/app/schemas/analysis.py`
