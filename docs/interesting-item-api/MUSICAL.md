## 뮤지컬(공연) — KOPIS

베이스: `http://www.kopis.or.kr/openApi/restful`
인증: 쿼리 `?service={서비스키}`

```
# 공연 목록 (장르 GGGD가 뮤지컬)
GET /pblprfr?service={KEY}&stdate={YYYYMMDD}&eddate={YYYYMMDD}&cpage=1&rows=10&shcate=GGGD

# 공연 상세
GET /pblprfr/{공연ID}?service={KEY}

# 공연장 정보
GET /prfplc?service={KEY}&cpage=1&rows=10
```

`shcate=GGGD`가 뮤지컬 장르 코드입니다(연극은 AAAA 등). 응답은 XML입니다. 공공데이터포털 또는 KOPIS에서 서비스키를 발급받습니다.

## 정리 표 (인증 방식 중심)

| 카테고리 | 베이스 URL | 인증 위치 | 응답 |
|---|---|---|---|
| 영화/드라마 | api.themoviedb.org/3 | 헤더 Bearer | JSON |
| 애니 | api.jikan.moe/v4 | 없음 | JSON |
| 게임 | api.rawg.io/api | 쿼리 `key` | JSON |
| 소설(알라딘) | aladin.co.kr/ttb/api | 쿼리 `ttbkey` | JSON/XML |
| 웹툰 | (자체 배포) | 프로젝트마다 | JSON |
| 뮤지컬 | kopis.or.kr/openApi/restful | 쿼리 `service` | XML |