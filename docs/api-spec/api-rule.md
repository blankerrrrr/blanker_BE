## 1. 기본 원칙

모든 API는 다음 원칙을 따른다.

- API는 리소스 중심으로 설계한다.
- 요청과 응답 형식은 일관되게 유지한다.

---

## 2. URL 규칙

### 기본 형식

```
/api/{resource}
```

예시:

```
/api/auth
```

### 규칙

- URL은 소문자와 하이픈을 사용한다.
- 리소스명은 복수형을 사용한다.
- 동사는 사용을 지향한다.

좋은 예:

```
GET /api/users
POST /api/auth/login
```

나쁜 예:

```
GET /api/getUser/1
POST /api/createNotice
```

---

## 3. 요청 규칙

### Header

공통 요청 헤더는 다음과 같다.

```
Content-Type: application/json
Trace-Id: {traceId}
```

| Header | 설명 |
| --- | --- |
| Content-Type | 요청 본문 타입 |
| Trace-Id | 요청 추적 ID |

---

## 4. ID 규칙

서비스별 리소스 ID는 접두사를 사용할 수 있다.

예시:

```
user_123
order_123
project_123
```

| 리소스 | 접두사 |
| --- | --- |
| User | user_ |
| Order | order_ |
| Project | project_ |

외부에 노출되는 ID는 내부 정수 PK를 그대로 노출하지 않고 `{model}_{id}` 형식의 Public ID를 사용한다.

---

## 5. Pagination 규칙

목록 조회 API는 기본적으로 페이지네이션을 지원한다.

요청 예시:

```
GET /api/notices?page=1&size=10
```

규칙:

- `page`는 1부터 시작한다.
- `size` 기본값은 10이다.
- 최대 `size`는 100으로 제한한다.

응답 예시:

```json
{
  "items": [],
  "page": 1,
  "size": 20,
  "totalElements": 100,
  "totalPages": 5
}
```

---

## 6. Sorting 규칙

정렬은 `sort` 파라미터를 사용한다.

```
GET /api/projects?sort=createdAt,desc
```

형식:

```
sort={field},{direction}
```

예시:

```
createdAt,desc
name,asc
```

---

## 7. 인증 및 인가 규칙

- 사용자 ID, 권한 정보를 헤더 또는 토큰에서 확인한다.
- 서비스 내부에서는 신뢰 가능한 인증 정보만 사용한다.

권장 헤더:

```
X-User-Id: user_123
X-User-Role: USER
```

단, 클라이언트가 직접 넣은 `X-User-Id`는 신뢰하지 않는다. 반드시 인증된 내부 시스템에서 추가해야 한다.

---

## 8. 이벤트 규칙

이벤트 이름은 과거형으로 작성한다.

좋은 예:

```
UserCreated
OrderPaid
ProjectDeleted
```

나쁜 예:

```
CreateUser
PayOrder
DeleteProject
```

이벤트 기본 형식:

```json
{
  "eventId": "event_123",
  "eventType": "UserCreated",
  "occurredAt": "2026-06-11T10:00:00Z",
  "source": "user-service",
  "data": {
    "userId": "user_123"
  }
}
```

---

## 9. 로깅 및 추적 규칙

모든 요청 로그에는 다음 값을 포함한다.

- traceId
- userId
- method
- path
- status
- elapsedTime

예시:

```
traceId=abc-123 method=GET path=/api/users/user_123 status=200 elapsed=32ms
```

---

## 10. API 문서화 규칙

각 서비스는 OpenAPI 문서를 제공한다. 해당 문서는 컨트롤러에 어노테이션을 붙여서 작성한다.

문서에는 다음 내용을 포함한다.

- API 설명
- 요청 파라미터
- 요청 바디
- 응답 예시
- 에러 코드
- 인증 필요 여부

---
## 11. 날짜 및 시간 포메팅

모든 시간은 UTC 기준 ISO-8601 형식을 사용한다.

```json
{
  "createdAt": "2026-06-11T10:00:00Z",
  "updatedAt": "2026-06-11T10:30:00Z"
}
```

서버 내부 저장은 `Instant` 사용을 권장한다.

---
## 12. 에러코드
에러 코드는 대문자 스네이크 케이스를 사용한다.

형식:

```
{DOMAIN}_{ERROR_REASON}
```

예시:

```
USER_NOT_FOUND
USER_ALREADY_EXISTS
ORDER_NOT_FOUND
ORDER_ALREADY_PAID
PROJECT_ACCESS_DENIED
INVALID_REQUEST_BODY
```

---
## 13. 응답 형식

- 반환 값은 항상 camelCase

### 성공 응답

```json
{
  "success": true,
  "data": {
    "id": "user_123",
    "name": "홍길동"
  }
}
```

### 목록 응답

```json
{
  "success": true,
  "data": {
    "items": [],
    "page": 1,
    "size": 20,
    "totalElements": 100,
    "totalPages": 5
  }
}
```

### 실패 응답

```json
{
  "error_code": "USER_NOT_FOUND",
  "message": "사용자를 찾을 수 없습니다."
}
```

---
## 14. 금지 사항

다음 행위는 금지한다.

- 다른 서비스의 DB 직접 조회
- URL에 동사 사용
- 서비스마다 다른 응답 형식 사용
- 에러 메시지만 반환하고 에러 코드 생략
- 실패 응답에 정의되지 않은 중첩 error 객체 사용
- 클라이언트가 보낸 사용자 ID를 그대로 신뢰
- API 버전 없이 운영 API 제공
- 내부 구현 Entity를 그대로 응답 DTO로 반환
