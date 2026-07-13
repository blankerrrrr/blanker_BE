from typing import Any

from pydantic import BaseModel, ConfigDict


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda value: "".join(
            word.capitalize() if index else word
            for index, word in enumerate(value.split("_"))
        ),
        populate_by_name=True,
    )


class SuccessResponse(CamelModel):
    success: bool = True
    data: Any


class ErrorDetail(CamelModel):
    code: str
    message: str
    status: int


class ErrorResponse(CamelModel):
    success: bool = False
    error: ErrorDetail
    timestamp: str
