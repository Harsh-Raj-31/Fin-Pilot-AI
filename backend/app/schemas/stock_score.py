from pydantic import BaseModel, Field


class StockScoreResponse(BaseModel):

    symbol: str = Field(
        ...,
        description="Stock symbol",
    )

    period: str = Field(
        ...,
        description="Historical data period",
    )

    performance_score: float | None = Field(
        None,
        description="Performance score from 0 to 100",
    )

    technical_score: float | None = Field(
        None,
        description="Technical score from 0 to 100",
    )

    risk_score: float | None = Field(
        None,
        description="Risk score from 0 to 100",
    )

    overall_score: float | None = Field(
        None,
        description="Overall stock score from 0 to 100",
    )

    strength: str = Field(
        ...,
        description="Overall stock strength classification",
    )