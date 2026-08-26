class IntentAgent:

    PORTFOLIO = "PORTFOLIO"
    STOCK = "STOCK"
    GENERAL = "GENERAL"

    def detect_intent(
        self,
        message: str,
    ) -> str:

        message = message.lower().strip()

        portfolio_keywords = [
            "portfolio",
            "my holdings",
            "my stocks",
            "my investment",
            "my investments",
            "my return",
            "my profit",
            "my loss",
            "my risk",
            "my diversification",
            "my allocation",
            "portfolio risk",
            "portfolio performance",
            "portfolio return",
            "portfolio loss",
            "portfolio profit",
        ]

        stock_keywords = [
            "stock price",
            "share price",
            "current price",
            "price of",
            "stock risk",
            "share risk",
            "risk of",
            "risk for",
            "risky",
            "stock information",
            "stock details",
            "stock performance",
            "share performance",
            "performing",
            "analyze",
            "analyse",
            "stock",
            "share",
            "company",
            "information about",
            "details about",
            "tell me about",
            
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

        # Portfolio has priority
        if any(
            keyword in message
            for keyword in portfolio_keywords
        ):
            return self.PORTFOLIO

        # Stock has priority over GENERAL
        if any(
            keyword in message
            for keyword in stock_keywords
        ):
            return self.STOCK

        return self.GENERAL