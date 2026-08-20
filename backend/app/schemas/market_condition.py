from pydantic import BaseModel, Field


class MarketConditionResponse(BaseModel):

    market: str = Field(
        ...,
        description="Market benchmark",
    )

    period: str = Field(
        ...,
        description="Historical data period",
    )

    current_price: float | None = Field(
        None,
        description="Current market index price",
    )

    sma_20: float | None = Field(
        None,
        description="20-period simple moving average",
    )

    ema_20: float | None = Field(
        None,
        description="20-period exponential moving average",
    )

    return_percentage: float | None = Field(
        None,
        description="Market return percentage",
    )

    trend: str = Field(
        ...,
        description="Overall market trend",
    )

    market_strength: float | None = Field(
        None,
        description="Market strength score from 0 to 100",
    )