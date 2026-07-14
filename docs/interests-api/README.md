## 관심사 분류
- 영화
- 애니메이션
- 소설
- 드라마
- 게임
- 웹툰
- 뮤지컬
- 기타

## 관심사 분류(기타 제외 7개)에 대한 API

- 필요한 필드: 제목, 장르, 이미지 URL, 

| 카테고리     | 추천 API            | 키 발급      | 한국 커버리지   | 상세 문서                                    |
|----------|-------------------|-----------|-----------|------------------------------------------|
| 영화 (+장르) | TMDB              | 필요(무료)    | 좋음(한글 O)  | [MOVIE-and-DRAMA.md](MOVIE-and-DRAMA.md) |
| 드라마      | TMDB (TV)         | 필요(무료)    | 좋음        | [MOVIE-and-DRAMA.md](MOVIE-and-DRAMA.md) |
| 애니메이션    | Jikan / AniList   | 불필요 / 불필요 | 보통(일본 중심) | [ANIME.md](ANIME.md)                     |
| 게임       | RAWG              | 필요(무료)    | 글로벌       | [GAME.md](GAME.md)                       |
| 소설(도서)   | 알라딘 / 네이버 책       | 필요(무료)    | 우수        | [BOOK.md](BOOK.md)                       |
| 웹툰       | korea-webtoon-api | 불필요       | 국내 특화     | [WEBTOON.md](WEBTOON.md)                 |
| 뮤지컬      | KOPIS             | 필요(무료)    | 국내 특화     | [MUSICAL.md](MUSICAL.md)                 |

## 이미지 URL 필드에 대해서

[image.md](image.md)

## 일괄 수집 동작

`scripts.import_interests --limit 50`은 DB에 이미 존재하는 `관심사 분류 + 작품명`을 제외하고 분류별 신규 작품을 최대 50개 수집한다. 한 페이지의 결과가 중복이면 다음 페이지를 조회하며, 영화·드라마·애니메이션은 TMDB에서 각각 최대 50개씩 수집한다.
