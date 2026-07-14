## 영화 + 드라마 — TMDB

베이스: `https://api.themoviedb.org/3`
인증: 헤더 `Authorization: Bearer {API_KEY}` (또는 쿼리 `?api_key={KEY}`)

```
# 영화 검색
GET /search/movie?query={제목}&language=ko-KR

# 영화 상세 (장르 포함)
GET /movie/{movie_id}?language=ko-KR

# 영화 장르 목록
GET /genre/movie/list?language=ko-KR

# 인기 영화
GET /movie/popular?language=ko-KR&page=1

# 드라마(TV) 검색
GET /search/tv?query={제목}&language=ko-KR

# 드라마 상세
GET /tv/{tv_id}?language=ko-KR

# 드라마 장르 목록
GET /genre/tv/list?language=ko-KR
```

예시: `https://api.themoviedb.org/3/movie/550?language=ko-KR`
