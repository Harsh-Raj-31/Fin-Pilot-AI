class SignalEngine:

    """
    Signal Engine

    Responsible for converting financial data into
    deterministic stock scores.

    It does NOT fetch market data.
    It does NOT call the LLM.
    It does NOT make up financial information.

    MarketDataService provides the data.
    SignalEngine analyzes the data.
    AIService will later explain the analysis.
    """

    # =========================================================
    # PERFORMANCE SCORE
    # =========================================================

    def calculate_performance_score(
        self,
        return_percentage: float | None,
    ) -> float | None:

        """
        Convert stock return into a 0-100 performance score.
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
        rsi: float | None,
        current_price: float | None,
        sma_20: float | None,
        ema_20: float | None,
        macd: float | None,
        macd_signal: float | None,
    ) -> float | None:

        """
        Calculate a 0-100 technical score using:

        RSI
        Price vs SMA 20
        Price vs EMA 20
        MACD vs MACD Signal
        """

        if (
            rsi is None
            or current_price is None
            or sma_20 is None
            or ema_20 is None
            or macd is None
            or macd_signal is None
        ):
            return None

        score = 0

        # -----------------------------------------------------
        # RSI
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
        # PRICE VS SMA
        # -----------------------------------------------------

        if current_price > sma_20:
            sma_score = 100
        else:
            sma_score = 40

        # -----------------------------------------------------
        # PRICE VS EMA
        # -----------------------------------------------------

        if current_price > ema_20:
            ema_score = 100
        else:
            ema_score = 40

        # -----------------------------------------------------
        # MACD
        # -----------------------------------------------------

        if macd > macd_signal:
            macd_score = 100
        else:
            macd_score = 40

        # -----------------------------------------------------
        # Combine technical indicators
        # -----------------------------------------------------

        score = (
            rsi_score * 0.40
            + sma_score * 0.20
            + ema_score * 0.20
            + macd_score * 0.20
        )

        return round(score, 2)

    # =========================================================
    # RISK STRENGTH SCORE
    # =========================================================

    def calculate_risk_strength_score(
        self,
        risk_score: float | None,
    ) -> float | None:

        """
        Convert risk score into risk strength.

        Lower risk = higher strength.

        Example:

        Risk Score = 20
        Risk Strength = 80
        """

        if risk_score is None:
            return None

        return round(
            100 - risk_score,
            2,
        )

    # =========================================================
    # OVERALL SCORE
    # =========================================================

    def calculate_overall_score(
        self,
        performance_score: float | None,
        technical_score: float | None,
        risk_strength_score: float | None,
    ) -> float | None:

        """
        Calculate the overall stock score.

        Performance = 40%
        Technical   = 30%
        Risk        = 30%
        """

        if (
            performance_score is None
            or technical_score is None
            or risk_strength_score is None
        ):
            return None

        overall_score = (
            performance_score * 0.40
            + technical_score * 0.30
            + risk_strength_score * 0.30
        )

        return round(
            overall_score,
            2,
        )


    # =========================================================
    # STOCK SIGNAL
    # =========================================================

    def determine_signal(
        self,
        overall_score: float | None,
        market_trend: str,
    ) -> str:

        """
        Determine the stock signal using:

        - Overall stock score
        - Broader market trend
        """

        if overall_score is None:
            return "HOLD"

        market_trend = market_trend.upper()

        # Strong stock + bullish market
        if (
            overall_score >= 70
            and market_trend == "BULLISH"
        ):
            return "BUY"

        # Weak stock + bearish market
        if (
            overall_score < 40
            and market_trend == "BEARISH"
        ):
            return "AVOID"

        # Strong stock but market confirmation is missing
        if overall_score >= 60:
            return "WATCH"

        # Default condition
        return "HOLD"


    # =========================================================
    # CONFIDENCE
    # =========================================================

    def calculate_confidence(
        self,
        overall_score: float | None,
        market_strength: float | None,
        market_trend: str,
    ) -> float | None:

        """
        Calculate signal confidence from 0 to 100.

        Stock Score      = 50%
        Market Strength  = 30%
        Market Alignment = 20%
        """

        if (
            overall_score is None
            or market_strength is None
        ):
            return None

        market_trend = market_trend.upper()

        if market_trend == "BULLISH":
            market_alignment = 100

        elif market_trend == "NEUTRAL":
            market_alignment = 60

        else:
            market_alignment = 30

        confidence = (
            overall_score * 0.50
            + market_strength * 0.30
            + market_alignment * 0.20
        )

        return round(
            confidence,
            2,
        )


    # =========================================================
    # COMPLETE STOCK ANALYSIS
    # =========================================================

    def analyze_stock(
        self,
        symbol: str,
        performance_data: dict,
        indicators: dict,
        risk_data: dict,
        market_data: dict,
    ) -> dict:

        """
        Perform complete stock signal analysis.

        The engine receives already-calculated financial data
        and converts it into scores, signal, and confidence.
        """

        symbol = symbol.strip().upper()

        # -----------------------------------------------------
        # Performance Score
        # -----------------------------------------------------

        performance_score = (
            self.calculate_performance_score(
                performance_data.get(
                    "return_percentage"
                )
            )
        )

        # -----------------------------------------------------
        # Technical Score
        # -----------------------------------------------------

        technical_score = (
            self.calculate_technical_score(
                rsi=indicators.get("rsi_14"),
                current_price=performance_data.get(
                    "current_price"
                ),
                sma_20=indicators.get("sma_20"),
                ema_20=indicators.get("ema_20"),
                macd=indicators.get("macd"),
                macd_signal=indicators.get(
                    "macd_signal"
                ),
            )
        )

        # -----------------------------------------------------
        # Risk Strength Score
        # -----------------------------------------------------

        risk_score = risk_data.get(
            "risk_score"
        )

        risk_strength_score = (
            self.calculate_risk_strength_score(
                risk_score
            )
        )

        # -----------------------------------------------------
        # Overall Score
        # -----------------------------------------------------

        overall_score = (
            self.calculate_overall_score(
                performance_score,
                technical_score,
                risk_strength_score,
            )
        )

        # -----------------------------------------------------
        # Market Context
        # -----------------------------------------------------

        market_trend = market_data.get(
            "trend",
            "NEUTRAL",
        )

        market_strength = market_data.get(
            "market_strength"
        )

        # -----------------------------------------------------
        # Signal
        # -----------------------------------------------------

        signal = self.determine_signal(
            overall_score,
            market_trend,
        )

        # -----------------------------------------------------
        # Confidence
        # -----------------------------------------------------

        confidence = (
            self.calculate_confidence(
                overall_score,
                market_strength,
                market_trend,
            )
        )

        # -----------------------------------------------------
        # Final Result
        # -----------------------------------------------------

        return {
            "symbol": symbol,

            "performance_score": (
                performance_score
            ),

            "technical_score": (
                technical_score
            ),

            "risk_score": (
                risk_score
            ),

            "risk_strength_score": (
                risk_strength_score
            ),

            "overall_score": (
                overall_score
            ),

            "market_trend": (
                market_trend
            ),

            "market_strength": (
                market_strength
            ),

            "signal": signal,

            "confidence": confidence,
        }
    

# =============================================================
# SINGLE ENGINE INSTANCE
# =============================================================

signal_engine = SignalEngine()