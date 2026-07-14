## 애니메이션 — TMDB (영화/드라마와 동일 소스)

> Jikan 대신 TMDB 사용. language=ko-KR로 한국어 제목 제공, 공식 API라 안정적.

베이스: `https://api.themoviedb.org/3`
인증: 헤더 `Authorization: Bearer {ACCESS_TOKEN}`

# 애니 검색 (TV 시리즈형 애니)
GET /search/tv?query={제목}&language=ko-KR

# 애니 검색 (극장판 애니)
GET /search/movie?query={제목}&language=ko-KR

# 애니 상세 (TV, 장르 포함)
GET /tv/{tv_id}?language=ko-KR

# 애니 상세 (극장판)
GET /movie/{movie_id}?language=ko-KR

# 애니메이션 장르로 필터링 (TV, 장르 id 16 = Animation)
GET /discover/tv?with_genres=16&language=ko-KR&sort_by=popularity.desc

# 애니메이션 장르로 필터링 (극장판)
GET /discover/movie?with_genres=16&language=ko-KR&sort_by=popularity.desc

예시: https://api.themoviedb.org/3/search/tv?query=귀멸의 칼날&language=ko-KR
참고: 애니메이션 장르 id는 16. with_genres=16으로 애니만 걸러낼 수 있음.

## ~~애니메이션 — Jikan (키 불필요)~~

> 해당 API는 한국어 지원이 약해서 더 이상 사용하지 않음

베이스: `https://api.jikan.moe/v4`
인증: 없음

```
# 애니 검색
GET /anime?q={제목}

# 애니 상세 (장르 포함)
GET /anime/{anime_id}

# 애니 장르 목록
GET /genres/anime

# 시즌별 애니
GET /seasons/{year}/{season}       # 예: /seasons/2026/winter

# 상위 랭킹
GET /top/anime
```

예시: `https://api.jikan.moe/v4/anime?q=frieren`
주의: rate limit이 빡빡합니다(초당 3회, 분당 60회). Redis 캐싱 필수.