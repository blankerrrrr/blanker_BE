from fastapi import APIRouter

from app.api import (
    analysis_requests,
    auth,
    block_settings,
    blocked_items,
    interest_items,
    interest_targets,
    interests,
    screenshot_analysis_requests,
    web_search,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    interests.router,
    prefix="/interests",
    tags=["interests"],
)
api_router.include_router(
    interest_targets.router,
    prefix="/interest-targets",
    tags=["interest-targets"],
)
api_router.include_router(
    block_settings.router,
    prefix="/block-settings",
    tags=["block-settings"],
)
api_router.include_router(
    analysis_requests.router,
    prefix="/analyses",
    tags=["analyses"],
)
api_router.include_router(
    blocked_items.router,
    prefix="/blocked-items",
    tags=["blocked-items"],
)
api_router.include_router(
    interest_items.router,
    prefix="/interest-items",
    tags=["interest-items"],
)
api_router.include_router(
    screenshot_analysis_requests.router,
    prefix="/analyses/screenshot",
    tags=["analyses"],
)
api_router.include_router(
    web_search.router,
    prefix="/web-search",
    tags=["web-search"],
)
