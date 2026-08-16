from app.repositories.portfolio_repository import PortfolioRepository


class PortfolioAnalyticsService:

    def __init__(self):
        self.portfolio_repository = PortfolioRepository()

    def calculate_portfolio_analytics(
        self,
        user_id: str,
    ) -> dict:

        portfolios = self.portfolio_repository.get_by_user_id(user_id)

        total_invested = 0
        total_current_value = 0

        for portfolio in portfolios:

            quantity = portfolio["quantity"]
            average_price = portfolio["average_price"]

            # Temporary current price
            current_price = average_price
            invested_amount = quantity * average_price
            current_value = quantity * current_price

            total_invested += invested_amount
            total_current_value += current_value

        total_profit_loss = (
            total_current_value - total_invested
        )

        if total_invested > 0:
            profit_loss_percentage = (
                total_profit_loss / total_invested
            ) * 100
        else:
            profit_loss_percentage = 0

        return {
            "total_invested": total_invested,
            "total_current_value": total_current_value,
            "total_profit_loss": total_profit_loss,
            "profit_loss_percentage": profit_loss_percentage,
        }