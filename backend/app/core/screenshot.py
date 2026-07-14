from playwright.async_api import async_playwright

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException

DEFAULT_TIMEOUT_MS = 30_000


async def take_screenshot(url: str, timeout_ms: int = DEFAULT_TIMEOUT_MS) -> bytes:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                page = await browser.new_page()
                await page.goto(url, timeout=timeout_ms)
                return await page.screenshot(full_page=True)
            finally:
                await browser.close()
    except Exception as exc:
        raise AppException(ErrorCode.SCREENSHOT_FAILED) from exc
