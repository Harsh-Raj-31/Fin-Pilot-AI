from pydantic import BaseModel, Field


class StockSignalResponse(BaseModel):

    symbol: str = Field(
        ...,
        description="Stock symbol",
    )

    period: str = Field(
        ...,
        description="Analysis period",
    )

    stock_score: float | None = Field(
        None,
        description="Overall stock score from 0 to 100",
    )

    market_trend: str = Field(
        ...,
        description="Overall market trend",
    )

    market_strength: float | None = Field(
        None,
        description="Market strength from 0 to 100",
    )

    signal: str = Field(
        ...,
        description="Current decision signal",
    )

    confidence: float | None = Field(
        None,
        description="Decision confidence from 0 to 100",
    )