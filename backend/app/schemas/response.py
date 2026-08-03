from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = Field(
        ...,
        description="Indicates whether the request was successful.",
    )

    message: str = Field(
        ...,
        description="Human-readable response message.",
    )

    data: T | None = Field(
        default=None,
        description="Response payload.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Stocks retrieved successfully.",
                "data": [],
            }
        }
    }