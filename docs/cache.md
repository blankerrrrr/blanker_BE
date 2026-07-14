# Cache 적용 API

조회 빈도가 높고 사용자별 쓰기와 직접 연결되지 않는 카탈로그성 API에 cache-aside 기법을 적용한다.

| Endpoint | 캐시 Key namespace | TTL | 적용 사유 |
| --- | --- | --- | --- |
| `GET /api/interests` | `query:interests:list:{hash}` | 10분 | 온보딩 관심사 목록은 필터/검색 UI에서 반복 조회된다. |
| `GET /api/interests/types` | `query:interests:types:{hash}` | 10분 | 온보딩 첫 진입 시 반복 조회되는 관심사 종류 목록이다. |
| `GET /api/interests/genres` | `query:interests:genres:{hash}` | 10분 | 관심사 종류 선택 후 장르 필터 UI에서 반복 조회된다. |

## 동작 방식

1. Service가 요청 파라미터를 기준으로 캐시 key를 생성한다.
2. Redis에 캐시된 응답 DTO가 있으면 DB를 조회하지 않고 반환한다.
3. 캐시가 없거나 Redis 오류가 발생하면 DB를 조회한다.
4. DB 조회 결과를 Redis에 저장한 뒤 응답한다.

Redis 장애는 조회 API 실패로 전파하지 않고 DB 조회로 fallback한다.
