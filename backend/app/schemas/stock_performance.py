from pydantic import BaseModel, Field


class StockPerformanceResponse(BaseModel):
    symbol: str = Field(
        ...,
        description="Stock symbol",
    )

    period: str = Field(
        ...,
        description="Performance period",
    )

    start_price: float = Field(
        ...,
        description="Price at the beginning of the period",
    )

    current_price: float = Field(
        ...,
        description="Latest closing price",
    )

    return_percentage: float = Field(
        ...,
        description="Percentage return during the period",
    )

    highest_price: float = Field(
        ...,
        description="Highest price during the period",
    )

    lowest_price: float = Field(
        ...,
        description="Lowest price during the period",
    )

    average_price: float = Field(
        ...,
        description="Average closing price during the period",
    )