## API 테스트 결과

### 요약

- 실패 및 수정이 필요한 API: 현재 8000 포트 서버의 `/api/analyses/screenshot`
- 코드 수정 완료: OCR 실행 환경 보정 로직 추가
- 재기동 후 확인 필요: 수정된 서버 프로세스에서 `/api/analyses/screenshot` 재호출

### 1. Tesseract 환경 확인

- `tesseract --version` 실행 성공: `tesseract v5.4.0.20240606`
- `tesseract --list-langs` 결과:
  - `eng`
  - `kor`
  - `osd`

### 2. 직접 OCR 확인

- 테스트 PNG 생성 후 직접 OCR 실행 성공
- 추출 텍스트:

```text
테 스 트 스 포 일 러 결 말 내 용

test spoiler ending text
```

### 3. POST /api/analyses/screenshot - 현재 8000 포트 서버

- 정상 작동 안함
- 응답: 500 Internal Server Error
- 에러 코드: `OCR_FAILED`
- 요청 형식: `multipart/form-data`
  - `url=https://example.com/screenshot-test-20260714`
  - `title=스크린샷 API 재테스트`
  - `image=@blanker-screenshot-api-test-20260714.png;type=image/png`

```json
{
  "error_code": "OCR_FAILED",
  "message": "텍스트 추출에 실패했습니다."
}
```

### 4. 수정 및 로컬 검증

- `backend/app/core/ocr.py`
  - `TESSERACT_CMD`, `TESSDATA_PREFIX` 설정값을 사용하도록 수정
  - 설정값이 없고 Windows 기본 설치 경로가 존재하면 자동으로 `C:\Program Files\Tesseract-OCR\tesseract.exe`, `C:\Program Files\Tesseract-OCR\tessdata`를 사용하도록 수정
- `backend/app/core/config.py`, `backend/.env.example`
  - OCR 경로 설정값 추가
- 테스트:

```text
.\.venv\Scripts\pytest.exe tests\unit\test_ocr.py tests\unit\test_analysis_api.py -q
9 passed
```

### 확인 내용

- 현재 8000 포트 서버 프로세스는 수정 전 코드 또는 수정 전 OCR 환경으로 실행 중이어서 API가 계속 실패함
- 수정된 코드의 OCR 함수는 테스트 이미지에서 Tesseract 호출까지 성공함
- 서버 재기동 후 `/api/analyses/screenshot` 재테스트가 필요함
