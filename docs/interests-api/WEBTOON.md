## 웹툰 — 만화규장각 Open API (한국만화영상진흥원, 공식)

> 공식 공공 Open API. 도서·유통·웹툰 정보 제공. 무료.
> 실명인증 회원가입 → 인증키 신청 → 관리자 승인(영업일 24h 내) 후 사용.
> 활용기간: 승인일로부터 12개월. 일일 트래픽: 1,000회.
> 특이점: 웹툰뿐 아니라 도서·영화·드라마·게임·공연까지 listSeCd로 구분 조회 가능.

베이스: https://www.kmas.or.kr/openapi
인증: 쿼리 파라미터 prvKey

# 목록 조회 (웹툰은 listSeCd=1)
GET https://www.kmas.or.kr/openapi/search/dcmtDtaList?prvKey={KEY}&listSeCd=1&pageNo=0&viewItemCnt=10

# 도서·웹툰 조회 (제목/ISBN 기반)
GET https://www.kmas.or.kr/openapi/search/bookAndWebtoonList?prvKey={KEY}&title={제목}&isbn={isbn}

예시: https://www.kmas.or.kr/openapi/search/dcmtDtaList?prvKey=발급키&listSeCd=1&pageNo=0
---

## 웹툰 — korea-webtoon-api 내부 컨테이너

> 외부 Heroku 호스팅 API에 직접 의존하지 않고 Docker Compose 내부 서비스로 실행한다.

공식 호스팅 API가 아니라 오픈소스 프로젝트를 사용합니다.

Base: `https://github.com/HyeokjaeLee/korea-webtoon-api`

Compose 내부 Base URL: `http://webtoon-api:3000`

```
# 웹툰 목록/검색
GET /webtoons?keyword={검색어}&page={n}&perPage={n}&provider={플랫폼}
```

정확한 스펙과 현재 사용 가능한 엔드포인트는 프로젝트의 Swagger 문서에서 확인해야 합니다. 공식 상용 API가 아니므로 컨테이너 빌드와 런타임 상태를 배포 환경에서 함께 관리해야 합니다.
