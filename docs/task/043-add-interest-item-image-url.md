# 043. 관심 정보 응답 이미지 URL 추가

## 작업 개요
- 작업명: 관심 정보 상세/목록 조회 API response에 이미지 URL 추가
- 관련 TASK: `TASK.next.md`
- 관련 API/문서: `GET /api/interest-items`, `GET /api/interest-items/{interestItemId}`, `POST /api/interest-items`
- 커밋 메시지: `feat: 관심 정보 이미지 URL 응답 추가`

## 변경한 파일
- `backend/app/core/config.py`
- `backend/app/core/s3.py`
- `backend/app/db/models/interest_item.py`
- `backend/app/schemas/interest_item.py`
- `backend/app/services/interest_item_service.py`
- `backend/alembic/versions/20260714_0015_add_image_url_to_interest_items.py`
- `backend/tests/unit/test_camel_model.py`
- `backend/tests/unit/test_interest_item_service.py`
- `docs/api-spec/GET-api-interest-items.md`
- `docs/api-spec/GET-api-interest-items-interestItemId.md`
- `docs/api-spec/POST-api-interest-items.md`
- `docs/data-modeling.md`
- `docs/task/043-add-interest-item-image-url.md`

## 구체적인 구현 내용
- `interest_items.image_url` 컬럼을 추가했다.
- `POST /api/interest-items` 요청에 선택 필드 `imageUrl`을 추가했다.
- AWS 설정이 있으면 입력 이미지 URL을 읽어 `interest-items/{userId}/{interestItemId}/{filename}` 경로로 S3에 업로드하고, 업로드된 URL을 저장한다.
- AWS 설정이 없으면 로컬 개발을 위해 입력 이미지 URL을 그대로 저장한다.
- 목록/상세 조회 응답에 `imageUrl`을 포함하도록 변경했다.

## 검증 내용
- 실행 명령: `.\.venv\Scripts\pytest.exe tests\unit -q`
- 검증 결과: `58 passed`
- 실행 명령: `.\.venv\Scripts\ruff.exe check . --no-cache`
- 검증 결과: 통과
- 실행 명령: `.\.venv\Scripts\alembic.exe upgrade head`
- 검증 결과: `20260714_0014 -> 20260714_0015` 마이그레이션 성공
- API 확인: `POST /api/interest-items` 201 Created
- API 확인: `GET /api/interest-items`, `GET /api/interest-items/{interestItemId}`에서 S3 `imageUrl` 반환
