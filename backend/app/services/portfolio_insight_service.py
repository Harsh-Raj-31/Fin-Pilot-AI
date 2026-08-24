from app.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)


class PortfolioInsightService:

    def __init__(self):
        self.portfolio_analytics_service = (
            PortfolioAnalyticsService()
        )

    def generate_portfolio_insight(
        self,
        user_id: str,
    ) -> dict:

        analytics = (
            self.portfolio_analytics_service
            .calculate_portfolio_analytics(
                user_id
            )
        )

        total_invested = analytics[
            "total_invested"
        ]

        total_current_value = analytics[
            "total_current_value"
        ]

        total_profit_loss = analytics[
            "total_profit_loss"
        ]

        profit_loss_percentage = analytics[
            "profit_loss_percentage"
        ]

        portfolio_risk_score = analytics[
            "portfolio_risk_score"
        ]

        portfolio_risk_level = analytics[
            "portfolio_risk_level"
        ]

        best_performer = analytics[
            "best_performer"
        ]

        worst_performer = analytics[
            "worst_performer"
        ]

        largest_holding = analytics[
            "largest_holding"
        ]

        diversification_level = analytics[
            "diversification_level"
        ]

        # Generate overall summary

        summary = (
            f"Your portfolio has "
            f"₹{total_invested:,.2f} invested "
            f"with a current value of "
            f"₹{total_current_value:,.2f}. "
            f"The portfolio is currently showing "
            f"a profit/loss of "
            f"₹{total_profit_loss:,.2f}, "
            f"representing a return of "
            f"{profit_loss_percentage:.2f}%."
        )

        # Generate risk insight

        risk_insight = (
            f"Your portfolio has a "
            f"{portfolio_risk_level.lower()} "
            f"risk level with a risk score of "
            f"{portfolio_risk_score:.2f}."
        )

        # Generate performance insight

        performance_insight = (
            f"{best_performer} is currently your "
            f"best-performing holding, while "
            f"{worst_performer} is your "
            f"weakest-performing holding."
        )

        # Generate diversification insight

        diversification_insight = (
            f"Your portfolio is classified as "
            f"{diversification_level.lower()}. "
            f"{largest_holding} is currently your "
            f"largest holding based on invested "
            f"capital."
        )

        # Generate recommendations

        recommendations = []

        # Portfolio-level loss

        if profit_loss_percentage < 0:
            recommendations.append(
                f"Your portfolio is currently down "
                f"{abs(profit_loss_percentage):.2f}%. "
                f"Review the holdings contributing "
                f"most to the overall loss."
            )

        # Portfolio-level risk

        if portfolio_risk_level in [
            "HIGH",
            "VERY HIGH",
        ]:
            recommendations.append(
                "Your portfolio has elevated risk. "
                "Review your exposure to higher-risk "
                "holdings."
            )

        elif portfolio_risk_level == "MEDIUM":
            recommendations.append(
                "Your portfolio has a medium risk level. "
                "Continue monitoring the risk of "
                "individual holdings."
            )

        # Diversification

        if diversification_level == (
            "HIGHLY CONCENTRATED"
        ):
            recommendations.append(
                f"{largest_holding} represents a large "
                "portion of your portfolio. Consider "
                "reviewing this concentration."
            )

        elif diversification_level == (
            "MODERATELY DIVERSIFIED"
        ):
            recommendations.append(
                f"{largest_holding} is your largest "
                "holding. Monitor its impact on your "
                "overall portfolio."
            )

        # Worst performer

        if worst_performer:

            worst_holding = next(
                (
                    holding
                    for holding in analytics["holdings"]
                    if holding["symbol"]
                    == worst_performer
                ),
                None,
            )

            if worst_holding:

                worst_return = (
                    worst_holding[
                        "profit_loss_percentage"
                    ]
                )

                if worst_return < -30:
                    recommendations.append(
                        f"{worst_performer} is down "
                        f"{abs(worst_return):.2f}% "
                        "from its average purchase price. "
                        "Consider reviewing its performance."
                    )

                else:
                    recommendations.append(
                        f"Monitor {worst_performer} because "
                        "it is currently your weakest "
                        "performing holding."
                    )

        # Best performer

        if best_performer:

            best_holding = next(
                (
                    holding
                    for holding in analytics["holdings"]
                    if holding["symbol"]
                    == best_performer
                ),
                None,
            )

            if best_holding:

                best_return = (
                    best_holding[
                        "profit_loss_percentage"
                    ]
                )

                if best_return >= 0:

                    recommendations.append(
                        f"{best_performer} is currently your "
                        f"best-performing holding with a "
                        f"{best_return:.2f}% return."
                    )

                else:

                    recommendations.append(
                        f"{best_performer} is currently your "
                        f"best-performing holding, but it is "
                        f"still down {abs(best_return):.2f}% "
                        f"from its average purchase price."
                    )

        # Fallback recommendation

        if not recommendations:
            recommendations.append(
                "Continue monitoring portfolio "
                "performance, risk, and diversification."
            )

        return {
            "summary": summary,
            "risk_insight": risk_insight,
            "performance_insight": (
                performance_insight
            ),
            "diversification_insight": (
                diversification_insight
            ),
            "recommendations": recommendations,
        }