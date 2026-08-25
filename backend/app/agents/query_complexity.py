class QueryComplexity:

    SIMPLE = "simple"
    COMPLEX = "complex"

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

    @classmethod
    def detect(
        cls,
        message: str,
    ) -> str:

        normalized = message.lower().strip()

        for keyword in cls.COMPLEX_KEYWORDS:

            if keyword in normalized:
                return cls.COMPLEX

        return cls.SIMPLE