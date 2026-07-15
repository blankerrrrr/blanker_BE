# 065. 분석 API의 Claude 응답 파싱 검증

## 작업 개요
- `POST /api/analyses`, `POST /api/analyses/screenshot`의 AI 분류 흐름을 재검증했다.
- Anthropic 모델을 `claude-sonnet-4-6`으로 변경하고 JSON 코드 펜스 응답을 처리하도록 보완했다.

## 변경 내용
- `AIClient`가 일반 JSON과 ```json 코드 펜스 JSON을 모두 파싱하도록 응답을 정규화한다.
- 코드 펜스 응답을 검증하는 단위 테스트를 추가했다.

## 검증
- `pytest tests\\unit\\test_ai_client.py tests\\unit\\test_analysis_api.py tests\\unit\\test_analysis_service.py`: 18개 통과
- 실제 Anthropic 분류 호출: 성공 (`SPOILER`, `HIGH` 응답 확인)
- `ruff check app\\ai\\client.py tests\\unit\\test_ai_client.py`: 통과
