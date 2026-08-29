class PortfolioInsightEngine:

    @classmethod
    def generate(
        cls,
        analytics: dict,
    ) -> dict:

        warnings = []
        insights = []

        # --------------------------------------------------
        # EMPTY PORTFOLIO
        # --------------------------------------------------

        if not analytics.get("holdings"):

            return {
                "warnings": [
                    "Portfolio has no holdings."
                ],
                "insights": [
                    "Portfolio analysis is not available "
                    "without holdings."
                ],
            }

        # --------------------------------------------------
        # PORTFOLIO PERFORMANCE
        # --------------------------------------------------

        portfolio_return = (
            analytics["profit_loss_percentage"]
        )

        if portfolio_return < -20:

            warnings.append(
                "Portfolio has a significant negative "
                f"return of {portfolio_return:.2f}%."
            )

        elif portfolio_return < 0:

            warnings.append(
                "Portfolio is currently showing a "
                f"negative return of {portfolio_return:.2f}%."
            )

        elif portfolio_return > 20:

            insights.append(
                "Portfolio is currently showing a strong "
                f"positive return of {portfolio_return:.2f}%."
            )

        else:

            insights.append(
                "Portfolio is currently showing a "
                f"positive return of {portfolio_return:.2f}%."
            )

        # --------------------------------------------------
        # PORTFOLIO RISK
        # --------------------------------------------------

        risk_score = (
            analytics["portfolio_risk_score"]
        )

        risk_level = (
            analytics["portfolio_risk_level"]
        )

        if risk_score >= 60:

            warnings.append(
                "Portfolio has a high overall risk level "
                f"with a risk score of {risk_score:.2f}."
            )

        elif risk_score >= 30:

            insights.append(
                "Portfolio has a medium overall risk level "
                f"with a risk score of {risk_score:.2f}."
            )

        else:

            insights.append(
                "Portfolio has a low overall risk level "
                f"with a risk score of {risk_score:.2f}."
            )

        # --------------------------------------------------
        # HIGHEST RISK HOLDING
        # --------------------------------------------------

        highest_risk = (
            analytics["highest_risk_holding"]
        )

        highest_risk_score = (
            analytics["highest_risk_score"]
        )

        highest_risk_level = (
            analytics["highest_risk_level"]
        )

        if highest_risk_level in {
            "HIGH",
            "VERY HIGH",
        }:

            warnings.append(
                f"{highest_risk} has the highest risk "
                f"score of {highest_risk_score:.1f} "
                f"({highest_risk_level})."
            )

        else:

            insights.append(
                f"{highest_risk} has the highest risk "
                f"score of {highest_risk_score:.1f} "
                f"({highest_risk_level})."
            )

        # --------------------------------------------------
        # CONCENTRATION
        # --------------------------------------------------

        largest_holding = (
            analytics["largest_holding"]
        )

        largest_allocation = (
            analytics["largest_allocation"]
        )

        if largest_allocation > 60:

            warnings.append(
                f"{largest_holding} represents "
                f"{largest_allocation:.2f}% of the "
                "portfolio, indicating high concentration."
            )

        elif largest_allocation > 40:

            warnings.append(
                f"{largest_holding} represents "
                f"{largest_allocation:.2f}% of the "
                "portfolio, indicating relatively high "
                "concentration."
            )

        else:

            insights.append(
                f"{largest_holding} represents "
                f"{largest_allocation:.2f}% of the "
                "portfolio."
            )

        # --------------------------------------------------
        # BEST PERFORMER
        # --------------------------------------------------

        best_performer = (
            analytics["best_performer"]
        )

        best_return = (
            analytics["best_performer_return"]
        )

        insights.append(
            f"{best_performer} is the best-performing "
            f"holding with a return of "
            f"{best_return:.2f}%."
        )

        # --------------------------------------------------
        # WORST PERFORMER
        # --------------------------------------------------

        worst_performer = (
            analytics["worst_performer"]
        )

        worst_return = (
            analytics["worst_performer_return"]
        )

        if worst_return < -20:

            warnings.append(
                f"{worst_performer} is the worst-performing "
                f"holding with a return of "
                f"{worst_return:.2f}%."
            )

        else:

            insights.append(
                f"{worst_performer} is the worst-performing "
                f"holding with a return of "
                f"{worst_return:.2f}%."
            )

        # --------------------------------------------------
        # DIVERSIFICATION
        # --------------------------------------------------

        diversification = (
            analytics["diversification_level"]
        )

        if diversification == "HIGHLY CONCENTRATED":

            warnings.append(
                "Portfolio diversification is limited "
                "because one holding represents more than "
                "60% of invested capital."
            )

        elif diversification == (
            "MODERATELY DIVERSIFIED"
        ):

            insights.append(
                "Portfolio is moderately diversified, "
                "but its largest holding has a relatively "
                "high allocation."
            )

        else:

            insights.append(
                "Portfolio allocation is reasonably "
                "distributed across holdings."
            )

        # --------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------

        return {
            "warnings": warnings,
            "insights": insights,
        }