from pydantic import BaseModel, Field


class StockIndicatorsResponse(BaseModel):
    symbol: str = Field(
        ...,
        description="Stock symbol",
    )

    period: str = Field(
        ...,
        description="Historical data period",
    )

    sma_20: float | None = Field(
        None,
        description="20-period Simple Moving Average",
    )

    ema_20: float | None = Field(
        None,
        description="20-period Exponential Moving Average",
    )

    rsi_14: float | None = Field(
        None,
        description="14-period Relative Strength Index",
    )

    macd: float | None = Field(
        None,
        description="Moving Average Convergence Divergence",
    )

    macd_signal: float | None = Field(
        None,
        description="MACD signal line",
    )

    volatility: float | None = Field(
        None,
        description="Historical price volatility",
    )