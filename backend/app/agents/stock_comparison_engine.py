class StockComparisonEngine:

    @classmethod
    def compare(
        cls,
        stock_data_list: list[dict],
    ) -> dict:

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

            # RSI
            if 50 <= rsi <= 70:
                rsi_score = 13

            elif rsi < 30:
                rsi_score = 8

            elif 30 <= rsi < 50:
                rsi_score = 7

            else:
                rsi_score = 5

            # MACD
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
            # TOTAL
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

        # Highest score first
        results.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        winner = results[0]["symbol"]

        return {
            "winner": winner,
            "stocks": results,
        }