from app.schemas.common import CamelModel


class WebSearchResultResponse(CamelModel):
    title: str
    url: str
    description: str


class WebSearchResponse(CamelModel):
    query: str
    results: list[WebSearchResultResponse]
