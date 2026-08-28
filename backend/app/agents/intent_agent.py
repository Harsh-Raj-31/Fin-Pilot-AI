class IntentAgent:

    PORTFOLIO = "PORTFOLIO"
    STOCK = "STOCK"
    GENERAL = "GENERAL"

    def detect_intent(
        self,
        message: str,
    ) -> str:

        message = (
            message
            .lower()
            .strip()
        )

        # --------------------------------------------------
        # PORTFOLIO KEYWORDS
        # --------------------------------------------------

        portfolio_keywords = [

            # Explicit portfolio references
            "portfolio",
            "my portfolio",
            "our portfolio",

            # Holdings
            "my holdings",
            "my holding",
            "my stocks",
            "my stock",
            "my shares",
            "my share",
            "my positions",
            "my position",

            # Investments
            "my investment",
            "my investments",

            # Performance
            "my return",
            "my returns",
            "my profit",
            "my loss",
            "my profit loss",
            "my profit/loss",
            "my performance",
            "am i in profit",
            "am i in loss",
            "am i in profit or loss",
            "am i making a profit",
            "am i making a loss",
            "profit or loss",

            # Risk
            "my risk",
            "my risks",
            "portfolio risk",
            "highest risk holding",
            "highest risk stock",
            "which holding has the highest risk",
            "which stock has the highest risk",
            "which holding has highest risk",
            "which stock has highest risk",
            "riskiest holding",
            "riskiest stock",
            "most risky holding",
            "most risky stock",
            "which holding is most risky",
            "which stock is most risky",           

            # Diversification
            "my diversification",
            "portfolio diversification",
            "how diversified",
            "is my portfolio diversified",
            "diversified portfolio",

            # Allocation
            "my allocation",
            "portfolio allocation",
            "largest holding",
            "biggest holding",
            "largest position",
            "biggest position",
            "largest allocation",
            "biggest allocation",

            # Portfolio performance
            "portfolio performance",
            "portfolio return",
            "portfolio returns",
            "portfolio loss",
            "portfolio losses",
            "portfolio profit",
            "portfolio profits",
            "portfolio pnl",
            "portfolio p&l",

            # Portfolio-specific questions
            "best performer",
            "worst performer",
            "best performing holding",
            "worst performing holding",
            "best performing stock",
            "worst performing stock",
            "which holding is performing best",
            "which holding is performing worst",
            "which stock is performing best",
            "which stock is performing worst",
            "which holding performed best",
            "which holding performed worst",
            "which stock performed best",
            "which stock performed worst",
        ]

        # --------------------------------------------------
        # STOCK KEYWORDS
        # --------------------------------------------------

        stock_keywords = [

            # Price
            "stock price",
            "share price",
            "current price",
            "price of",

            # Stock risk
            "stock risk",
            "share risk",
            "risk of",
            "risk for",
            "risky stock",
            "risky share",

            # Stock information
            "stock information",
            "stock details",
            "stock performance",
            "share performance",
            "stock analysis",
            "share analysis",

            # General stock terminology
            "stock",
            "share",
            "company",

            # Information requests
            "information about",
            "details about",
            "tell me about",

            # Analysis
            "analyze",
            "analyse",

            # Recommendation queries
            "should i buy",
            "should i sell",
            "should i hold",
            "what should i do",
            "what do you recommend",
            "recommend me",
            "is it a buy",
            "is it a sell",
            "buy or sell",
            "buy or hold",
            "sell or hold",
            "buy hold or sell",
            "buy/hold/sell",
            "investment recommendation",

            # Comparison queries
            "compare",
            "comparison",
            "compare stocks",
            "compare shares",
        ]

        # --------------------------------------------------
        # PORTFOLIO HAS PRIORITY
        # --------------------------------------------------

        if any(
            keyword in message
            for keyword in portfolio_keywords
        ):

            return self.PORTFOLIO

        # --------------------------------------------------
        # STOCK
        # --------------------------------------------------

        if any(
            keyword in message
            for keyword in stock_keywords
        ):

            return self.STOCK

        # --------------------------------------------------
        # GENERAL
        # --------------------------------------------------

        return self.GENERAL