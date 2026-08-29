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


    def extract_possible_symbol(
        self,
        message: str,
    ) -> str | None:

        message_upper = (
            message.upper()
            .strip()
        )

        # --------------------------------------------------
        # Look for a phrase after common stock commands
        # --------------------------------------------------

        patterns = [
            r"\bANALYZE\s+([A-Z][A-Z0-9&.-]*)",
            r"\bANALYSE\s+([A-Z][A-Z0-9&.-]*)",
            r"\bANALYSIS\s+OF\s+([A-Z][A-Z0-9&.-]*)",
            r"\bSTOCK\s+([A-Z][A-Z0-9&.-]*)",
            r"\bSHARE\s+([A-Z][A-Z0-9&.-]*)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                message_upper,
            )

            if match:

                candidate = (
                    match.group(1)
                    .strip()
                )

                # Ignore generic words.
                if candidate in {
                    "THE",
                    "A",
                    "AN",
                    "STOCK",
                    "SHARE",
                }:
                    continue

                return candidate

        return None
    