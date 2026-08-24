from app.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)


class PortfolioTool:

    def __init__(self):
        self.portfolio_analytics_service = (
            PortfolioAnalyticsService()
        )

    def get_portfolio_analytics(
        self,
        user_id: str,
    ) -> dict:

        return (
            self.portfolio_analytics_service
            .calculate_portfolio_analytics(
                user_id
            )
        )