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
            "diversification",
            "allocation",
            "portfolio risk",
        ]

        stock_keywords = [
            "stock price",
            "share price",
            "current price",
            "stock risk",
            "share risk",
            "risk of",
            "risk for",
            "stock information",
            "stock details",
            "stock performance",
            "share performance",
            "information about",
            "performing",
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