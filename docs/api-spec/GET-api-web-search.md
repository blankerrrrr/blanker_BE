# 웹 검색 API

`GET /api/web-search?query=테스트&count=5`

## 설명

서버가 외부 검색 공급자 API를 호출해 인터넷 검색 결과를 반환한다. 기본 구현은 Brave Web Search API를 사용하며, 서버 환경 변수에 검색 API 키가 설정되어 있어야 한다.

## 구현 방안

1. 클라이언트는 서버의 `GET /api/web-search`만 호출한다.
2. 서버는 `WEB_SEARCH_API_URL`과 `WEB_SEARCH_API_KEY`로 외부 검색 API를 호출한다.
3. 외부 응답 중 `web.results`를 `title`, `url`, `description` 필드로 정규화한다.
4. 외부 API 키가 없으면 `WEB_SEARCH_NOT_CONFIGURED`, 호출 실패 시 `WEB_SEARCH_FAILED`를 반환한다.

## REQUEST

```json
{}
```

### Query String

| 필드 | 필수 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `query` | Yes | - | 검색어 |
| `count` | No | `5` | 결과 수. 1~20 |
| `country` | No | `KR` | 국가 코드 |
| `searchLang` | No | `ko` | 검색 언어 |
| `freshness` | No | - | 최신성 필터. 예: `pd`, `pw`, `pm`, `py` |

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "query": "테스트",
    "results": [
      {
        "title": "검색 결과 제목",
        "url": "https://example.com/article",
        "description": "검색 결과 요약"
      }
    ]
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `INVALID_REQUEST_BODY` | 422 | query 누락 또는 요청 형식 오류 |
| `WEB_SEARCH_NOT_CONFIGURED` | 503 | 서버 검색 API 키 미설정 |
| `WEB_SEARCH_FAILED` | 502 | 외부 검색 API 호출 실패 |
