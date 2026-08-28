class StockComparisonEngine:

    @classmethod
    def compare(
        cls,
        stock_data_list: list[dict],
    ) -> dict:

        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        if len(stock_data_list) < 2:
            raise ValueError(
                "At least two stocks are required "
                "for comparison."
            )

        results = []

        # --------------------------------------------------
        # ANALYZE EACH STOCK
        # --------------------------------------------------

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

            # --------------------------------------------------
            # STORE RESULT
            # --------------------------------------------------

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

        # --------------------------------------------------
        # SCORE DIFFERENCE
        # --------------------------------------------------

        score_difference = (
            first["score"]
            - second["score"]
        )

        # --------------------------------------------------
        # WINNER / TIE
        # --------------------------------------------------

        if score_difference == 0:

            winner = None
            comparison_result = "SCORE TIE"

        else:

            winner = first["symbol"]
            comparison_result = "WINNER"

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
        # METRICS
        # --------------------------------------------------

        first_metrics = first["metrics"]
        second_metrics = second["metrics"]

        observations = []

        # --------------------------------------------------
        # PERFORMANCE
        # --------------------------------------------------

        if (
            first_metrics["return_percentage"]
            > second_metrics["return_percentage"]
        ):

            observations.append(
                f"{first['symbol']} has the "
                "better 1-month return."
            )

        elif (
            first_metrics["return_percentage"]
            < second_metrics["return_percentage"]
        ):

            observations.append(
                f"{second['symbol']} has the "
                "better 1-month return."
            )

        # --------------------------------------------------
        # RISK SCORE
        # --------------------------------------------------

        if (
            first_metrics["risk_score"]
            < second_metrics["risk_score"]
        ):

            observations.append(
                f"{first['symbol']} has the "
                "lower risk score."
            )

        elif (
            first_metrics["risk_score"]
            > second_metrics["risk_score"]
        ):

            observations.append(
                f"{second['symbol']} has the "
                "lower risk score."
            )

        # --------------------------------------------------
        # VOLATILITY
        # --------------------------------------------------

        if (
            first_metrics["volatility"]
            < second_metrics["volatility"]
        ):

            observations.append(
                f"{first['symbol']} has lower "
                "volatility."
            )

        elif (
            first_metrics["volatility"]
            > second_metrics["volatility"]
        ):

            observations.append(
                f"{second['symbol']} has lower "
                "volatility."
            )

        # --------------------------------------------------
        # MAXIMUM DRAWDOWN
        # --------------------------------------------------

        if (
            first_metrics["maximum_drawdown"]
            > second_metrics["maximum_drawdown"]
        ):

            observations.append(
                f"{first['symbol']} has the "
                "smaller maximum drawdown."
            )

        elif (
            first_metrics["maximum_drawdown"]
            < second_metrics["maximum_drawdown"]
        ):

            observations.append(
                f"{second['symbol']} has the "
                "smaller maximum drawdown."
            )

        # --------------------------------------------------
        # TREND OBSERVATION
        # --------------------------------------------------

        first_above_both = (
            first_metrics["current_price"]
            > first_metrics["sma_20"]
            and
            first_metrics["current_price"]
            > first_metrics["ema_20"]
        )

        second_above_both = (
            second_metrics["current_price"]
            > second_metrics["sma_20"]
            and
            second_metrics["current_price"]
            > second_metrics["ema_20"]
        )

        if (
            first_above_both
            and not second_above_both
        ):

            observations.append(
                f"{first['symbol']} is above "
                "both its 20-day SMA and EMA."
            )

        elif (
            second_above_both
            and not first_above_both
        ):

            observations.append(
                f"{second['symbol']} is above "
                "both its 20-day SMA and EMA."
            )

        # --------------------------------------------------
        # METRIC LEADERS
        # --------------------------------------------------

        metric_leaders = {}

        # Best performance

        if (
            first_metrics["return_percentage"]
            > second_metrics["return_percentage"]
        ):

            metric_leaders[
                "best_performance"
            ] = first["symbol"]

        elif (
            first_metrics["return_percentage"]
            < second_metrics["return_percentage"]
        ):

            metric_leaders[
                "best_performance"
            ] = second["symbol"]

        else:

            metric_leaders[
                "best_performance"
            ] = None

        # Lowest risk

        if (
            first_metrics["risk_score"]
            < second_metrics["risk_score"]
        ):

            metric_leaders[
                "lowest_risk"
            ] = first["symbol"]

        elif (
            first_metrics["risk_score"]
            > second_metrics["risk_score"]
        ):

            metric_leaders[
                "lowest_risk"
            ] = second["symbol"]

        else:

            metric_leaders[
                "lowest_risk"
            ] = None

        # Lowest volatility

        if (
            first_metrics["volatility"]
            < second_metrics["volatility"]
        ):

            metric_leaders[
                "lowest_volatility"
            ] = first["symbol"]

        elif (
            first_metrics["volatility"]
            > second_metrics["volatility"]
        ):

            metric_leaders[
                "lowest_volatility"
            ] = second["symbol"]

        else:

            metric_leaders[
                "lowest_volatility"
            ] = None

        # Smallest drawdown

        if (
            first_metrics["maximum_drawdown"]
            > second_metrics["maximum_drawdown"]
        ):

            metric_leaders[
                "smallest_drawdown"
            ] = first["symbol"]

        elif (
            first_metrics["maximum_drawdown"]
            < second_metrics["maximum_drawdown"]
        ):

            metric_leaders[
                "smallest_drawdown"
            ] = second["symbol"]

        else:

            metric_leaders[
                "smallest_drawdown"
            ] = None

        # --------------------------------------------------
        # TIE BREAKER
        # --------------------------------------------------

        tie_breaker = None

        if score_difference == 0:

            advantages = {}

            for metric, symbol in (
                metric_leaders.items()
            ):

                if symbol is not None:

                    advantages[symbol] = (
                        advantages.get(
                            symbol,
                            0
                        ) + 1
                    )

            if advantages:

                highest_count = max(
                    advantages.values()
                )

                leaders = [
                    symbol
                    for symbol, count
                    in advantages.items()
                    if count == highest_count
                ]

                if len(leaders) == 1:

                    tie_breaker = leaders[0]

        # --------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------

        return {
            "winner": winner,

            "winner_score":
                first["score"],

            "score_difference":
                score_difference,

            "comparison_result":
                comparison_result,

            "comparison_strength":
                comparison_strength,

            "factor_differences":
                factor_differences,

            "metric_leaders":
                metric_leaders,

            "tie_breaker":
                tie_breaker,

            "observations":
                observations,

            "stocks":
                results,
        }