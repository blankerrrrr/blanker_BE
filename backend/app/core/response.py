from datetime import UTC, datetime
from typing import Any

from app.core.error_codes import ErrorCode


def success_response(data: Any) -> dict[str, Any]:
    return {"success": True, "data": data}


def error_response(
    code: ErrorCode | str,
    message: str,
    status_code: int,
) -> dict[str, Any]:
    return {
        "success": False,
        "error": {
            "code": str(code),
            "message": message,
            "status": status_code,
        },
        "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    }
