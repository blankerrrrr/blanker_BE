from pydantic import BaseModel, Field


class PageRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)


class PageResponse[T](BaseModel):
    items: list[T]
    page: int
    size: int
    total_elements: int = Field(serialization_alias="totalElements")
    total_pages: int = Field(serialization_alias="totalPages")
