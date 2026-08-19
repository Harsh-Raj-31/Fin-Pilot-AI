from pydantic import BaseModel, Field


class StockComparisonItem(BaseModel):
    symbol: str = Field(
        ...,
        description="Stock symbol",
    )

    return_percentage: float | None = Field(
        None,
        description="Percentage return during the selected period",
    )

    rsi_14: float | None = Field(
        None,
        description="14-period Relative Strength Index",
    )

    volatility: float | None = Field(
        None,
        description="Historical daily volatility percentage",
    )

    maximum_drawdown: float | None = Field(
        None,
        description="Maximum percentage decline from a previous peak",
    )

    risk_score: float | None = Field(
        None,
        description="Overall risk score",
    )

    risk_level: str = Field(
        ...,
        description="Overall risk classification",
    )

    comparison_score: float | None = Field(
        None,
        description="Overall comparison score",
    )    


class StockComparisonResponse(BaseModel):
    period: str = Field(
        ...,
        description="Historical data period used for comparison",
    )

    stocks: list[StockComparisonItem] = Field(
        ...,
        description="Stocks being compared",
    )

    winner: str | None = Field(
        None,
        description="Stock with the stronger comparison score",
    )