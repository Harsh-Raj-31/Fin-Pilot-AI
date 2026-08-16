from pydantic import BaseModel


class PortfolioAnalyticsResponse(BaseModel):
    total_invested: float
    total_current_value: float
    total_profit_loss: float
    profit_loss_percentage: float