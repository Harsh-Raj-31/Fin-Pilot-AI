class PortfolioQueryType:

    GENERAL = "general"
    RETURN = "return"
    VALUE = "value"
    PROFIT_LOSS = "profit_loss"
    BEST_PERFORMER = "best_performer"
    WORST_PERFORMER = "worst_performer"
    HIGHEST_RISK = "highest_risk"
    LARGEST_HOLDING = "largest_holding"
    DIVERSIFICATION = "diversification"

    RETURN_KEYWORDS = {
        "portfolio return",
        "portfolio performance",
        "portfolio percentage",
        "portfolio gain percentage",
        "portfolio loss percentage",
        "return on my portfolio",
        "how much return",
        "what is my return",
    }

    VALUE_KEYWORDS = {
        "portfolio value",
        "current portfolio value",
        "current value",
        "worth of my portfolio",
        "how much is my portfolio worth",
        "what is my portfolio worth",
    }

    PROFIT_LOSS_KEYWORDS = {
        "profit or loss",
        "profit loss",
        "profit/loss",
        "portfolio pnl",
        "portfolio p&l",
        "how much profit",
        "how much loss",
        "am i in profit",
        "am i in loss",
    }

    BEST_PERFORMER_KEYWORDS = {
        "best performer",
        "best performing stock",
        "best performing holding",
        "performing best",
        "which stock performed best",
        "which stock is performing best",
        "which holding performed best",
        "which holding is performing best",
    }

    WORST_PERFORMER_KEYWORDS = {
        "worst performer",
        "worst performing stock",
        "worst performing holding",
        "performing worst",
        "which stock performed worst",
        "which stock is performing worst",
        "which holding performed worst",
        "which holding is performing worst",
    }

    HIGHEST_RISK_KEYWORDS = {
        "highest risk",
        "highest risk stock",
        "highest risk holding",
        "riskiest stock",
        "riskiest holding",
        "most risky stock",
        "most risky holding",
        "which stock has the highest risk",
        "which holding has the highest risk",
    }

    LARGEST_HOLDING_KEYWORDS = {
        "largest holding",
        "biggest holding",
        "largest position",
        "biggest position",
        "largest allocation",
        "biggest allocation",
        "which stock has the largest allocation",
        "which holding has the largest allocation",
    }

    DIVERSIFICATION_KEYWORDS = {
        "diversification",
        "diversified",
        "diversify",
        "how diversified",
        "is my portfolio diversified",
        "portfolio concentration",
        "concentrated portfolio",
    }

    @classmethod
    def detect(
        cls,
        message: str,
    ) -> str:

        normalized = (
            message.lower()
            .strip()
        )

        # --------------------------------------------------
        # RETURN
        # --------------------------------------------------

        for keyword in cls.RETURN_KEYWORDS:

            if keyword in normalized:

                return cls.RETURN

        # --------------------------------------------------
        # VALUE
        # --------------------------------------------------

        for keyword in cls.VALUE_KEYWORDS:

            if keyword in normalized:

                return cls.VALUE

        # --------------------------------------------------
        # PROFIT / LOSS
        # --------------------------------------------------

        for keyword in cls.PROFIT_LOSS_KEYWORDS:

            if keyword in normalized:

                return cls.PROFIT_LOSS

        # --------------------------------------------------
        # BEST PERFORMER
        # --------------------------------------------------

        for keyword in cls.BEST_PERFORMER_KEYWORDS:

            if keyword in normalized:

                return cls.BEST_PERFORMER

        # --------------------------------------------------
        # WORST PERFORMER
        # --------------------------------------------------

        for keyword in cls.WORST_PERFORMER_KEYWORDS:

            if keyword in normalized:

                return cls.WORST_PERFORMER

        # --------------------------------------------------
        # HIGHEST RISK
        # --------------------------------------------------

        for keyword in cls.HIGHEST_RISK_KEYWORDS:

            if keyword in normalized:

                return cls.HIGHEST_RISK

        # --------------------------------------------------
        # LARGEST HOLDING
        # --------------------------------------------------

        for keyword in cls.LARGEST_HOLDING_KEYWORDS:

            if keyword in normalized:

                return cls.LARGEST_HOLDING

        # --------------------------------------------------
        # DIVERSIFICATION
        # --------------------------------------------------

        for keyword in cls.DIVERSIFICATION_KEYWORDS:

            if keyword in normalized:

                return cls.DIVERSIFICATION

        # --------------------------------------------------
        # GENERAL
        # --------------------------------------------------

        return cls.GENERAL