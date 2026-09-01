from pydantic import BaseModel


class PortfolioHoldingAnalytics(BaseModel):
    symbol: str
    quantity: float
    average_price: float
    current_price: float
    invested_amount: float
    current_value: float
    profit_loss: float
    profit_loss_percentage: float
    allocation_percentage: float
    risk_score: float
    risk_level: str


class PortfolioAnalyticsResponse(BaseModel):
    total_invested: float
    total_current_value: float
    total_profit_loss: float
    profit_loss_percentage: float

    holdings: list[PortfolioHoldingAnalytics]

    portfolio_risk_score: float | None
    portfolio_risk_level: str

    best_performer: str | None
    best_performer_return: float | None

    worst_performer: str | None
    worst_performer_return: float | None

    highest_risk_holding: str | None
    highest_risk_score: float | None
    highest_risk_level: str | None

    largest_holding: str | None
    largest_allocation: float | None

    diversification_level: str

    observations: list[str]