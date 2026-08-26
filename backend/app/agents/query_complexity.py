class QueryComplexity:

    SIMPLE = "simple"
    COMPLEX = "complex"

    RECOMMENDATION = "recommendation"

    COMPLEX_KEYWORDS = {
        "analyze",
        "analysis",
        "compare",
        "comparison",
        "recommend",
        "recommendation",
        "strategy",
        "strategies",
        "diversify",
        "diversification",
        "explain why",
        "why",
        "should i",
        "what should",
        "pros and cons",
        "detailed",
        "in detail",
        "deep analysis",
        "risk assessment",
    }

    RECOMMENDATION_KEYWORDS = {
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
    }

    @classmethod
    def detect(
        cls,
        message: str,
    ) -> str:

        normalized = message.lower().strip()

        for keyword in cls.RECOMMENDATION_KEYWORDS:
            if keyword in normalized:
                return cls.RECOMMENDATION

        for keyword in cls.COMPLEX_KEYWORDS:
            if keyword in normalized:
                return cls.COMPLEX

        return cls.SIMPLE