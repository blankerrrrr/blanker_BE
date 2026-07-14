# 데이터 모델링

본 문서는 [feat.md](./feat.md)와 [api-spec/README.md](./api-spec/README.md)를 기준으로 MVP 구현에 필요한 데이터 모델을 정의한다.

## 1. 모델 요약

| 테이블                    | 설명                         | 주요 기능                 |
|------------------------|----------------------------|-----------------------|
| `users`                | 사용자 계정 정보                  | 회원가입, 로그인, 계정별 데이터 소유 |
| `interests`            | 온보딩에서 선택 가능한 관심사 카탈로그      | 종류/장르별 관심사 조회, 개인 관심사 저장 기준 |
| `interest_targets`     | 사용자가 등록한 관심 작품, 인물, 주제     | 관심 대상 설정, 관련도 판단      |
| `block_settings`       | 정보 유형별 차단 여부와 민감도          | 차단 유형 및 민감도 설정        |
| `analysis_requests`    | 웹페이지 분석 요청 단위              | 콘텐츠 분석 요청 이력          |
| `analysis_contents`    | 분석 요청에 포함된 개별 텍스트, 이미지, 영역 | 텍스트, 이미지, 영역 단위 분석    |
| `analysis_results`     | 콘텐츠별 분석 결과                 | 분류, 위험도, 관련도, 차단 사유   |
| `blocked_items`        | 사용자가 저장한 차단 콘텐츠            | 나중에 보기 보관함            |
| `interest_item_groups` | 중복 통합된 관심 정보 그룹            | 중복 콘텐츠 통합             |
| `interest_items`       | 자동 수집된 관심 정보 원본            | 관심 정보 자동 수집, 출처 관리    |

## 2. 공통 규칙

| 항목            | 규칙                                                                                          |
|---------------|---------------------------------------------------------------------------------------------|
| ID            | 외부 노출 ID는 내부 정수 PK를 그대로 노출하지 않고 `{model}_{id}` 형식의 Public ID를 사용한다. 예: `user_1`, `interest_target_1` |
| 시간            | 모든 시간은 UTC 기준 ISO-8601로 응답하고 DB에는 `timestamp with time zone` 사용을 권장한다.                      |
| 삭제            | MVP에서는 물리 삭제를 기본으로 하되, 사용자 데이터 추적이 필요한 테이블은 `deletedAt` 확장을 고려한다.                           |
| 배열 값          | `aliases`, `keywords`, `categories`, `relatedTopics`는 PostgreSQL `text[]` 또는 JSON 배열로 저장한다. |
| 소유권           | 사용자별 데이터는 반드시 `userId`를 통해 소유자를 검증한다.                                                       |
| Refresh Token | 클라이언트에는 HttpOnly Secure Cookie로 저장하고, 서버에는 검증용 hash를 Redis에만 저장한다.                          |

## 3. Enum 정의

| Enum                   | 값                                                           | 설명                          |
|------------------------|-------------------------------------------------------------|-----------------------------|
| `InterestType`         | `영화`, `드라마`, `애니메이션`, `소설`, `게임`, `뮤지컬`, `웹툰`, `기타` | 온보딩 관심사 종류                  |
| `InterestTargetType`   | `WORK`, `PERSON`, `TOPIC`                                   | 사용자 관심 대상 유형                |
| `BlockSettingCategory` | `SPOILER`, `HARMFUL`, `INTEREST`                            | 차단 설정 카테고리                  |
| `BlockCategory`        | `SPOILER`, `HARMFUL`, `INTEREST`                            | 분석 결과 및 보관함 차단 분류          |
| `Sensitivity`          | `LOW`, `MEDIUM`, `HIGH`                                     | 차단 민감도                      |
| `ContentUnitType`      | `TEXT`, `IMAGE`, `AREA`                                     | 분석 콘텐츠 단위 및 차단 액션 대상 단위    |
| `RiskLevel`            | `LOW`, `MEDIUM`, `HIGH`                                     | 콘텐츠 위험도                     |
| `RelevanceLevel`       | `LOW`, `MEDIUM`, `HIGH`                                     | 사용자 관심 대상과의 관련도             |

현재 구현은 DB native enum 타입을 사용하지 않고 문자열 컬럼에 enum 값을 저장한다. API 요청/응답에서는 Pydantic `StrEnum`으로 값을 검증한다.

## 4. 테이블 상세

### 4.1 `users`

| 컬럼              | 타입           | 제약               | 설명                                |
|-----------------|--------------|------------------|-----------------------------------|
| `id`            | integer      | PK               | 내부 식별자                             |
| `userId`        | varchar(64)  | UNIQUE           | 사용자 Public ID. 예: `user_1`          |
| `email`         | varchar(255) | UNIQUE, NOT NULL | 로그인 이메일                           |
| `passwordHash`  | varchar(255) | NOT NULL         | 해시된 비밀번호                          |
| `createdAt`     | timestamptz  | NOT NULL         | 가입 시각                             |
| `updatedAt`     | timestamptz  | NOT NULL         | 수정 시각                             |

### 4.2 `interests`

| 컬럼          | 타입           | 제약               | 설명                              |
|-------------|--------------|------------------|---------------------------------|
| `id`        | integer      | PK               | 내부 식별자                          |
| `interestId` | varchar(64)  | UNIQUE          | 관심사 Public ID. 예: `interest_1` |
| `interestType` | varchar(50) | NOT NULL       | 관심사 종류. 예: 영화, 드라마, 애니메이션, 소설 |
| `interestTypeImageUrl` | varchar(1000) | NULL | 관심사 종류 대표 이미지 URL |
| `title`     | varchar(200) | NOT NULL         | 관심사 제목                          |
| `genre`     | varchar(100) | NOT NULL         | 관심사 장르. 관심사 종류와 별도 분류 값        |
| `imageUrl`  | varchar(1000) | NULL            | 관심사 이미지 URL                     |
| `createdAt` | timestamptz  | NOT NULL         | 생성 시각                           |
| `updatedAt` | timestamptz  | NOT NULL         | 수정 시각                           |

| 인덱스 | 컬럼 | 설명 |
| --- | --- | --- |
| `ix_interests_interest_id` | `interestId` | Public ID 단건 조회 |
| `uk_interests_type_title_genre` | `interestType`, `title`, `genre` | 동일 종류/장르 내 관심사 중복 방지 |

### 4.3 `interest_targets`

| 컬럼          | 타입           | 제약                     | 설명                                    |
|-------------|--------------|------------------------|---------------------------------------|
| `id`        | integer      | PK                     | 내부 식별자                                |
| `interestTargetId` | varchar(64)  | UNIQUE                | 관심 대상 Public ID. 예: `interest_target_1` |
| `userId`    | varchar(64)  | FK, NOT NULL           | `users.userId`                         |
| `type`      | varchar(20)  | NOT NULL               | `WORK`, `PERSON`, `TOPIC`             |
| `name`      | varchar(200) | NOT NULL               | 관심 대상 대표 이름                           |
| `aliases`   | text[]       | NOT NULL, DEFAULT `[]` | 별칭 목록                                 |
| `keywords`  | text[]       | NOT NULL, DEFAULT `[]` | 관련 키워드 목록                             |
| `createdAt` | timestamptz  | NOT NULL               | 생성 시각                                 |
| `updatedAt` | timestamptz  | NOT NULL               | 수정 시각                                 |

| 인덱스                                  | 컬럼                       | 설명             |
|--------------------------------------|--------------------------|----------------|
| `idx_interest_targets_user_id`       | `userId`                 | 사용자별 관심 대상 조회  |
| `uk_interest_targets_user_name_type` | `userId`, `type`, `name` | 사용자 내 중복 등록 방지 |

### 4.4 `block_settings`

| 컬럼            | 타입          | 제약           | 설명                               |
|---------------|-------------|--------------|----------------------------------|
| `id`          | integer     | PK           | 내부 식별자                         |
| `blockSettingId` | varchar(64) | UNIQUE      | 차단 설정 Public ID. 예: `block_setting_1` |
| `userId`      | varchar(64) | FK, NOT NULL | `users.userId`                   |
| `category`    | varchar(20) | NOT NULL     | `SPOILER`, `HARMFUL`, `INTEREST` |
| `enabled`     | boolean     | NOT NULL     | 차단 활성화 여부                        |
| `sensitivity` | varchar(20) | NOT NULL     | `LOW`, `MEDIUM`, `HIGH`          |
| `createdAt`   | timestamptz | NOT NULL     | 생성 시각                            |
| `updatedAt`   | timestamptz | NOT NULL     | 수정 시각                            |

| 인덱스 | 컬럼 | 설명 |
| --- | --- | --- |
| `uk_block_settings_user_category` | `userId`, `category` | 사용자별 카테고리 설정 1개 유지 |

### 4.5 `analysis_requests`

| 컬럼          | 타입           | 제약           | 설명                                      |
|-------------|--------------|--------------|-----------------------------------------|
| `id`        | integer      | PK           | 내부 식별자                                 |
| `analysisRequestId` | varchar(64)  | UNIQUE      | 분석 요청 Public ID. 예: `analysis_request_1` |
| `userId`    | varchar(64)  | FK, NOT NULL | `users.userId`                          |
| `pageUrl`   | text         | NOT NULL     | 분석한 페이지 URL                             |
| `pageTitle` | varchar(500) | NULL         | 분석한 페이지 제목                              |
| `createdAt` | timestamptz  | NOT NULL     | 요청 시각                                   |

| 인덱스                                  | 컬럼                    | 설명            |
|--------------------------------------|-----------------------|---------------|
| `idx_analysis_requests_user_created` | `userId`, `createdAt` | 사용자별 분석 이력 조회 |

### 4.6 `analysis_contents`

| 컬럼                  | 타입           | 제약           | 설명                      |
|---------------------|--------------|--------------|-------------------------|
| `id`                | integer      | PK           | 내부 식별자                    |
| `analysisContentId` | varchar(64)  | UNIQUE       | 분석 콘텐츠 Public ID. 예: `analysis_content_1` |
| `analysisRequestId` | varchar(64)  | FK, NOT NULL | `analysis_requests.analysisRequestId` |
| `clientContentId`   | varchar(100) | NOT NULL     | 확장 클라이언트가 전달한 DOM 단위 ID |
| `unitType`          | varchar(20)  | NOT NULL     | `TEXT`, `IMAGE`, `AREA` |
| `text`              | text         | NULL         | 분석 대상 텍스트               |
| `imageUrl`          | text         | NULL         | 분석 대상 이미지 URL           |
| `altText`           | text         | NULL         | 이미지 대체 텍스트              |
| `contextText`       | text         | NULL         | 주변 문맥                   |
| `selector`          | text         | NULL         | 페이지 내 위치 식별자            |
| `createdAt`         | timestamptz  | NOT NULL     | 생성 시각                   |

| 인덱스                                      | 컬럼                                     | 설명                |
|------------------------------------------|----------------------------------------|-------------------|
| `uk_analysis_contents_request_client_id` | `analysisRequestId`, `clientContentId` | 요청 내 콘텐츠 ID 중복 방지 |

### 4.7 `analysis_results`

| 컬럼                  | 타입          | 제약                     | 설명                                       |
|---------------------|-------------|------------------------|------------------------------------------|
| `id`                | integer     | PK                     | 내부 식별자                                  |
| `analysisResultId` | varchar(64) | UNIQUE                | 분석 결과 Public ID. 예: `analysis_result_1` |
| `analysisContentId` | varchar(64) | FK, UNIQUE, NOT NULL   | `analysis_contents.analysisContentId`     |
| `categories`        | text[]      | NOT NULL, DEFAULT `[]` | `SPOILER`, `HARMFUL`, `INTEREST` 등 분류 결과 |
| `riskLevel`         | varchar(20) | NOT NULL               | 위험도                                      |
| `relevanceLevel`    | varchar(20) | NOT NULL               | 관련도                                      |
| `shouldBlock`       | boolean     | NOT NULL               | 차단 필요 여부                                 |
| `blockReason`       | text        | NULL                   | 사용자에게 표시할 차단 사유                          |
| `relatedTopics`     | text[]      | NOT NULL, DEFAULT `[]` | 관련 주제                                    |
| `createdAt`         | timestamptz | NOT NULL               | 생성 시각                                    |

| 인덱스                                 | 컬럼            | 설명        |
|-------------------------------------|---------------|-----------|
| `idx_analysis_results_should_block` | `shouldBlock` | 차단 대상 필터링 |

### 4.8 `blocked_items`

| 컬럼                 | 타입          | 제약                     | 설명                                      |
|--------------------|-------------|------------------------|-----------------------------------------|
| `id`               | integer     | PK                     | 내부 식별자                                  |
| `blockedItemId`    | varchar(64) | UNIQUE                | 보관함 항목 Public ID. 예: `blocked_item_1`   |
| `userId`           | varchar(64) | FK, NOT NULL           | `users.userId`                          |
| `analysisRequestId` | varchar(64) | NULL                  | 저장 근거가 된 분석 요청                          |
| `summary`          | text        | NOT NULL               | 차단 콘텐츠 요약                               |
| `categories`       | text[]      | NOT NULL, DEFAULT `[]` | 차단 유형 목록                                |
| `relatedTopics`    | text[]      | NOT NULL, DEFAULT `[]` | 관련 주제                                   |
| `sourceUrl`        | text        | NOT NULL               | 원본 링크                                   |
| `selector`         | text        | NULL                   | 페이지 내 발견 위치                             |
| `positionText`     | text        | NULL                   | 사람이 이해 가능한 위치 설명                        |
| `foundAt`          | timestamptz | NOT NULL               | 발견 시각                                   |
| `savedAt`          | timestamptz | NOT NULL               | 저장 시각                                   |

| 인덱스                             | 컬럼                    | 설명              |
|---------------------------------|-----------------------|-----------------|
| `idx_blocked_items_user_saved`  | `userId`, `savedAt`   | 보관함 최신순 조회      |
| `idx_blocked_items_user_source` | `userId`, `sourceUrl` | 같은 페이지 저장 항목 조회 |

### 4.9 `interest_item_groups`

| 컬럼                     | 타입           | 제약                     | 설명                                               |
|------------------------|--------------|------------------------|--------------------------------------------------|
| `id`                   | integer      | PK                     | 내부 식별자                                             |
| `groupId`              | varchar(64)  | UNIQUE                | 관심 정보 그룹 Public ID. 예: `interest_item_group_1` |
| `userId`               | varchar(64)  | FK, NOT NULL           | `users.userId`                                      |
| `representativeItemId` | varchar(64)  | NULL                  | 대표 관심 정보. `interest_items.interestItemId`          |
| `title`                | varchar(500) | NOT NULL               | 그룹 대표 제목                                         |
| `summary`              | text         | NOT NULL               | 그룹 대표 요약                                         |
| `relatedTopics`        | text[]       | NOT NULL, DEFAULT `[]` | 관련 주제                                            |
| `duplicateReason`      | text         | NULL                   | 중복 통합 판단 사유                                      |
| `sourceCount`          | integer      | NOT NULL, DEFAULT `0`  | 그룹 내 출처 수                                        |
| `createdAt`            | timestamptz  | NOT NULL               | 생성 시각                                            |
| `updatedAt`            | timestamptz  | NOT NULL               | 수정 시각                                            |

| 인덱스                                     | 컬럼                    | 설명              |
|-----------------------------------------|-----------------------|-----------------|
| `idx_interest_item_groups_user_updated` | `userId`, `updatedAt` | 관심 정보 피드 최신순 조회 |

### 4.10 `interest_items`

| 컬럼               | 타입           | 제약                     | 설명                                           |
|------------------|--------------|------------------------|----------------------------------------------|
| `id`             | integer      | PK                     | 내부 식별자                                      |
| `interestItemId` | varchar(64)  | UNIQUE                | 관심 정보 Public ID. 예: `interest_item_1`       |
| `userId`         | varchar(64)  | FK, NOT NULL           | `users.userId`                               |
| `groupId`        | varchar(64)  | FK, NOT NULL           | `interest_item_groups.groupId`               |
| `title`          | varchar(500) | NOT NULL               | 수집된 정보 제목                                    |
| `summary`        | text         | NOT NULL               | 수집된 정보 요약                                    |
| `contentText`    | text         | NULL                   | 수집된 원문 또는 핵심 본문                              |
| `relatedTopics`  | text[]       | NOT NULL, DEFAULT `[]` | 관련 주제                                        |
| `sourceUrl`      | text         | NOT NULL               | 원본 링크                                        |
| `selector`       | text         | NULL                   | 페이지 내 위치                                     |
| `duplicateScore` | numeric(5,4) | NULL                   | 대표 그룹과의 중복 유사도                               |
| `discoveredAt`   | timestamptz  | NOT NULL               | 발견 시각                                        |
| `createdAt`      | timestamptz  | NOT NULL               | 저장 시각                                        |

| 인덱스                                  | 컬럼                       | 설명                      |
|--------------------------------------|--------------------------|-------------------------|
| `idx_interest_items_user_discovered` | `userId`, `discoveredAt` | 사용자별 관심 정보 최신순 조회       |
| `idx_interest_items_group_id`        | `groupId`                | 그룹 상세 출처 조회             |
| `uk_interest_items_user_source`      | `userId`, `sourceUrl`    | 동일 사용자의 동일 URL 중복 저장 방지 |

## 5. Redis 데이터

Refresh token 원문은 클라이언트의 HttpOnly Secure Cookie에 저장한다. 서버는 refresh token 원문을 영속 DB에 저장하지 않고, 검증용 hash만 Redis에 저장한다. 토큰 재발급 시 서버는 Cookie로 전달된 refresh token을 해시한 뒤 Redis 저장값과 비교한다.

| Key                               | Type   | TTL                     | Value              | 용도                         |
|-----------------------------------|--------|-------------------------|--------------------|----------------------------|
| `auth:refresh:{userId}:{tokenId}` | string | refresh token 만료 시간과 동일 | refresh token hash | 토큰 재발급 검증                  |
| `auth:user-sessions:{userId}`     | set    | refresh token 최대 만료 시간  | tokenId 목록         | 로그아웃, 전체 세션 만료, 사용자별 세션 관리 |

| 동작      | 처리                                                                                                                   |
|---------|----------------------------------------------------------------------------------------------------------------------|
| 로그인     | refresh token 생성 후 원문은 `Set-Cookie`로 내려주고, hash는 `auth:refresh:{userId}:{tokenId}`에 저장하며 tokenId를 사용자 세션 set에 추가한다.  |
| 토큰 재발급  | Cookie의 refresh token을 해시해 Redis 저장값과 비교하고, 유효하면 새 access token과 refresh token을 발급한다. 새 refresh token도 Cookie로 갱신한다. |
| 로그아웃    | 해당 `auth:refresh:{userId}:{tokenId}`를 삭제하고 사용자 세션 set에서 tokenId를 제거한 뒤 refresh token Cookie를 만료시킨다.                  |
| 전체 로그아웃 | `auth:user-sessions:{userId}`의 tokenId를 순회해 refresh token key를 삭제한다.                                                 |
| 만료      | Redis TTL 만료로 자동 폐기한다.                                                                                               |

| Cookie 속성  | 값                   | 설명                        |
|------------|---------------------|---------------------------|
| `Name`     | `refreshToken`      | refresh token Cookie 이름   |
| `HttpOnly` | `true`              | JavaScript에서 접근하지 못하도록 제한 |
| `Secure`   | `true`              | HTTPS 환경에서만 전송            |
| `SameSite` | `Lax` 또는 `None`     | 확장 프로그램/배포 도메인 구조에 따라 결정  |
| `Path`     | `/api/auth`         | 인증 API로 전송 범위 제한          |
| `Max-Age`  | refresh token 만료 시간 | Redis TTL과 동일하게 관리        |

## 6. 관계 요약

| 관계                                        | 카디널리티 | 설명                         |
|-------------------------------------------|-------|----------------------------|
| `users` - `interest_targets`              | 1:N   | 한 사용자는 여러 관심 대상을 등록할 수 있다. |
| `interests` - `interest_targets`          | 선택 복사 | 온보딩 관심사를 선택하면 사용자 개인 관심사로 저장한다. |
| `users` - `block_settings`                | 1:N   | 한 사용자는 차단 유형별 설정을 가진다.     |
| `users` - `analysis_requests`             | 1:N   | 분석 요청은 사용자에게 귀속된다.         |
| `analysis_requests` - `analysis_contents` | 1:N   | 한 분석 요청은 여러 콘텐츠 단위를 포함한다.  |
| `analysis_contents` - `analysis_results`  | 1:1   | 각 콘텐츠 단위는 하나의 분석 결과를 가진다.  |
| `users` - `blocked_items`                 | 1:N   | 보관함 항목은 사용자에게 귀속된다.        |
| `analysis_requests` - `blocked_items`     | 1:N   | 하나의 분석 요청이 저장 근거가 될 수 있다.  |
| `users` - `interest_item_groups`          | 1:N   | 중복 통합 그룹은 사용자별로 관리된다.      |
| `interest_item_groups` - `interest_items` | 1:N   | 한 그룹은 여러 출처 관심 정보를 포함한다.   |
