import asyncio
import io
import os
from pathlib import Path

import pytesseract
from PIL import Image

from app.core.config import settings
from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException

_WINDOWS_TESSERACT_CMD = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
_WINDOWS_TESSDATA_PREFIX = Path(r"C:\Program Files\Tesseract-OCR\tessdata")


def _configure_tesseract() -> None:
    tesseract_cmd = settings.tesseract_cmd
    if tesseract_cmd is None and _WINDOWS_TESSERACT_CMD.exists():
        tesseract_cmd = str(_WINDOWS_TESSERACT_CMD)

    if tesseract_cmd is not None:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    tessdata_prefix = settings.tessdata_prefix
    if tessdata_prefix is None and _WINDOWS_TESSDATA_PREFIX.exists():
        tessdata_prefix = str(_WINDOWS_TESSDATA_PREFIX)

    if tessdata_prefix is not None:
        os.environ.setdefault("TESSDATA_PREFIX", tessdata_prefix)


async def extract_text(image_bytes: bytes) -> str:
    try:
        _configure_tesseract()
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
