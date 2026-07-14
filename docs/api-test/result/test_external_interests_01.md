## API 테스트 결과

> interesting-item-api 후보 외부 API 호출 테스트

### 요약

- 정상 작동하는 API: TMDB 영화, TMDB 드라마, Jikan 애니메이션, 알라딘 도서
- 실패 및 확인이 필요한 API: RAWG 게임, KOPIS 뮤지컬, 웹툰

### 1. TMDB 영화

- API 정상 작동
- 요청: `GET https://api.themoviedb.org/3/movie/popular?language=ko-KR&page=1`
- 확인 결과: `results` 20개 반환, 제목/장르/포스터 경로 매핑 가능

### 2. TMDB 드라마

- API 정상 작동
- 요청: `GET https://api.themoviedb.org/3/tv/popular?language=ko-KR&page=1`
- 확인 결과: `results` 20개 반환, 제목/장르/포스터 경로 매핑 가능

### 3. Jikan 애니메이션

- API 정상 작동
- 요청: `GET https://api.jikan.moe/v4/top/anime`
- 확인 결과: `data` 25개 반환, 제목/장르/이미지 URL 매핑 가능

### 4. 알라딘 도서

- API 정상 작동
- 요청: `GET http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?...`
- 확인 결과: `item` 10개 반환, 제목/장르/커버 URL 매핑 가능

### 5. RAWG 게임

- 정상 작동 확인 실패
- 실패 원인: Windows PowerShell/Schannel 환경에서 `SSL/TLS connection failed` 발생
- 수정 필요 여부: 서버 Linux 환경 또는 다른 TLS 스택에서 재검증 필요

### 6. KOPIS 뮤지컬

- API 응답은 오지만 데이터 확인 실패
- 실패 원인: 요청 기간을 넓혀도 `<dbs/>` 빈 XML 반환
- 수정 필요 여부: 서비스키 권한, 날짜 범위, KOPIS 제공 데이터 조건 재확인 필요

### 7. 웹툰

- 테스트 미수행
- 실패 원인: 문서상 공식 호스팅 API가 아니라 직접 배포 또는 사용 가능한 인스턴스 확인이 필요함
- 수정 필요 여부: 사용할 korea-webtoon-api 인스턴스 URL 결정 필요
