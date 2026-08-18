from pydantic import BaseModel, Field


class StockHistoryResponse(BaseModel):
    date: str = Field(
        ...,
        description="Trading date",
    )

    open: float = Field(
        ...,
        description="Opening price",
    )

    high: float = Field(
        ...,
        description="Highest price",
    )

    low: float = Field(
        ...,
        description="Lowest price",
    )

    close: float = Field(
        ...,
        description="Closing price",
    )

    volume: int = Field(
        ...,
        description="Trading volume",
    )