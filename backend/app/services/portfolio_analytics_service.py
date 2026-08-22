from fastapi import HTTPException, status

from app.repositories.portfolio_repository import PortfolioRepository
from app.services.market_data_service import MarketDataService
from app.services.stock_service import StockService


class PortfolioAnalyticsService:

    def __init__(self):
        self.portfolio_repository = PortfolioRepository()
        self.market_data_service = MarketDataService()
        self.stock_service = StockService()

    def calculate_portfolio_analytics(
        self,
        user_id: str,
    ) -> dict:

        portfolios = (
            self.portfolio_repository.get_by_user_id(
                user_id
            )
        )

        total_invested = 0
        total_current_value = 0
        holdings = []

        # Calculate analytics for every holding
        for portfolio in portfolios:

            quantity = portfolio["quantity"]
            average_price = portfolio["average_price"]
            symbol = portfolio["symbol"]

            try:
                # Discover the stock if it does not
                # already exist in the database.
                self.stock_service._get_or_discover_stock(
                    symbol
                )

                # Get the latest valid market price.
                current_price = (
                    self.market_data_service.get_current_price(
                        symbol
                    )
                )

                # Get stock risk information.
                risk_data = (
                    self.market_data_service.get_stock_risk(
                        symbol,
                        "3mo",
                    )
                )

            except RuntimeError as e:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=str(e),
                )

            # Calculate invested amount.
            invested_amount = (
                quantity * average_price
            )

            # Calculate current market value.
            current_value = (
                quantity * current_price
            )

            # Calculate profit or loss.
            profit_loss = (
                current_value - invested_amount
            )

            # Calculate holding return percentage.
            if invested_amount > 0:
                profit_loss_percentage = (
                    profit_loss / invested_amount
                ) * 100
            else:
                profit_loss_percentage = 0

            # Store holding-level analytics.
            holdings.append(
                {
                    "symbol": symbol,
                    "quantity": quantity,
                    "average_price": average_price,
                    "current_price": current_price,
                    "invested_amount": invested_amount,
                    "current_value": current_value,
                    "profit_loss": profit_loss,
                    "profit_loss_percentage": (
                        profit_loss_percentage
                    ),
                    "risk_score": risk_data["risk_score"],
                    "risk_level": risk_data["risk_level"],
                }
            )

            # Update portfolio totals.
            total_invested += invested_amount
            total_current_value += current_value

        # Calculate allocation percentage
        # for every holding.
        for holding in holdings:

            if total_invested > 0:
                holding["allocation_percentage"] = (
                    holding["invested_amount"]
                    / total_invested
                ) * 100
            else:
                holding["allocation_percentage"] = 0

        # Calculate weighted portfolio risk score.
        portfolio_risk_score = 0

        for holding in holdings:

            portfolio_risk_score += (
                holding["risk_score"]
                * holding["allocation_percentage"]
                / 100
            )

        # Determine portfolio risk level.
        if portfolio_risk_score < 30:
            portfolio_risk_level = "LOW"

        elif portfolio_risk_score < 60:
            portfolio_risk_level = "MEDIUM"

        elif portfolio_risk_score < 80:
            portfolio_risk_level = "HIGH"

        else:
            portfolio_risk_level = "VERY HIGH"

        # Determine portfolio summary.
        if holdings:

            # Best performer based on return percentage.
            best_holding = max(
                holdings,
                key=lambda holding: (
                    holding["profit_loss_percentage"]
                ),
            )

            # Worst performer based on return percentage.
            worst_holding = min(
                holdings,
                key=lambda holding: (
                    holding["profit_loss_percentage"]
                ),
            )

            # Largest holding based on allocation.
            largest_holding_data = max(
                holdings,
                key=lambda holding: (
                    holding["allocation_percentage"]
                ),
            )

            best_performer = (
                best_holding["symbol"]
            )

            worst_performer = (
                worst_holding["symbol"]
            )

            largest_holding = (
                largest_holding_data["symbol"]
            )

            largest_allocation = (
                largest_holding_data[
                    "allocation_percentage"
                ]
            )

            # Determine diversification level.
            if largest_allocation <= 40:
                diversification_level = (
                    "WELL DIVERSIFIED"
                )

            elif largest_allocation <= 60:
                diversification_level = (
                    "MODERATELY DIVERSIFIED"
                )

            else:
                diversification_level = (
                    "HIGHLY CONCENTRATED"
                )

        else:

            best_performer = None
            worst_performer = None
            largest_holding = None

            diversification_level = (
                "NOT AVAILABLE"
            )

        # Calculate total portfolio profit/loss.
        total_profit_loss = (
            total_current_value
            - total_invested
        )

        # Calculate total portfolio return.
        if total_invested > 0:
            profit_loss_percentage = (
                total_profit_loss
                / total_invested
            ) * 100
        else:
            profit_loss_percentage = 0

        return {
            "total_invested": total_invested,
            "total_current_value": total_current_value,
            "total_profit_loss": total_profit_loss,
            "profit_loss_percentage": (
                profit_loss_percentage
            ),
            "holdings": holdings,
            "portfolio_risk_score": round(
                portfolio_risk_score,
                2,
            ),
            "portfolio_risk_level": (
                portfolio_risk_level
            ),
            "best_performer": best_performer,
            "worst_performer": worst_performer,
            "largest_holding": largest_holding,
            "diversification_level": (
                diversification_level
            ),
        }
    