## API 테스트 결과

### 요약

- 정상 작동하는 API: `/api/interests/targets`
- 실패 및 수정이 필요한 API: 없음

### 1. POST /api/interests/targets

- API 정상 작동
- 응답: 201 Created
- 확인 내용: `name`만 전달해 관심 대상 직접 등록 성공
- 요청 형식:

```json
{
  "name": "테스트 작품 20260714185824"
}
```

- 응답 확인:
  - `type`: `WORK`
  - `aliases`: `[]`
  - `keywords`: `["테스트 작품 20260714185824"]`

### 참고

- 현재 테스트 환경에서는 AI API 키가 설정되지 않아 fallback 보강이 적용됨
- fallback 동작: `type=WORK`, `aliases=[]`, `keywords=[name]`
