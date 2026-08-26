import re


class StockSymbolResolver:

    STOCK_ALIASES = {
        "TCS": "TCS",
        "TATA CONSULTANCY SERVICES": "TCS",

        "WIPRO": "WIPRO",
        "WIPRO LIMITED": "WIPRO",

        "RELIANCE": "RELIANCE",
        "RELIANCE INDUSTRIES": "RELIANCE",
        "RELIANCE INDUSTRIES LIMITED": "RELIANCE",

        "INFY": "INFY",
        "INFOSYS": "INFY",
        "INFOSYS LIMITED": "INFY",

        "HDFC BANK": "HDFCBANK",
        "HDFC BANK LIMITED": "HDFCBANK",
        "HDFCBANK": "HDFCBANK",

        "ICICI BANK": "ICICIBANK",
        "ICICI BANK LIMITED": "ICICIBANK",
        "ICICIBANK": "ICICIBANK",

        "SBI": "SBIN",
        "STATE BANK OF INDIA": "SBIN",
        "SBIN": "SBIN",

        "ITC": "ITC",

        "LARSEN AND TOUBRO": "LT",
        "L&T": "LT",
        "LT": "LT",

        "BHARTI AIRTEL": "BHARTIARTL",
        "BHARTI AIRTEL LIMITED": "BHARTIARTL",
        "BHARTIARTL": "BHARTIARTL",
    }

    def resolve(
        self,
        message: str,
    ) -> str | None:

        symbols = self.resolve_multiple(
            message
        )

        if not symbols:
            return None

        return symbols[0]

    def resolve_multiple(
        self,
        message: str,
    ) -> list[str]:

        message_upper = (
            message.upper()
            .strip()
        )

        aliases = sorted(
            self.STOCK_ALIASES,
            key=len,
            reverse=True,
        )

        symbols = []

        for alias in aliases:

            pattern = (
                rf"(?<![A-Z0-9])"
                rf"{re.escape(alias)}"
                rf"(?![A-Z0-9])"
            )

            if re.search(
                pattern,
                message_upper,
            ):

                symbol = self.STOCK_ALIASES[
                    alias
                ]

                if symbol not in symbols:
                    symbols.append(symbol)

        return symbols