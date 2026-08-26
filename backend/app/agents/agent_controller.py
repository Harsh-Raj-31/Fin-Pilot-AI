from app.agents.intent_agent import IntentAgent
from app.agents.portfolio_tool import PortfolioTool
from app.agents.stock_tool import StockTool
from app.agents.stock_symbol_resolver import StockSymbolResolver
from app.agents.query_complexity import QueryComplexity
from app.agents.recommendation_engine import RecommendationEngine
from app.agents.stock_comparison_engine import StockComparisonEngine
from app.services.ai_service import AIService


class AgentController:

    def __init__(self):
        self.intent_agent = IntentAgent()
        self.portfolio_tool = PortfolioTool()
        self.stock_tool = StockTool()
        self.stock_symbol_resolver = StockSymbolResolver()
        self.ai_service = AIService()

    def handle(
        self,
        user_id: int,
        message: str,
    ) -> str:

        # --------------------------------------------------
        # INTENT AND QUERY TYPE
        # --------------------------------------------------

        intent = self.intent_agent.detect_intent(
            message
        )

        query_type = QueryComplexity.detect(
            message
        )

        print(
            f"[AI] Intent: {intent} | "
            f"Query type: {query_type}"
        )

        # --------------------------------------------------
        # PORTFOLIO
        # --------------------------------------------------

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

IMPORTANT RULES:

1. Never invent financial numbers or facts.
2. Never use outside knowledge.
3. Never assume information that is not provided.
4. Do not speculate about causes of gains or losses.
5. If information is unavailable, clearly say so.
6. Answer the user's actual question directly.
7. Do not provide unnecessary information.

Portfolio data:

Total invested:
₹{analytics["total_invested"]:.2f}

Current value:
₹{analytics["total_current_value"]:.2f}

Profit/Loss:
₹{analytics["total_profit_loss"]:.2f}

Return:
{analytics["profit_loss_percentage"]:.2f}%

Portfolio risk score:
{analytics["portfolio_risk_score"]:.2f}

Portfolio risk level:
{analytics["portfolio_risk_level"]}

Best performer:
{analytics["best_performer"]}

Worst performer:
{analytics["worst_performer"]}

Largest holding:
{analytics["largest_holding"]}

Diversification:
{analytics["diversification_level"]}

Holdings:
{analytics["holdings"]}

User question:
{message}

Answer clearly and concisely.
"""

            return self.ai_service.generate_response(
                prompt
            )

        # --------------------------------------------------
        # STOCK
        # --------------------------------------------------

        elif intent == IntentAgent.STOCK:

            symbols = (
                self.stock_symbol_resolver
                .resolve_multiple(message)
            )

            if not symbols:
                return (
                    "Please provide the stock symbol "
                    "you want me to analyze."
                )

            # --------------------------------------------------
            # BUY / HOLD / SELL RECOMMENDATION
            # --------------------------------------------------

            if (
                query_type
                == QueryComplexity.RECOMMENDATION
            ):

                if len(symbols) > 1:
                    return (
                        "Please ask for a recommendation "
                        "for one stock at a time."
                    )

                symbol = symbols[0]

                stock_data = (
                    self.stock_tool
                    .get_stock_analysis(
                        symbol
                    )
                )

                recommendation = (
                    RecommendationEngine.analyze(
                        stock_data
                    )
                )

                breakdown = recommendation[
                    "breakdown"
                ]

                metrics = recommendation[
                    "metrics"
                ]

                return (
                    f"FinPilot Recommendation: "
                    f"{recommendation['recommendation']}\n\n"
                    f"Score: "
                    f"{recommendation['score']}/100\n\n"
                    f"Score breakdown:\n"
                    f"- Performance: "
                    f"{breakdown['performance']}/20\n"
                    f"- Trend: "
                    f"{breakdown['trend']}/25\n"
                    f"- Momentum: "
                    f"{breakdown['momentum']}/25\n"
                    f"- Risk: "
                    f"{breakdown['risk']}/30\n\n"
                    f"Key metrics:\n"
                    f"- Return: "
                    f"{metrics['return_percentage']}%\n"
                    f"- RSI: "
                    f"{metrics['rsi_14']}\n"
                    f"- SMA 20: "
                    f"₹{metrics['sma_20']}\n"
                    f"- EMA 20: "
                    f"₹{metrics['ema_20']}\n"
                    f"- MACD: "
                    f"{metrics['macd']}\n"
                    f"- MACD Signal: "
                    f"{metrics['macd_signal']}\n"
                    f"- Risk Score: "
                    f"{metrics['risk_score']}\n"
                    f"- Risk Level: "
                    f"{metrics['risk_level']}\n"
                    f"- Volatility: "
                    f"{metrics['volatility']}\n"
                    f"- Maximum Drawdown: "
                    f"{metrics['maximum_drawdown']}%"
                )

            # --------------------------------------------------
            # MULTI-STOCK COMPARISON
            # --------------------------------------------------

            elif len(symbols) > 1:

                stock_data_list = []

                for symbol in symbols:

                    stock_data = (
                        self.stock_tool
                        .get_stock_analysis(
                            symbol
                        )
                    )

                    stock_data_list.append(
                        stock_data
                    )

                comparison = (
                    StockComparisonEngine.compare(
                        stock_data_list
                    )
                )

                response_lines = [
                    "FinPilot Stock Comparison",
                    "",
                    f"Overall stronger stock: "
                    f"{comparison['winner']}",
                    "",
                ]

                for stock in comparison["stocks"]:

                    breakdown = stock[
                        "breakdown"
                    ]

                    metrics = stock[
                        "metrics"
                    ]

                    response_lines.extend(
                        [
                            f"{stock['symbol']}: "
                            f"{stock['score']}/100",
                            "",
                            "Score breakdown:",
                            f"- Performance: "
                            f"{breakdown['performance']}/25",
                            f"- Trend: "
                            f"{breakdown['trend']}/25",
                            f"- Momentum: "
                            f"{breakdown['momentum']}/25",
                            f"- Risk: "
                            f"{breakdown['risk']}/25",
                            "",
                            "Key metrics:",
                            f"- Return: "
                            f"{metrics['return_percentage']}%",
                            f"- RSI: "
                            f"{metrics['rsi_14']}",
                            f"- Risk score: "
                            f"{metrics['risk_score']}",
                            f"- Risk level: "
                            f"{metrics['risk_level']}",
                            f"- Volatility: "
                            f"{metrics['volatility']}",
                            f"- Maximum drawdown: "
                            f"{metrics['maximum_drawdown']}%",
                            "",
                        ]
                    )

                response_lines.append(
                    "This comparison is based only "
                    "on FinPilot's current scoring model "
                    "and the available market data."
                )

                return "\n".join(
                    response_lines
                )

            # --------------------------------------------------
            # NORMAL SINGLE-STOCK QUERY
            # --------------------------------------------------

            else:

                symbol = symbols[0]

                stock_data = (
                    self.stock_tool
                    .get_stock_analysis(
                        symbol
                    )
                )

                prompt = f"""
You are FinPilot AI, a financial assistant.

Use ONLY the stock data provided below.

IMPORTANT RULES:

1. Never invent market data.
2. Never use outside knowledge.
3. Never invent prices, returns, risk values,
   or financial metrics.
4. Do not assume information that is not provided.
5. Do not speculate about price movements.
6. If information is unavailable, say so clearly.
7. Answer the user's actual question directly.
8. Do not provide unnecessary information.

Stock data:

Market data:
{stock_data["market_data"]}

Performance:
{stock_data["performance"]}

Risk:
{stock_data["risk"]}

Technical indicators:
{stock_data["indicators"]}

User question:
{message}

Answer clearly and concisely.
"""

        # --------------------------------------------------
        # GENERAL QUERY
        # --------------------------------------------------

        else:

            prompt = f"""
You are FinPilot AI, a helpful financial assistant.

Answer the user's question clearly and accurately.

IMPORTANT RULES:

1. Do not invent financial data.
2. Do not claim access to unavailable information.
3. If personal portfolio information is requested,
   explain that portfolio data requires the
   portfolio tool.
4. Answer the user's actual question directly.
5. Avoid unnecessary explanations.

User question:
{message}

Answer clearly and concisely.
"""

        # --------------------------------------------------
        # LLM RESPONSE
        # --------------------------------------------------

        return self.ai_service.generate_response(
            prompt
        )