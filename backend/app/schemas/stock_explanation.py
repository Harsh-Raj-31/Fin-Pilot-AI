from pydantic import BaseModel, Field


class StockExplanationResponse(BaseModel):

    symbol: str = Field(
        ...,
        description="Stock symbol",
    )

    period: str = Field(
        ...,
        description="Analysis period",
    )

    signal: str = Field(
        ...,
        description="Current stock signal",
    )

    confidence: float | None = Field(
        None,
        description="Signal confidence from 0 to 100",
    )

    summary: str = Field(
        ...,
        description="Short explanation of the current signal",
    )

    reasons: list[str] = Field(
        ...,
        description="Reasons supporting the signal",
    )