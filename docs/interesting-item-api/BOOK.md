## 소설(도서) — 알라딘 Open API

베이스: `http://www.aladin.co.kr/ttb/api`
인증: 쿼리 `?ttbkey={TTB_KEY}`

```
# 도서 검색
GET /ItemSearch.aspx?ttbkey={KEY}&Query={검색어}&QueryType=Keyword&SearchTarget=Book&output=js&Version=20131101

# 도서 상세 (ItemId 또는 ISBN)
GET /ItemLookUp.aspx?ttbkey={KEY}&itemIdType=ISBN13&ItemId={isbn}&output=js&Version=20131101

# 신간/베스트셀러 리스트
GET /ItemList.aspx?ttbkey={KEY}&QueryType=Bestseller&SearchTarget=Book&output=js&Version=20131101
```

`output=js`로 JSON, `output=xml`로 XML을 받습니다. 국내 도서는 알라딘 커버리지가 좋아요.

**대안 — 네이버 책 API**
베이스: `https://openapi.naver.com/v1/search`
인증: 헤더 `X-Naver-Client-Id`, `X-Naver-Client-Secret`

```
GET /book.json?query={검색어}&display=10&start=1
```