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
        ]

        if any(
            keyword in message
            for keyword in portfolio_keywords
        ):
            return self.PORTFOLIO

        if any(
            keyword in message
            for keyword in stock_keywords
        ):
            return self.STOCK

        return self.GENERAL