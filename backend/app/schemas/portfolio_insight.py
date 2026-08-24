from pydantic import BaseModel


class PortfolioInsightResponse(BaseModel):
    summary: str
    risk_insight: str
    performance_insight: str
    diversification_insight: str
    recommendations: list[str]