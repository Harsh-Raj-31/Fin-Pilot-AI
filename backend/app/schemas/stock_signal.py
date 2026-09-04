from pydantic import BaseModel, Field


class StockSignalResponse(BaseModel):

    symbol: str = Field(
        ...,
        description="Stock symbol",
        example="TCS",
    )

    period: str = Field(
        ...,
        description="Analysis period",
        example="3mo",
    )

    stock_score: float | None = Field(
        None,
        description="Overall stock score from 0 to 100",
        example=80.6,
    )

    market_trend: str = Field(
        ...,
        description="Overall market trend",
        example="BULLISH",
    )

    market_strength: float | None = Field(
        None,
        description="Market strength from 0 to 100",
        example=80,
    )

    signal: str = Field(
        ...,
        description="Current decision signal",
        example="BUY",
    )

    confidence: float | None = Field(
        None,
        description="Decision confidence from 0 to 100",
        example=84.3,
    )

    technical_reasoning: list[str] = Field(
        default_factory=list,
        description="Technical analysis reasoning",
    )

    risk_reasoning: list[str] = Field(
        default_factory=list,
        description="Risk analysis reasoning",
    )

    market_reasoning: list[str] = Field(
        default_factory=list,
        description="Market condition reasoning",
    )

    explanation: str = Field(
        ...,
        description="Overall explanation for the generated signal",
    )