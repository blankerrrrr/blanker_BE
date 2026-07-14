import os

import pytesseract

from app.core import ocr


def test_configure_tesseract_uses_settings(monkeypatch) -> None:
    monkeypatch.setattr(ocr.settings, "tesseract_cmd", r"C:\Tools\tesseract.exe")
    monkeypatch.setattr(ocr.settings, "tessdata_prefix", r"C:\Tools\tessdata")
    monkeypatch.delenv("TESSDATA_PREFIX", raising=False)

    ocr._configure_tesseract()

    assert pytesseract.pytesseract.tesseract_cmd == r"C:\Tools\tesseract.exe"
    assert os.environ["TESSDATA_PREFIX"] == r"C:\Tools\tessdata"


def test_configure_tesseract_uses_windows_default_paths(monkeypatch, tmp_path) -> None:
    tesseract_cmd = tmp_path / "tesseract.exe"
    tessdata_prefix = tmp_path / "tessdata"
    tesseract_cmd.write_text("")
    tessdata_prefix.mkdir()

    monkeypatch.setattr(ocr.settings, "tesseract_cmd", None)
    monkeypatch.setattr(ocr.settings, "tessdata_prefix", None)
    monkeypatch.setattr(ocr, "_WINDOWS_TESSERACT_CMD", tesseract_cmd)
    monkeypatch.setattr(ocr, "_WINDOWS_TESSDATA_PREFIX", tessdata_prefix)
    monkeypatch.delenv("TESSDATA_PREFIX", raising=False)

    ocr._configure_tesseract()

    assert pytesseract.pytesseract.tesseract_cmd == str(tesseract_cmd)
    assert os.environ["TESSDATA_PREFIX"] == str(tessdata_prefix)
