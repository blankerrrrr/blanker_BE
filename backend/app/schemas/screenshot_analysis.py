from app.schemas.analysis import (
    BlockActionResponse,
    BlockCategory,
    RelevanceLevel,
    RiskLevel,
)
from app.schemas.common import CamelModel


class ScreenshotAnalysisRequestCreate(CamelModel):
    url: str
    title: str | None = None


class ScreenshotAnalysisRequestResponse(CamelModel):
    analysis_request_id: str
    extracted_text: str
    categories: list[BlockCategory]
    risk_level: RiskLevel
    relevance_level: RelevanceLevel
    should_block: bool
    block_action: BlockActionResponse | None = None
