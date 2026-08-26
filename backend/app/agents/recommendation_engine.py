class RecommendationEngine:

    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"

    @classmethod
    def analyze(
        cls,
        stock_data: dict,
    ) -> dict:

        performance = stock_data["performance"]
        risk = stock_data["risk"]
        indicators = stock_data["indicators"]

        # --------------------------------------------------
        # 1. PERFORMANCE SCORE - 20 POINTS
        # --------------------------------------------------

        return_percentage = (
            performance["return_percentage"]
        )

        if return_percentage > 5:
            performance_score = 20
        elif return_percentage > 2:
            performance_score = 16
        elif return_percentage >= 0:
            performance_score = 12
        elif return_percentage > -2:
            performance_score = 8
        elif return_percentage > -5:
            performance_score = 4
        else:
            performance_score = 0

        # --------------------------------------------------
        # 2. TREND SCORE - 25 POINTS
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
        # 3. MOMENTUM SCORE - 25 POINTS
        # --------------------------------------------------

        rsi = indicators["rsi_14"]

        macd = indicators["macd"]
        macd_signal = indicators["macd_signal"]

        # RSI component - 12 points
        if rsi < 30:
            rsi_score = 8

        elif rsi < 50:
            rsi_score = 5

        elif rsi <= 70:
            rsi_score = 10

        else:
            rsi_score = 4

        # MACD component - 13 points
        if macd > macd_signal:
            macd_score = 13
        else:
            macd_score = 5

        momentum_score = (
            rsi_score + macd_score
        )

        # --------------------------------------------------
        # 4. RISK SCORE - 30 POINTS
        # --------------------------------------------------

        risk_score = risk["risk_score"]

        if risk_score <= 30:
            risk_points = 30

        elif risk_score <= 50:
            risk_points = 24

        elif risk_score <= 70:
            risk_points = 15

        elif risk_score <= 85:
            risk_points = 8

        else:
            risk_points = 0

        # --------------------------------------------------
        # FINAL SCORE
        # --------------------------------------------------

        total_score = (
            performance_score
            + trend_score
            + momentum_score
            + risk_points
        )

        # --------------------------------------------------
        # RECOMMENDATION
        # --------------------------------------------------

        if total_score >= 80:
            recommendation = cls.BUY

        elif total_score >= 55:
            recommendation = cls.HOLD

        else:
            recommendation = cls.SELL

        return {
            "symbol": stock_data["market_data"]["symbol"],
            "recommendation": recommendation,
            "score": total_score,
            "breakdown": {
                "performance": performance_score,
                "trend": trend_score,
                "momentum": momentum_score,
                "risk": risk_points,
            },
            "metrics": {
                "return_percentage": return_percentage,
                "current_price": current_price,
                "sma_20": sma_20,
                "ema_20": ema_20,
                "rsi_14": rsi,
                "macd": macd,
                "macd_signal": macd_signal,
                "risk_score": risk_score,
                "risk_level": risk["risk_level"],
                "volatility": risk["volatility"],
                "maximum_drawdown": risk[
                    "maximum_drawdown"
                ],
            },
        }