## 게임 — RAWG

베이스: `https://api.rawg.io/api`
인증: 쿼리 `?key={API_KEY}`

```
# 게임 검색
GET /games?key={KEY}&search={제목}

# 게임 상세 (장르 포함)
GET /games/{game_id}?key={KEY}

# 게임 장르 목록
GET /genres?key={KEY}

# 플랫폼별/장르별 필터
GET /games?key={KEY}&genres={장르}&platforms={플랫폼id}
```

예시: `https://api.rawg.io/api/games?key=YOUR_KEY&search=zelda`