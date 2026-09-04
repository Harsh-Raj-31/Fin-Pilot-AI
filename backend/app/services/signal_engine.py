class SignalEngine:

    # =========================================================
    # PERFORMANCE SCORE
    # =========================================================

    def calculate_performance_score(
        self,
        return_percentage,
    ):
        """
        Convert stock return into a
        0-100 performance score.
        """

        if return_percentage is None:
            return None

        if return_percentage >= 10:
            return 100

        if return_percentage >= 5:
            return 80

        if return_percentage >= 0:
            return 60

        if return_percentage >= -5:
            return 40

        if return_percentage >= -10:
            return 20

        return 0

    # =========================================================
    # TECHNICAL SCORE
    # =========================================================

    def calculate_technical_score(
        self,
        rsi,
        current_price=None,
        sma_20=None,
        ema_20=None,
        macd=None,
        macd_signal=None,
    ):
        """
        Calculate technical score using:

        RSI        -> 40%
        SMA 20     -> 20%
        EMA 20     -> 20%
        MACD       -> 20%

        Final score is between 0 and 100.
        """

        if rsi is None:
            return None

        # -----------------------------------------------------
        # RSI SCORE
        # -----------------------------------------------------

        if 50 <= rsi < 70:
            rsi_score = 80

        elif 40 <= rsi < 50:
            rsi_score = 70

        elif 30 <= rsi < 40:
            rsi_score = 60

        elif 70 <= rsi < 80:
            rsi_score = 50

        elif rsi < 30:
            rsi_score = 40

        else:
            rsi_score = 30

        # -----------------------------------------------------
        # SMA SCORE
        # -----------------------------------------------------

        if current_price is not None and sma_20 is not None:

            if current_price > sma_20:
                sma_score = 100
            else:
                sma_score = 40

        else:
            sma_score = 50

        # -----------------------------------------------------
        # EMA SCORE
        # -----------------------------------------------------

        if current_price is not None and ema_20 is not None:

            if current_price > ema_20:
                ema_score = 100
            else:
                ema_score = 40

        else:
            ema_score = 50

        # -----------------------------------------------------
        # MACD SCORE
        # -----------------------------------------------------

        if macd is not None and macd_signal is not None:

            if macd > macd_signal:
                macd_score = 100
            else:
                macd_score = 40

        else:
            macd_score = 50

        # -----------------------------------------------------
        # WEIGHTED TECHNICAL SCORE
        # -----------------------------------------------------

        score = (
            rsi_score * 0.40
            + sma_score * 0.20
            + ema_score * 0.20
            + macd_score * 0.20
        )

        return round(score, 2)

    # =========================================================
    # TECHNICAL REASONING
    # =========================================================

    def generate_technical_reasoning(
        self,
        rsi: float | None,
        current_price: float | None,
        sma_20: float | None,
        ema_20: float | None,
        macd: float | None,
        macd_signal: float | None,
    ) -> list[str]:
        """
        Generate deterministic technical reasoning
        from the same indicators used by the
        technical scoring system.

        This method does not call the LLM.
        """

        reasons = []

        # -----------------------------------------------------
        # RSI
        # -----------------------------------------------------

        if rsi is not None:

            if 50 <= rsi < 70:
                reasons.append(
                    f"RSI is {rsi:.2f}, indicating positive momentum."
                )

            elif 40 <= rsi < 50:
                reasons.append(
                    f"RSI is {rsi:.2f}, indicating moderate momentum."
                )

            elif 30 <= rsi < 40:
                reasons.append(
                    f"RSI is {rsi:.2f}, indicating relatively weak momentum."
                )

            elif rsi < 30:
                reasons.append(
                    f"RSI is {rsi:.2f}, indicating oversold conditions."
                )

            elif 70 <= rsi < 80:
                reasons.append(
                    f"RSI is {rsi:.2f}, indicating strong momentum with "
                    "potentially elevated conditions."
                )

            else:
                reasons.append(
                    f"RSI is {rsi:.2f}, indicating weak or elevated momentum."
                )

        # -----------------------------------------------------
        # PRICE VS SMA 20
        # -----------------------------------------------------

        if current_price is not None and sma_20 is not None:

            if current_price > sma_20:
                reasons.append(
                    f"Current price ({current_price:.2f}) is above "
                    f"the 20-day SMA ({sma_20:.2f})."
                )

            else:
                reasons.append(
                    f"Current price ({current_price:.2f}) is below "
                    f"the 20-day SMA ({sma_20:.2f})."
                )

        # -----------------------------------------------------
        # PRICE VS EMA 20
        # -----------------------------------------------------

        if current_price is not None and ema_20 is not None:

            if current_price > ema_20:
                reasons.append(
                    f"Current price ({current_price:.2f}) is above "
                    f"the 20-day EMA ({ema_20:.2f})."
                )

            else:
                reasons.append(
                    f"Current price ({current_price:.2f}) is below "
                    f"the 20-day EMA ({ema_20:.2f})."
                )

        # -----------------------------------------------------
        # MACD
        # -----------------------------------------------------

        if macd is not None and macd_signal is not None:

            if macd > macd_signal:
                reasons.append(
                    f"MACD ({macd:.2f}) is above its signal line "
                    f"({macd_signal:.2f}), indicating positive momentum."
                )

            else:
                reasons.append(
                    f"MACD ({macd:.2f}) is below its signal line "
                    f"({macd_signal:.2f}), indicating weaker momentum."
                )

        return reasons

    # =========================================================
    # RISK STRENGTH SCORE
    # =========================================================

    def calculate_risk_strength_score(
        self,
        risk_score,
    ):
        """
        Convert risk score into a
        0-100 risk strength score.

        Lower risk = higher score.
        """

        if risk_score is None:
            return None

        return 100 - risk_score
    

    # =========================================================
    # RISK REASONING
    # =========================================================

    def generate_risk_reasoning(
        self,
        risk_score: float | None,
    ) -> list[str]:
        """
        Generate deterministic risk reasoning
        from the calculated risk score.

        Lower risk score indicates lower risk.
        """

        reasons = []

        if risk_score is None:
            reasons.append(
                "Risk information is not available."
            )
            return reasons

        if risk_score <= 20:
            reasons.append(
                f"Risk score is {risk_score:.2f}, "
                "indicating very low risk."
            )

        elif risk_score <= 40:
            reasons.append(
                f"Risk score is {risk_score:.2f}, "
                "indicating relatively low risk."
            )

        elif risk_score <= 60:
            reasons.append(
                f"Risk score is {risk_score:.2f}, "
                "indicating moderate risk."
            )

        elif risk_score <= 80:
            reasons.append(
                f"Risk score is {risk_score:.2f}, "
                "indicating relatively high risk."
            )

        else:
            reasons.append(
                f"Risk score is {risk_score:.2f}, "
                "indicating high risk."
            )

        return reasons


    # =========================================================
    # MARKET REASONING
    # =========================================================

    def generate_market_reasoning(
        self,
        market_trend: str | None,
        market_strength: float | None,
    ) -> list[str]:
        """
        Generate deterministic market reasoning
        from market trend and market strength.
        """

        reasons = []

        if market_trend is None:
            market_trend = "UNKNOWN"

        market_trend = market_trend.upper()

        if market_strength is None:
            reasons.append(
                f"Market trend is {market_trend}, "
                "but market strength is unavailable."
            )
            return reasons

        # -----------------------------------------------------
        # MARKET TREND
        # -----------------------------------------------------

        if market_trend == "BULLISH":
            reasons.append(
                "The broader market trend is bullish, "
                "which provides a supportive environment "
                "for the stock."
            )

        elif market_trend == "BEARISH":
            reasons.append(
                "The broader market trend is bearish, "
                "which creates a challenging environment "
                "for the stock."
            )

        elif market_trend == "NEUTRAL":
            reasons.append(
                "The broader market trend is neutral, "
                "providing limited directional support "
                "for the stock."
            )

        else:
            reasons.append(
                f"The broader market trend is {market_trend}."
            )

        # -----------------------------------------------------
        # MARKET STRENGTH
        # -----------------------------------------------------

        if market_strength >= 70:
            reasons.append(
                f"Market strength is {market_strength:.2f}, "
                "indicating strong market conditions."
            )

        elif market_strength >= 40:
            reasons.append(
                f"Market strength is {market_strength:.2f}, "
                "indicating moderate market conditions."
            )

        else:
            reasons.append(
                f"Market strength is {market_strength:.2f}, "
                "indicating weak market conditions."
            )

        return reasons


    # =========================================================
    # OVERALL SCORE
    # =========================================================

    def calculate_overall_score(
        self,
        performance_score,
        technical_score,
        risk_strength_score,
    ):
        """
        Calculate the overall stock score.

        Performance: 40%
        Technical:   30%
        Risk:        30%
        """

        if (
            performance_score is None
            or technical_score is None
            or risk_strength_score is None
        ):
            return None

        return round(
            (
                performance_score * 0.40
                + technical_score * 0.30
                + risk_strength_score * 0.30
            ),
            2,
        )



    # =========================================================
    # OVERALL EXPLANATION
    # =========================================================

    def generate_overall_explanation(
        self,
        symbol: str,
        signal: str,
        overall_score: float | None,
        confidence: float | None,
        technical_reasons: list[str],
        risk_reasons: list[str],
        market_reasons: list[str],
    ) -> str:
        """
        Generate a structured explanation for the
        final stock signal.

        The explanation is based only on calculated
        scores and deterministic reasoning.
        """

        if overall_score is None:
            return (
                f"Unable to generate a reliable recommendation "
                f"for {symbol.upper()} because sufficient scoring "
                f"data is unavailable."
            )

        explanation_parts = []

        # -----------------------------------------------------
        # FINAL SIGNAL
        # -----------------------------------------------------

        explanation_parts.append(
            f"{symbol.upper()} has a {signal} signal with "
            f"an overall score of {overall_score:.2f}."
        )

        if confidence is not None:
            explanation_parts.append(
                f"The confidence level is {confidence:.2f}%."
            )

        # -----------------------------------------------------
        # TECHNICAL REASONING
        # -----------------------------------------------------

        if technical_reasons:
            explanation_parts.append(
                "Technical analysis: "
                + " ".join(technical_reasons)
            )

        # -----------------------------------------------------
        # RISK REASONING
        # -----------------------------------------------------

        if risk_reasons:
            explanation_parts.append(
                "Risk analysis: "
                + " ".join(risk_reasons)
            )

        # -----------------------------------------------------
        # MARKET REASONING
        # -----------------------------------------------------

        if market_reasons:
            explanation_parts.append(
                "Market analysis: "
                + " ".join(market_reasons)
            )

        # -----------------------------------------------------
        # FINAL INTERPRETATION
        # -----------------------------------------------------

        if signal == "BUY":
            explanation_parts.append(
                "The combination of stock strength and market "
                "conditions supports a BUY signal."
            )

        elif signal == "AVOID":
            explanation_parts.append(
                "The combination of weak stock conditions and "
                "market risk supports an AVOID signal."
            )

        elif signal == "WATCH":
            explanation_parts.append(
                "The stock shows potentially favorable conditions, "
                "but the current market context does not provide "
                "enough support for a BUY signal."
            )

        else:
            explanation_parts.append(
                "The available indicators are mixed or not strong "
                "enough to support a stronger directional signal, "
                "resulting in a HOLD recommendation."
            )

        return " ".join(explanation_parts)


    # =========================================================
    # SIGNAL
    # =========================================================

    def determine_signal(
        self,
        overall_score,
        market_trend,
    ):
        """
        Determine final stock signal using
        stock score and market condition.
        """

        if overall_score is None:
            return "HOLD"

        market_trend = (
            market_trend.upper()
            if market_trend
            else "NEUTRAL"
        )

        # -----------------------------------------------------
        # STRONG STOCK + BULLISH MARKET
        # -----------------------------------------------------

        if (
            overall_score >= 70
            and market_trend == "BULLISH"
        ):
            return "BUY"

        # -----------------------------------------------------
        # WEAK STOCK + BEARISH MARKET
        # -----------------------------------------------------

        if (
            overall_score < 40
            and market_trend == "BEARISH"
        ):
            return "AVOID"

        # -----------------------------------------------------
        # GOOD STOCK + NEUTRAL MARKET
        # -----------------------------------------------------

        if overall_score >= 60:
            return "WATCH"

        # -----------------------------------------------------
        # DEFAULT
        # -----------------------------------------------------

        return "HOLD"

    # =========================================================
    # CONFIDENCE
    # =========================================================

    def calculate_confidence(
        self,
        overall_score,
        market_strength,
        market_trend,
    ):
        """
        Calculate confidence in the final signal.

        Stock Score:      50%
        Market Strength:  30%
        Market Alignment: 20%
        """

        if (
            overall_score is None
            or market_strength is None
        ):
            return None

        # -----------------------------------------------------
        # STOCK SCORE COMPONENT
        # -----------------------------------------------------

        stock_component = overall_score * 0.50

        # -----------------------------------------------------
        # MARKET STRENGTH COMPONENT
        # -----------------------------------------------------

        market_component = market_strength * 0.30

        # -----------------------------------------------------
        # MARKET ALIGNMENT COMPONENT
        # -----------------------------------------------------

        market_trend = (
            market_trend.upper()
            if market_trend
            else "NEUTRAL"
        )

        if market_trend == "BULLISH":

            if overall_score >= 60:
                alignment_score = 100
            else:
                alignment_score = 50

        elif market_trend == "BEARISH":

            if overall_score < 40:
                alignment_score = 100
            else:
                alignment_score = 50

        else:
            alignment_score = 50

        alignment_component = alignment_score * 0.20

        # -----------------------------------------------------
        # FINAL CONFIDENCE
        # -----------------------------------------------------

        confidence = (
            stock_component
            + market_component
            + alignment_component
        )

        return round(
            max(0, min(confidence, 100)),
            2,
        )


# =============================================================
# SINGLE SIGNAL ENGINE INSTANCE
# =============================================================

signal_engine = SignalEngine()