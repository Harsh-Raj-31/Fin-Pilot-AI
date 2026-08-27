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

        # --------------------------------------------------
        # SIGNAL STRENGTH
        # --------------------------------------------------

        if recommendation == cls.BUY:

            if total_score >= 80:
                signal_strength = "STRONG"

            else:
                signal_strength = "MODERATE"

        elif recommendation == cls.HOLD:

            signal_strength = "BORDERLINE"

        else:

            if total_score < 30:
                signal_strength = "STRONG"

            else:
                signal_strength = "MODERATE"

        # --------------------------------------------------
        # SUMMARY
        # --------------------------------------------------

        summary = (
            f"FinPilot's current model generates a "
            f"{signal_strength.lower()} "
            f"{recommendation} signal based on the "
            f"available market indicators."
        )

        # --------------------------------------------------
        # RECOMMENDATION REASONS
        # --------------------------------------------------

        reasons = []

        # Performance reason

        if return_percentage > 0:

            reasons.append(
                f"1-month return is positive "
                f"({return_percentage:.2f}%)."
            )

        elif return_percentage < 0:

            reasons.append(
                f"1-month return is negative "
                f"({return_percentage:.2f}%)."
            )

        else:

            reasons.append(
                "1-month return is 0%."
            )

        # Trend reasons

        if current_price > sma_20:

            reasons.append(
                "Current price is above the "
                "20-day SMA."
            )

        else:

            reasons.append(
                "Current price is below the "
                "20-day SMA."
            )

        if current_price > ema_20:

            reasons.append(
                "Current price is above the "
                "20-day EMA."
            )

        else:

            reasons.append(
                "Current price is below the "
                "20-day EMA."
            )

        # RSI reason

        if rsi < 30:

            reasons.append(
                f"RSI is {rsi:.2f}, which is below "
                "30 and indicates an oversold "
                "condition."
            )

        elif rsi <= 70:

            reasons.append(
                f"RSI is {rsi:.2f}, which is within "
                "the 30-70 range."
            )

        else:

            reasons.append(
                f"RSI is {rsi:.2f}, which is above "
                "70 and indicates an overbought "
                "condition."
            )

        # MACD reason

        if macd > macd_signal:

            reasons.append(
                "MACD is above its signal line."
            )

        else:

            reasons.append(
                "MACD is below its signal line."
            )

        # Risk reason

        reasons.append(
            f"Risk level is {risk['risk_level']} "
            f"with a risk score of "
            f"{risk_score:.1f}."
        )

        # --------------------------------------------------
        # FACTOR CLASSIFICATION
        # --------------------------------------------------

        positive_factors = []
        negative_factors = []
        neutral_factors = []

        # --------------------------------------------------
        # PERFORMANCE FACTOR
        # --------------------------------------------------

        if return_percentage > 0:

            positive_factors.append(
                f"Positive 1-month return "
                f"({return_percentage:.2f}%)."
            )

        elif return_percentage < 0:

            negative_factors.append(
                f"Negative 1-month return "
                f"({return_percentage:.2f}%)."
            )

        else:

            neutral_factors.append(
                "1-month return is 0%."
            )

        # --------------------------------------------------
        # SMA TREND FACTOR
        # --------------------------------------------------

        if current_price > sma_20:

            positive_factors.append(
                "Current price is above the "
                "20-day SMA."
            )

        else:

            negative_factors.append(
                "Current price is below the "
                "20-day SMA."
            )

        # --------------------------------------------------
        # EMA TREND FACTOR
        # --------------------------------------------------

        if current_price > ema_20:

            positive_factors.append(
                "Current price is above the "
                "20-day EMA."
            )

        else:

            negative_factors.append(
                "Current price is below the "
                "20-day EMA."
            )

        # --------------------------------------------------
        # RSI FACTOR
        # --------------------------------------------------

        if rsi < 30:

            neutral_factors.append(
                f"RSI is {rsi:.2f}, indicating "
                "an oversold condition."
            )

        elif rsi <= 70:

            positive_factors.append(
                f"RSI is {rsi:.2f}, within the "
                "30-70 range."
            )

        else:

            negative_factors.append(
                f"RSI is {rsi:.2f}, indicating "
                "an overbought condition."
            )

        # --------------------------------------------------
        # MACD FACTOR
        # --------------------------------------------------

        if macd > macd_signal:

            positive_factors.append(
                "MACD is above its signal line."
            )

        else:

            negative_factors.append(
                "MACD is below its signal line."
            )

        # --------------------------------------------------
        # RISK FACTOR
        # --------------------------------------------------

        if risk_score <= 50:

            positive_factors.append(
                f"Risk level is {risk['risk_level']} "
                f"with a risk score of "
                f"{risk_score:.1f}."
            )

        elif risk_score <= 70:

            neutral_factors.append(
                f"Risk level is {risk['risk_level']} "
                f"with a risk score of "
                f"{risk_score:.1f}."
            )

        else:

            negative_factors.append(
                f"Risk level is {risk['risk_level']} "
                f"with a risk score of "
                f"{risk_score:.1f}."
            )

        # --------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------

        return {
            "symbol": stock_data["market_data"]["symbol"],

            "recommendation": recommendation,

            "score": total_score,

            "signal_strength": signal_strength,

            "summary": summary,

            "reasons": reasons,

            "positive_factors": positive_factors,

            "negative_factors": negative_factors,

            "neutral_factors": neutral_factors,

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