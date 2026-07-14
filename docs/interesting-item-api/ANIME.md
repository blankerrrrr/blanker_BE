## 애니메이션 — Jikan (키 불필요)

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