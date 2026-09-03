from pydantic import BaseModel, Field


class WatchlistCreate(BaseModel):
    symbol: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Stock symbol to add to the watchlist",
        example="TCS",
    )


class WatchlistItemResponse(BaseModel):
    symbol: str = Field(
        ...,
        description="Stock symbol",
    )

    company_name: str = Field(
        ...,
        description="Company name",
    )

    current_price: float | None = Field(
        None,
        description="Current market price",
    )

    daily_change: float | None = Field(
        None,
        description="Daily percentage change",
    )

    signal: str | None = Field(
        None,
        description="Current stock signal",
    )

    confidence: float | None = Field(
        None,
        description="Signal confidence from 0 to 100",
    )


class WatchlistActionResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Whether the operation succeeded",
    )

    message: str = Field(
        ...,
        description="Operation result message",
    )