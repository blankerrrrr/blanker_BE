from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.response import success_response


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    register_exception_handlers(app)
    app.include_router(api_router, prefix="/api")

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, object]:
        return success_response({"status": "ok"})

    return app


app = create_app()
