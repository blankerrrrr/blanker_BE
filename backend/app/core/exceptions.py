from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.error_codes import ErrorCode


# 비즈니스 Exception
class AppException(Exception):
    def __init__(self, error_code: ErrorCode) -> None:
        self.error_code = error_code
        self.message = error_code.message
        self.status_code = error_code.status_code


# 전역 핸들러
def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(
        request: Request,
        exc: AppException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": exc.error_code.code,
                "message": exc.message,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=ErrorCode.INVALID_REQUEST_BODY.status_code,
            content={
                "error_code": ErrorCode.INVALID_REQUEST_BODY.code,
                "message": ErrorCode.INVALID_REQUEST_BODY.message,
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=ErrorCode.INTERNAL_SERVER_ERROR.status_code,
            content={
                "error_code": ErrorCode.INTERNAL_SERVER_ERROR.code,
                "message": ErrorCode.INTERNAL_SERVER_ERROR.message,
            },
        )
