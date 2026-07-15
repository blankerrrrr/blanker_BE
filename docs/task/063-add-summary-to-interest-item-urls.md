# 063. 관심 정보 URL 목록 요약 추가

## 작업 개요
- 작업명: 관심 정보 URL 목록 응답에 요약 포함
- 관련 API: `GET /api/interest-items/urls`
- 커밋 메시지: `feat: 관심 정보 URL 목록에 요약 추가`

## 변경 내용
- `interest_items.summary`를 URL 목록 응답 스키마에 추가했다.
- 기존 URL 목록 조회 모델에서 요약을 읽어 응답에 포함한다.
- API 명세와 단위 테스트를 갱신했다.

## 검증 내용
- 실행 명령: `uv --cache-dir .uv-cache run pytest tests/unit -q --basetemp=.pytest-all-interest-url-summary`
- 검증 결과: 88 passed
- 실행 명령: `uv --cache-dir .uv-cache run ruff check app/schemas/interest_item.py app/services/interest_item_service.py tests/unit/test_interest_item_api.py tests/unit/test_interest_item_service.py`
- 검증 결과: 통과
