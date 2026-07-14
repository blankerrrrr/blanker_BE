import asyncio
import io

import pytesseract
from PIL import Image

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException


async def extract_text(image_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text: str = await asyncio.to_thread(
            pytesseract.image_to_string,
            image,
            lang="kor+eng",
        )
        return text.strip()
    except AppException:
        raise
    except Exception as exc:
        raise AppException(ErrorCode.OCR_FAILED) from exc
