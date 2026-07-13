# 콘텐츠 분석 요청 API

`POST /api/analysis-requests`

## 설명

확장 프로그램이 수집한 웹페이지의 텍스트, 이미지, 영역 단위 콘텐츠를 서버에 분석 요청한다. 서버는 분류, 위험도, 관련도, 차단 여부, 차단 사유를 반환한다.

## REQUEST

```json
{
  "page": {
    "url": "https://example.com/article",
    "title": "페이지 제목"
  },
  "contents": [
    {
      "clientContentId": "node_001",
      "unitType": "TEXT",
      "text": "분석할 텍스트",
      "contextText": "주변 문맥",
      "selector": "article > p:nth-child(1)"
    },
    {
      "clientContentId": "node_002",
      "unitType": "IMAGE",
      "imageUrl": "https://example.com/image.png",
      "altText": "이미지 설명",
      "contextText": "주변 문맥",
      "selector": "article img:nth-child(1)"
    }
  ]
}
```

## RESPONSE `200`

```json
{
  "success": true,
  "data": {
    "analysisRequestId": "analysis_request_1",
    "results": [
      {
        "clientContentId": "node_001",
        "categories": ["SPOILER"],
        "riskLevel": "HIGH",
        "relevanceLevel": "HIGH",
        "shouldBlock": true,
        "blockAction": {
          "unitType": "TEXT",
          "reason": "등록한 관심 작품과 관련된 스포일러 가능성이 높습니다.",
          "relatedTopics": ["작품명"]
        }
      }
    ]
  }
}
```

## 에러 코드

| 코드 | HTTP Status | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 401 | 인증 토큰 누락 또는 유효하지 않은 토큰 |
| `ANALYSIS_CONTENT_TOO_LARGE` | 413 | 분석 요청 본문이 허용 크기를 초과함 |
| `ANALYSIS_FAILED` | 502 | AI 분석 처리 실패 |
