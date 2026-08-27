class StockComparisonEngine:

    @classmethod
    def compare(
        cls,
        stock_data_list: list[dict],
    ) -> dict:

        if len(stock_data_list) < 2:
            raise ValueError(
                "At least two stocks are required "
                "for comparison."
            )

        results = []

        for stock_data in stock_data_list:

            performance = stock_data["performance"]
            risk = stock_data["risk"]
            indicators = stock_data["indicators"]

            # --------------------------------------------------
            # PERFORMANCE SCORE - 25
            # --------------------------------------------------

            return_percentage = (
                performance["return_percentage"]
            )

            if return_percentage > 5:
                performance_score = 25

            elif return_percentage > 2:
                performance_score = 20

            elif return_percentage >= 0:
                performance_score = 15

            elif return_percentage > -2:
                performance_score = 10

            elif return_percentage > -5:
                performance_score = 5

            else:
                performance_score = 0

            # --------------------------------------------------
            # TREND SCORE - 25
            # --------------------------------------------------

            current_price = (
                performance["current_price"]
            )

            sma_20 = indicators["sma_20"]
            ema_20 = indicators["ema_20"]

            if (
                current_price > sma_20
                and current_price > ema_20
            ):
                trend_score = 25

            elif (
                current_price > sma_20
                or current_price > ema_20
            ):
                trend_score = 17

            else:
                trend_score = 7

            # --------------------------------------------------
            # MOMENTUM SCORE - 25
            # --------------------------------------------------

            rsi = indicators["rsi_14"]

            macd = indicators["macd"]
            macd_signal = indicators["macd_signal"]

            if 50 <= rsi <= 70:
                rsi_score = 13

            elif rsi < 30:
                rsi_score = 8

            elif 30 <= rsi < 50:
                rsi_score = 7

            else:
                rsi_score = 5

            if macd > macd_signal:
                macd_score = 12

            else:
                macd_score = 5

            momentum_score = (
                rsi_score + macd_score
            )

            # --------------------------------------------------
            # RISK SCORE - 25
            # --------------------------------------------------

            risk_score = risk["risk_score"]

            if risk_score <= 30:
                risk_points = 25

            elif risk_score <= 50:
                risk_points = 20

            elif risk_score <= 70:
                risk_points = 13

            elif risk_score <= 85:
                risk_points = 7

            else:
                risk_points = 0

            # --------------------------------------------------
            # TOTAL SCORE
            # --------------------------------------------------

            total_score = (
                performance_score
                + trend_score
                + momentum_score
                + risk_points
            )

            results.append(
                {
                    "symbol": stock_data[
                        "market_data"
                    ]["symbol"],

                    "score": total_score,

                    "breakdown": {
                        "performance": performance_score,
                        "trend": trend_score,
                        "momentum": momentum_score,
                        "risk": risk_points,
                    },

                    "metrics": {
                        "return_percentage":
                            return_percentage,

                        "current_price":
                            current_price,

                        "sma_20":
                            sma_20,

                        "ema_20":
                            ema_20,

                        "rsi_14":
                            rsi,

                        "macd":
                            macd,

                        "macd_signal":
                            macd_signal,

                        "risk_score":
                            risk_score,

                        "risk_level":
                            risk["risk_level"],

                        "volatility":
                            risk["volatility"],

                        "maximum_drawdown":
                            risk["maximum_drawdown"],
                    },
                }
            )

        # --------------------------------------------------
        # SORT BY SCORE
        # --------------------------------------------------

        results.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        first = results[0]
        second = results[1]

        score_difference = (
            first["score"]
            - second["score"]
        )

        # --------------------------------------------------
        # WINNER / TIE
        # --------------------------------------------------

        if score_difference == 0:
            winner = None

        else:
            winner = first["symbol"]

        # --------------------------------------------------
        # COMPARISON STRENGTH
        # --------------------------------------------------

        if score_difference <= 2:
            comparison_strength = "VERY CLOSE"

        elif score_difference <= 5:
            comparison_strength = "CLOSE"

        elif score_difference <= 10:
            comparison_strength = "MODERATE"

        else:
            comparison_strength = "CLEAR"

        # --------------------------------------------------
        # FACTOR DIFFERENCES
        # --------------------------------------------------

        factor_differences = {}

        for factor in [
            "performance",
            "trend",
            "momentum",
            "risk",
        ]:

            first_score = first[
                "breakdown"
            ][factor]

            second_score = second[
                "breakdown"
            ][factor]

            factor_differences[factor] = (
                first_score - second_score
            )

        # --------------------------------------------------
        # RAW METRIC COMPARISON
        # --------------------------------------------------

        first_metrics = first["metrics"]
        second_metrics = second["metrics"]

        observations = []

        # Return
        if (
            first_metrics["return_percentage"]
            > second_metrics["return_percentage"]
        ):
            observations.append(
                f"{first['symbol']} has the "
                f"better 1-month return."
            )

        elif (
            first_metrics["return_percentage"]
            < second_metrics["return_percentage"]
        ):
            observations.append(
                f"{second['symbol']} has the "
                f"better 1-month return."
            )

        # Risk score
        if (
            first_metrics["risk_score"]
            < second_metrics["risk_score"]
        ):
            observations.append(
                f"{first['symbol']} has the "
                f"lower risk score."
            )

        elif (
            first_metrics["risk_score"]
            > second_metrics["risk_score"]
        ):
            observations.append(
                f"{second['symbol']} has the "
                f"lower risk score."
            )

        # Volatility
        if (
            first_metrics["volatility"]
            < second_metrics["volatility"]
        ):
            observations.append(
                f"{first['symbol']} has lower "
                f"volatility."
            )

        elif (
            first_metrics["volatility"]
            > second_metrics["volatility"]
        ):
            observations.append(
                f"{second['symbol']} has lower "
                f"volatility."
            )

        # Maximum drawdown
        if (
            first_metrics["maximum_drawdown"]
            > second_metrics["maximum_drawdown"]
        ):
            observations.append(
                f"{first['symbol']} has the "
                f"smaller maximum drawdown."
            )

        elif (
            first_metrics["maximum_drawdown"]
            < second_metrics["maximum_drawdown"]
        ):
            observations.append(
                f"{second['symbol']} has the "
                f"smaller maximum drawdown."
            )

        # Trend
        if (
            first_metrics["current_price"]
            > first_metrics["sma_20"]
            and first_metrics["current_price"]
            > first_metrics["ema_20"]
        ):
            observations.append(
                f"{first['symbol']} is above "
                f"both its 20-day SMA and EMA."
            )

        elif (
            second_metrics["current_price"]
            > second_metrics["sma_20"]
            and second_metrics["current_price"]
            > second_metrics["ema_20"]
        ):
            observations.append(
                f"{second['symbol']} is above "
                f"both its 20-day SMA and EMA."
            )

        # --------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------

        return {
            "winner": winner,

            "winner_score": (
                first["score"]
            ),

            "score_difference":
                score_difference,

            "comparison_strength":
                comparison_strength,

            "factor_differences":
                factor_differences,

            "observations":
                observations,

            "stocks":
                results,
        }