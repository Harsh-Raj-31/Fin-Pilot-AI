class PortfolioDecisionEngine:

    @classmethod
    def analyze(
        cls,
        analytics: dict,
    ) -> dict:

        attention_areas = []
        positive_areas = []

        holdings = analytics.get(
            "holdings",
            []
        )

        # --------------------------------------------------
        # EMPTY PORTFOLIO
        # --------------------------------------------------

        if not holdings:

            return {
                "overall_assessment": (
                    "Portfolio decision support is "
                    "not available because there are "
                    "no holdings."
                ),
                "attention_areas": [],
                "positive_areas": [],
            }

        # --------------------------------------------------
        # PORTFOLIO RETURN
        # --------------------------------------------------

        portfolio_return = (
            analytics.get(
                "profit_loss_percentage",
                0,
            )
        )

        if portfolio_return < -20:

            attention_areas.append(
                "Portfolio return is significantly "
                f"negative at {portfolio_return:.2f}%."
            )

        elif portfolio_return < 0:

            attention_areas.append(
                "Portfolio is currently showing a "
                f"negative return of "
                f"{portfolio_return:.2f}%."
            )

        elif portfolio_return > 0:

            positive_areas.append(
                "Portfolio is currently showing a "
                f"positive return of "
                f"{portfolio_return:.2f}%."
            )

        else:

            positive_areas.append(
                "Portfolio is currently at break-even."
            )

        # --------------------------------------------------
        # PORTFOLIO RISK
        # --------------------------------------------------

        risk_score = (
            analytics.get(
                "portfolio_risk_score",
                0,
            )
        )

        risk_level = (
            analytics.get(
                "portfolio_risk_level",
                "NOT AVAILABLE",
            )
        )

        if risk_level in {
            "HIGH",
            "VERY HIGH",
        }:

            attention_areas.append(
                "Overall portfolio risk is "
                f"{risk_level} with a risk score "
                f"of {risk_score:.2f}."
            )

        elif risk_level == "MEDIUM":

            attention_areas.append(
                "Overall portfolio risk is MEDIUM "
                f"with a risk score of "
                f"{risk_score:.2f}."
            )

        elif risk_level == "LOW":

            positive_areas.append(
                "Overall portfolio risk is LOW "
                f"with a risk score of "
                f"{risk_score:.2f}."
            )

        # --------------------------------------------------
        # HIGHEST-RISK HOLDING
        # --------------------------------------------------

        highest_risk_holding = (
            analytics.get(
                "highest_risk_holding"
            )
        )

        highest_risk_score = (
            analytics.get(
                "highest_risk_score",
                0,
            )
        )

        highest_risk_level = (
            analytics.get(
                "highest_risk_level",
                "NOT AVAILABLE",
            )
        )

        if highest_risk_holding:

            if highest_risk_level in {
                "HIGH",
                "VERY HIGH",
            }:

                attention_areas.append(
                    f"{highest_risk_holding} is the "
                    "highest-risk holding with a "
                    f"risk score of "
                    f"{highest_risk_score:.1f} "
                    f"({highest_risk_level})."
                )

            else:

                positive_areas.append(
                    f"{highest_risk_holding} has the "
                    "highest holding-level risk score "
                    f"of {highest_risk_score:.1f} "
                    f"({highest_risk_level})."
                )

        # --------------------------------------------------
        # LARGEST HOLDING / CONCENTRATION
        # --------------------------------------------------

        largest_holding = (
            analytics.get(
                "largest_holding"
            )
        )

        largest_allocation = (
            analytics.get(
                "largest_allocation",
                0,
            )
        )

        if largest_holding:

            if largest_allocation > 60:

                attention_areas.append(
                    f"{largest_holding} represents "
                    f"{largest_allocation:.2f}% of the "
                    "portfolio, indicating high "
                    "concentration."
                )

            elif largest_allocation > 40:

                attention_areas.append(
                    f"{largest_holding} represents "
                    f"{largest_allocation:.2f}% of the "
                    "portfolio, indicating relatively "
                    "high concentration."
                )

            else:

                positive_areas.append(
                    f"The largest holding, "
                    f"{largest_holding}, represents "
                    f"{largest_allocation:.2f}% of the "
                    "portfolio."
                )

        # --------------------------------------------------
        # DIVERSIFICATION
        # --------------------------------------------------

        diversification = (
            analytics.get(
                "diversification_level",
                "NOT AVAILABLE",
            )
        )

        if diversification == (
            "HIGHLY CONCENTRATED"
        ):

            attention_areas.append(
                "Portfolio diversification is limited "
                "because one holding represents more "
                "than 60% of invested capital."
            )

        elif diversification == (
            "MODERATELY DIVERSIFIED"
        ):

            attention_areas.append(
                "Portfolio is moderately diversified "
                "but has a relatively high allocation "
                "to its largest holding."
            )

        elif diversification == (
            "WELL DIVERSIFIED"
        ):

            positive_areas.append(
                "Portfolio is well diversified based "
                "on its largest holding allocation."
            )

        # --------------------------------------------------
        # BEST PERFORMER
        # --------------------------------------------------

        best_performer = (
            analytics.get(
                "best_performer"
            )
        )

        best_performer_return = (
            analytics.get(
                "best_performer_return"
            )
        )

        if best_performer:

            positive_areas.append(
                f"{best_performer} is the "
                "best-performing holding with a "
                f"return of "
                f"{best_performer_return:.2f}%."
            )

        # --------------------------------------------------
        # WORST PERFORMER
        # --------------------------------------------------

        worst_performer = (
            analytics.get(
                "worst_performer"
            )
        )

        worst_performer_return = (
            analytics.get(
                "worst_performer_return"
            )
        )

        if worst_performer:

            if worst_performer_return < -20:

                attention_areas.append(
                    f"{worst_performer} is the "
                    "worst-performing holding with a "
                    f"return of "
                    f"{worst_performer_return:.2f}%."
                )

            else:

                positive_areas.append(
                    f"{worst_performer} is the "
                    "lowest-performing holding with a "
                    f"return of "
                    f"{worst_performer_return:.2f}%."
                )

        # --------------------------------------------------
        # OVERALL ASSESSMENT
        # --------------------------------------------------

        if attention_areas:

            overall_assessment = (
                "The portfolio has several areas "
                "that may require attention based "
                "on its current performance, risk, "
                "and allocation data."
            )

        else:

            overall_assessment = (
                "The portfolio does not show any "
                "major attention areas based on "
                "the current analytics."
            )

        # --------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------

        return {
            "overall_assessment": (
                overall_assessment
            ),
            "attention_areas": (
                attention_areas
            ),
            "positive_areas": (
                positive_areas
            ),
        }
    