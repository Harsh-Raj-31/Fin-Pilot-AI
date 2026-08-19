from pydantic import BaseModel, Field


class StockRiskResponse(BaseModel):
    symbol: str = Field(
        ...,
        description="Stock symbol",
    )

    period: str = Field(
        ...,
        description="Historical data period",
    )

    volatility: float | None = Field(
        None,
        description="Historical daily volatility percentage",
    )

    maximum_drawdown: float | None = Field(
        None,
        description="Maximum percentage decline from a previous peak",
    )

    return_percentage: float | None = Field(
        None,
        description="Percentage return during the selected period",
    )

    risk_score: float | None = Field(
        None,
        description="Calculated risk score",
    )

    risk_level: str = Field(
        ...,
        description="Overall risk classification",
    )