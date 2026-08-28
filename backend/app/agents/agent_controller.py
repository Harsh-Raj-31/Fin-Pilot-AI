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
        # INTENT DETECTION
        # --------------------------------------------------

        intent = self.intent_agent.detect_intent(
            message
        )

        # --------------------------------------------------
        # QUERY COMPLEXITY
        # --------------------------------------------------

        query_type = QueryComplexity.detect(
            message
        )

        print(
            f"[AI] Intent: {intent} | "
            f"Query type: {query_type}"
        )

        # ==================================================
        # PORTFOLIO
        # ==================================================

        if intent == IntentAgent.PORTFOLIO:

            analytics = (
                self.portfolio_tool
                .get_portfolio_analytics(
                    user_id
                )
            )

            prompt = f"""
You are FinPilot AI, a financial portfolio assistant.

Your job is to answer the user's question using
ONLY the portfolio data provided below.

IMPORTANT RULES:

1. Never invent financial numbers or facts.
2. Never use outside knowledge.
3. Never assume information that is not provided.
4. Do not speculate about causes of gains,
   losses, or market movements.
5. If the requested information is not available,
   clearly say that it is not available in the
   provided portfolio data.
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

Query type:
{query_type}

User question:
{message}

Response guidelines:

For a simple question:
- Give a direct answer.
- Keep the response concise.
- Prefer 1-3 sentences.

For a complex question:
- Analyze the provided portfolio data.
- Explain the important factors clearly.
- Organize the answer logically.
- Do not go beyond the available data.
"""

            return self.ai_service.generate_response(
                prompt
            )

        # ==================================================
        # STOCK
        # ==================================================

        elif intent == IntentAgent.STOCK:

            # --------------------------------------------------
            # RESOLVE STOCK SYMBOLS
            # --------------------------------------------------

            symbols = (
                self.stock_symbol_resolver
                .resolve_multiple(
                    message
                )
            )

            if not symbols:

                return (
                    "Please provide the stock symbol "
                    "you want me to analyze."
                )

            # ==================================================
            # STOCK RECOMMENDATION
            # ==================================================

            if (
                query_type
                == QueryComplexity.RECOMMENDATION
            ):

                # Recommendation is currently designed
                # for one stock at a time.

                if len(symbols) > 1:

                    return (
                        "Please ask for a recommendation "
                        "for one stock at a time."
                    )

                symbol = symbols[0]

                # --------------------------------------------------
                # GET STOCK DATA
                # --------------------------------------------------

                stock_data = (
                    self.stock_tool
                    .get_stock_analysis(
                        symbol
                    )
                )

                # --------------------------------------------------
                # RUN RECOMMENDATION ENGINE
                # --------------------------------------------------

                recommendation = (
                    RecommendationEngine.analyze(
                        stock_data
                    )
                )

                breakdown = (
                    recommendation[
                        "breakdown"
                    ]
                )

                metrics = (
                    recommendation[
                        "metrics"
                    ]
                )

                # --------------------------------------------------
                # BUILD RESPONSE
                # --------------------------------------------------

                response_lines = [
                    "FinPilot Recommendation: "
                    f"{recommendation['recommendation']}",

                    "",

                    f"Score: "
                    f"{recommendation['score']}/100",

                    f"Signal strength: "
                    f"{recommendation['signal_strength']}",

                    "",

                    recommendation["summary"],

                    "",

                    "Why this recommendation:",
                ]

                # --------------------------------------------------
                # GENERAL REASONS
                # --------------------------------------------------

                for reason in recommendation[
                    "reasons"
                ]:

                    response_lines.append(
                        f"- {reason}"
                    )

                # --------------------------------------------------
                # POSITIVE FACTORS
                # --------------------------------------------------

                response_lines.extend(
                    [
                        "",
                        "Positive factors:",
                    ]
                )

                if recommendation[
                    "positive_factors"
                ]:

                    for factor in recommendation[
                        "positive_factors"
                    ]:

                        response_lines.append(
                            f"- {factor}"
                        )

                else:

                    response_lines.append(
                        "- None"
                    )

                # --------------------------------------------------
                # NEGATIVE FACTORS
                # --------------------------------------------------

                response_lines.extend(
                    [
                        "",
                        "Negative factors:",
                    ]
                )

                if recommendation[
                    "negative_factors"
                ]:

                    for factor in recommendation[
                        "negative_factors"
                    ]:

                        response_lines.append(
                            f"- {factor}"
                        )

                else:

                    response_lines.append(
                        "- None"
                    )

                # --------------------------------------------------
                # NEUTRAL FACTORS
                # --------------------------------------------------

                response_lines.extend(
                    [
                        "",
                        "Neutral factors:",
                    ]
                )

                if recommendation[
                    "neutral_factors"
                ]:

                    for factor in recommendation[
                        "neutral_factors"
                    ]:

                        response_lines.append(
                            f"- {factor}"
                        )

                else:

                    response_lines.append(
                        "- None"
                    )

                # --------------------------------------------------
                # SCORE BREAKDOWN
                # --------------------------------------------------

                response_lines.extend(
                    [
                        "",
                        "Score breakdown:",

                        f"- Performance: "
                        f"{breakdown['performance']}/20",

                        f"- Trend: "
                        f"{breakdown['trend']}/25",

                        f"- Momentum: "
                        f"{breakdown['momentum']}/25",

                        f"- Risk: "
                        f"{breakdown['risk']}/30",
                    ]
                )

                # --------------------------------------------------
                # KEY METRICS
                # --------------------------------------------------

                response_lines.extend(
                    [
                        "",
                        "Key metrics:",

                        f"- Return: "
                        f"{metrics['return_percentage']}%",

                        f"- RSI: "
                        f"{metrics['rsi_14']}",

                        f"- SMA 20: "
                        f"₹{metrics['sma_20']}",

                        f"- EMA 20: "
                        f"₹{metrics['ema_20']}",

                        f"- MACD: "
                        f"{metrics['macd']}",

                        f"- MACD Signal: "
                        f"{metrics['macd_signal']}",

                        f"- Risk Score: "
                        f"{metrics['risk_score']}",

                        f"- Risk Level: "
                        f"{metrics['risk_level']}",

                        f"- Volatility: "
                        f"{metrics['volatility']}",

                        f"- Maximum Drawdown: "
                        f"{metrics['maximum_drawdown']}%",
                    ]
                )

                return "\n".join(
                    response_lines
                )

            # ==================================================
            # MULTI-STOCK COMPARISON
            # ==================================================

            elif len(symbols) > 1:

                stock_data_list = []

                # --------------------------------------------------
                # GET DATA FOR EACH STOCK
                # --------------------------------------------------

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

                # --------------------------------------------------
                # RUN COMPARISON ENGINE
                # --------------------------------------------------

                comparison = (
                    StockComparisonEngine.compare(
                        stock_data_list
                    )
                )

                # --------------------------------------------------
                # HEADER
                # --------------------------------------------------

                if comparison["winner"] is None:

                    response_lines = [
                        "FinPilot Stock Comparison",
                        "",
                        "Comparison result: TIE",
                        "",
                        "Both stocks have the same overall score.",
                        "",
                    ]

                    if comparison.get("tie_breaker"):

                        response_lines.extend(
                            [
                                "Metric-based advantage: "
                                f"{comparison['tie_breaker']}",
                                "",
                            ]
                        )

                else:

                    response_lines = [
                        "FinPilot Stock Comparison",
                        "",
                        "Overall stronger stock: "
                        f"{comparison['winner']}",
                        "",
                        "Score difference: "
                        f"{comparison['score_difference']} point(s)",
                
                        f"Comparison strength: "
                        f"{comparison['comparison_strength']}",

                        "",
                    ]                
                # --------------------------------------------------
                # METRIC LEADERS
                # --------------------------------------------------

                metric_leaders = comparison.get(
                    "metric_leaders",
                    {}
                )

                response_lines.extend(
                    [
                        "Metric leaders:",
                        f"- Best performance: "
                        f"{metric_leaders.get('best_performance') or 'TIE'}",
                
                        f"- Lowest risk: "
                        f"{metric_leaders.get('lowest_risk') or 'TIE'}",
                
                        f"- Lowest volatility: "
                        f"{metric_leaders.get('lowest_volatility') or 'TIE'}",
                
                        f"- Smallest drawdown: "
                        f"{metric_leaders.get('smallest_drawdown') or 'TIE'}",
                
                        "",
                    ]
                )

                # --------------------------------------------------
                # STOCK RESULTS
                # --------------------------------------------------

                for stock in comparison[
                    "stocks"
                ]:

                    breakdown = (
                        stock["breakdown"]
                    )

                    metrics = (
                        stock["metrics"]
                    )

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

                # --------------------------------------------------
                # OBSERVATIONS
                # --------------------------------------------------

                response_lines.append(
                    "Key observations:"
                )

                for observation in comparison[
                    "observations"
                ]:

                    response_lines.append(
                        f"- {observation}"
                    )

                # --------------------------------------------------
                # DISCLAIMER
                # --------------------------------------------------

                response_lines.extend(
                    [
                        "",
                        "This comparison is based only "
                        "on FinPilot's current scoring "
                        "model and the available "
                        "market data.",
                    ]
                )

                return "\n".join(
                    response_lines
                )

            # ==================================================
            # NORMAL SINGLE-STOCK QUERY
            # ==================================================

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
5. Do not speculate about the reason for a price
   movement or future performance.
6. If the requested information is unavailable,
   clearly state that it is not available.
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

Query type:
{query_type}

User question:
{message}

Response guidelines:

For a simple question:
- Give a direct answer.
- Keep it concise.

For a complex question:
- Analyze the available stock data.
- Explain the relevant metrics.
- Structure the answer clearly.
- Do not go beyond the provided data.
"""

                return self.ai_service.generate_response(
                    prompt
                )

        # ==================================================
        # GENERAL QUERY
        # ==================================================

        else:

            prompt = f"""
You are FinPilot AI, a helpful financial assistant.

Answer the user's question clearly and accurately.

IMPORTANT RULES:

1. Do not invent financial data.
2. Do not claim access to information
   that has not been provided.
3. If the user asks for personal portfolio
   information, explain that portfolio data
   must be retrieved through the portfolio tool.
4. Answer the user's actual question directly.
5. Avoid unnecessary explanations.
6. Do not provide personalized financial advice
   beyond the data and capabilities available
   to FinPilot.

Query type:
{query_type}

User question:
{message}

Response guidelines:

For a simple question:
- Give a short and direct answer.

For a complex question:
- Provide a clear and structured explanation.
- Explain relevant concepts carefully.
"""

            return self.ai_service.generate_response(
                prompt
            )