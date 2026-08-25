from app.agents.intent_agent import IntentAgent
from app.agents.portfolio_tool import PortfolioTool
from app.agents.stock_tool import StockTool
from app.agents.stock_symbol_resolver import (
    StockSymbolResolver,
)
from app.services.ai_service import AIService


class AgentController:

    def __init__(self):
        self.intent_agent = IntentAgent()
        self.portfolio_tool = PortfolioTool()
        self.stock_tool = StockTool()
        self.stock_symbol_resolver = (
            StockSymbolResolver()
        )
        self.ai_service = AIService()


    def handle(
        self,
        user_id: int,
        message: str,
    ) -> str:

        intent = self.intent_agent.detect_intent(
            message
        )

        if intent == IntentAgent.PORTFOLIO:

            analytics = (
                self.portfolio_tool
                .get_portfolio_analytics(
                    user_id
                )
            )

            prompt = f"""
You are FinPilot AI, a financial portfolio assistant.

Use ONLY the portfolio data provided below.

Do not invent financial numbers, facts, or causes.

If a reason or cause is not present in the data,
do not speculate.

Portfolio data:

Total invested: ₹{analytics["total_invested"]:.2f}
Current value: ₹{analytics["total_current_value"]:.2f}
Profit/Loss: ₹{analytics["total_profit_loss"]:.2f}
Return: {analytics["profit_loss_percentage"]:.2f}%

Portfolio risk score: {analytics["portfolio_risk_score"]:.2f}
Portfolio risk level: {analytics["portfolio_risk_level"]}

Best performer: {analytics["best_performer"]}
Worst performer: {analytics["worst_performer"]}
Largest holding: {analytics["largest_holding"]}
Diversification: {analytics["diversification_level"]}

Holdings:
{analytics["holdings"]}

User question:
{message}
"""

        elif intent == IntentAgent.STOCK:

            symbol = (
                self.stock_symbol_resolver
                .resolve(message)
            )

            if not symbol:
                return (
                    "Please provide the stock symbol "
                    "you want me to analyze."
                )

            stock_data = (
                self.stock_tool
                .get_stock_analysis(symbol)
            )

            prompt = f"""
You are FinPilot AI, a financial assistant.

Use ONLY the stock data provided below.

Do not invent additional market data.

Stock market data:
{stock_data["market_data"]}

Stock performance:
{stock_data["performance"]}

Stock risk:
{stock_data["risk"]}

User question:
{message}

Answer the user's question clearly and concisely.

If the available data does not contain the reason
for a price movement or performance, do not speculate.
Clearly state that the available data does not provide
the reason.
"""

        else:

            prompt = f"""
You are FinPilot AI, a helpful financial assistant.

Answer the user's question clearly and concisely.

Do not invent financial data.

If the question requires the user's personal
portfolio data, explain that portfolio information
requires the appropriate portfolio tool.

User question:
{message}
"""

        return self.ai_service.generate_response(
            prompt
        )        