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

        # --------------------------------------------------
        # CALCULATE ANALYTICS FOR EVERY HOLDING
        # --------------------------------------------------

        for portfolio in portfolios:

            quantity = portfolio["quantity"]
            average_price = portfolio["average_price"]
            symbol = portfolio["symbol"]

            try:

                # Discover stock if it does not
                # already exist in the database.
                self.stock_service._get_or_discover_stock(
                    symbol
                )

                # Get latest valid market price.
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
                    status_code=(
                        status.HTTP_503_SERVICE_UNAVAILABLE
                    ),
                    detail=str(e),
                )

            # --------------------------------------------------
            # INVESTED AMOUNT
            # --------------------------------------------------

            invested_amount = (
                quantity * average_price
            )

            # --------------------------------------------------
            # CURRENT VALUE
            # --------------------------------------------------

            current_value = (
                quantity * current_price
            )

            # --------------------------------------------------
            # PROFIT / LOSS
            # --------------------------------------------------

            profit_loss = (
                current_value
                - invested_amount
            )

            # --------------------------------------------------
            # HOLDING RETURN %
            # --------------------------------------------------

            if invested_amount > 0:

                profit_loss_percentage = (
                    profit_loss
                    / invested_amount
                ) * 100

            else:

                profit_loss_percentage = 0

            # --------------------------------------------------
            # STORE HOLDING ANALYTICS
            # --------------------------------------------------

            holdings.append(
                {
                    "symbol": symbol,
                    "quantity": quantity,
                    "average_price": average_price,
                    "current_price": current_price,

                    "invested_amount":
                        invested_amount,

                    "current_value":
                        current_value,

                    "profit_loss":
                        profit_loss,

                    "profit_loss_percentage":
                        profit_loss_percentage,

                    "risk_score":
                        risk_data["risk_score"],

                    "risk_level":
                        risk_data["risk_level"],
                }
            )

            # --------------------------------------------------
            # UPDATE PORTFOLIO TOTALS
            # --------------------------------------------------

            total_invested += invested_amount
            total_current_value += current_value

        # --------------------------------------------------
        # EMPTY PORTFOLIO
        # --------------------------------------------------

        if not holdings:

            return {
                "total_invested": 0,
                "total_current_value": 0,
                "total_profit_loss": 0,
                "profit_loss_percentage": 0,

                "holdings": [],

                "portfolio_risk_score": None,
                "portfolio_risk_level":
                    "NOT AVAILABLE",

                "best_performer": None,
                "best_performer_return": None,

                "worst_performer": None,
                "worst_performer_return": None,

                "highest_risk_holding": None,
                "highest_risk_score": None,
                "highest_risk_level": None,

                "largest_holding": None,
                "largest_allocation": None,

                "diversification_level":
                    "NOT AVAILABLE",

                "observations": [
                    "Portfolio has no holdings.",
                    "Portfolio risk cannot be "
                    "calculated without holdings.",
                ],
            }

        # --------------------------------------------------
        # ALLOCATION PERCENTAGE
        # --------------------------------------------------

        for holding in holdings:

            if total_invested > 0:

                holding["allocation_percentage"] = (
                    holding["invested_amount"]
                    / total_invested
                ) * 100

            else:

                holding["allocation_percentage"] = 0

        # --------------------------------------------------
        # WEIGHTED PORTFOLIO RISK
        # --------------------------------------------------

        portfolio_risk_score = 0

        for holding in holdings:

            portfolio_risk_score += (
                holding["risk_score"]
                * holding["allocation_percentage"]
                / 100
            )

        portfolio_risk_score = round(
            portfolio_risk_score,
            2,
        )

        # --------------------------------------------------
        # PORTFOLIO RISK LEVEL
        # --------------------------------------------------

        if portfolio_risk_score < 30:

            portfolio_risk_level = "LOW"

        elif portfolio_risk_score < 60:

            portfolio_risk_level = "MEDIUM"

        elif portfolio_risk_score < 80:

            portfolio_risk_level = "HIGH"

        else:

            portfolio_risk_level = "VERY HIGH"

        # --------------------------------------------------
        # BEST PERFORMER
        # --------------------------------------------------

        best_holding = max(
            holdings,
            key=lambda holding:
                holding["profit_loss_percentage"],
        )

        best_performer = (
            best_holding["symbol"]
        )

        best_performer_return = (
            best_holding[
                "profit_loss_percentage"
            ]
        )

        # --------------------------------------------------
        # WORST PERFORMER
        # --------------------------------------------------

        worst_holding = min(
            holdings,
            key=lambda holding:
                holding["profit_loss_percentage"],
        )

        worst_performer = (
            worst_holding["symbol"]
        )

        worst_performer_return = (
            worst_holding[
                "profit_loss_percentage"
            ]
        )

        # --------------------------------------------------
        # HIGHEST RISK HOLDING
        # --------------------------------------------------

        highest_risk_holding_data = max(
            holdings,
            key=lambda holding:
                holding["risk_score"],
        )

        highest_risk_holding = (
            highest_risk_holding_data["symbol"]
        )

        highest_risk_score = (
            highest_risk_holding_data["risk_score"]
        )

        highest_risk_level = (
            highest_risk_holding_data["risk_level"]
        )

        # --------------------------------------------------
        # LARGEST HOLDING
        # --------------------------------------------------

        largest_holding_data = max(
            holdings,
            key=lambda holding:
                holding["allocation_percentage"],
        )

        largest_holding = (
            largest_holding_data["symbol"]
        )

        largest_allocation = (
            largest_holding_data[
                "allocation_percentage"
            ]
        )

        # --------------------------------------------------
        # DIVERSIFICATION
        # --------------------------------------------------

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

        # --------------------------------------------------
        # TOTAL PROFIT / LOSS
        # --------------------------------------------------

        total_profit_loss = (
            total_current_value
            - total_invested
        )

        # --------------------------------------------------
        # TOTAL PORTFOLIO RETURN
        # --------------------------------------------------

        if total_invested > 0:

            profit_loss_percentage = (
                total_profit_loss
                / total_invested
            ) * 100

        else:

            profit_loss_percentage = 0

        # --------------------------------------------------
        # PORTFOLIO OBSERVATIONS
        # --------------------------------------------------

        observations = []

        # Overall performance

        if profit_loss_percentage > 0:

            observations.append(
                "Portfolio is currently "
                f"profitable with a return of "
                f"{profit_loss_percentage:.2f}%."
            )

        elif profit_loss_percentage < 0:

            observations.append(
                "Portfolio is currently "
                f"underperforming with a return "
                f"of {profit_loss_percentage:.2f}%."
            )

        else:

            observations.append(
                "Portfolio is currently "
                "approximately at break-even."
            )

        # Best performer

        observations.append(
            f"{best_performer} is the best-performing "
            f"holding with a return of "
            f"{best_performer_return:.2f}%."
        )

        # Worst performer

        observations.append(
            f"{worst_performer} is the worst-performing "
            f"holding with a return of "
            f"{worst_performer_return:.2f}%."
        )

        # Highest risk

        observations.append(
            f"{highest_risk_holding} has the highest "
            f"risk score of {highest_risk_score:.1f} "
            f"({highest_risk_level})."
        )

        # Largest allocation

        observations.append(
            f"{largest_holding} represents the largest "
            f"portfolio allocation at "
            f"{largest_allocation:.2f}%."
        )

        # Concentration warning

        if largest_allocation > 60:

            observations.append(
                "Portfolio is highly concentrated "
                "in one holding."
            )

        elif largest_allocation > 40:

            observations.append(
                "Portfolio has a relatively high "
                "concentration in its largest holding."
            )

        else:

            observations.append(
                "Portfolio allocation is reasonably "
                "distributed across holdings."
            )

        # --------------------------------------------------
        # RETURN PORTFOLIO ANALYTICS
        # --------------------------------------------------

        return {

            "total_invested":
                total_invested,

            "total_current_value":
                total_current_value,

            "total_profit_loss":
                total_profit_loss,

            "profit_loss_percentage":
                profit_loss_percentage,

            "holdings":
                holdings,

            "portfolio_risk_score":
                portfolio_risk_score,

            "portfolio_risk_level":
                portfolio_risk_level,

            "best_performer":
                best_performer,

            "best_performer_return":
                best_performer_return,

            "worst_performer":
                worst_performer,

            "worst_performer_return":
                worst_performer_return,

            "highest_risk_holding":
                highest_risk_holding,

            "highest_risk_score":
                highest_risk_score,

            "highest_risk_level":
                highest_risk_level,

            "largest_holding":
                largest_holding,

            "largest_allocation":
                largest_allocation,

            "diversification_level":
                diversification_level,

            "observations":
                observations,
        }