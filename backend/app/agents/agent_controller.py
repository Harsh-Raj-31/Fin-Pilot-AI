from app.agents.intent_agent import IntentAgent
from app.agents.portfolio_tool import PortfolioTool
from app.agents.portfolio_insight_engine import (
    PortfolioInsightEngine,
)
from app.agents.portfolio_decision_engine import (
    PortfolioDecisionEngine,
)
from app.agents.stock_tool import StockTool
from app.agents.stock_symbol_resolver import StockSymbolResolver
from app.agents.query_complexity import QueryComplexity
from app.agents.portfolio_query_type import PortfolioQueryType
from app.agents.recommendation_engine import RecommendationEngine
from app.agents.stock_comparison_engine import StockComparisonEngine
from app.services.ai_service import AIService




class AgentController:

    def __init__(self):

        self.intent_agent = IntentAgent()

        self.portfolio_tool = PortfolioTool()

        self.portfolio_insight_engine = (
            PortfolioInsightEngine()
        )

        self.stock_tool = StockTool()

        self.stock_symbol_resolver = (
            StockSymbolResolver()
        )

        self.ai_service = AIService()

    def handle(
        self,
        user_id: str,
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

            # --------------------------------------------------
            # PORTFOLIO QUERY TYPE
            # --------------------------------------------------

            portfolio_query_type = (
                PortfolioQueryType.detect(
                    message
                )
            )

            print(
                "[AI] Portfolio query type: "
                f"{portfolio_query_type}"
            )


            # ==================================================
            # PORTFOLIO DECISION SUPPORT
            # ==================================================

            if (
                portfolio_query_type
                == PortfolioQueryType.DECISION_SUPPORT
            ):

                decision = (
                    PortfolioDecisionEngine.analyze(
                        analytics
                    )
                )

                response_lines = [
                    "FinPilot Portfolio Decision Support",
                    "",
                    "Overall assessment:",
                    decision["overall_assessment"],
                    "",
                    "Areas needing attention:",
                ]

                if decision["attention_areas"]:

                    for area in (
                        decision["attention_areas"]
                    ):

                        response_lines.append(
                            f"- {area}"
                        )

                else:

                    response_lines.append(
                        "- No major attention areas detected."
                    )

                response_lines.extend(
                    [
                        "",
                        "Positive areas:",
                    ]
                )

                if decision["positive_areas"]:

                    for area in (
                        decision["positive_areas"]
                    ):

                        response_lines.append(
                            f"- {area}"
                        )

                else:

                    response_lines.append(
                        "- No additional positive areas identified."
                    )

                response_lines.extend(
                    [
                        "",
                        "This assessment is based only on "
                        "your portfolio data and FinPilot's "
                        "current analytics model.",
                    ]
                )

                return "\n".join(
                    response_lines
                )

            # ==================================================
            # PORTFOLIO INSIGHTS
            # ==================================================

            if (
                portfolio_query_type
                == PortfolioQueryType.INSIGHTS
            ):

                insight_data = (
                    PortfolioInsightEngine.generate(
                        analytics
                    )
                )

                response_lines = [
                    "FinPilot Portfolio Insights",
                    "",
                ]

                # --------------------------------------------------
                # WARNINGS
                # --------------------------------------------------

                response_lines.append(
                    "Portfolio warnings:"
                )

                if insight_data["warnings"]:

                    for warning in (
                        insight_data["warnings"]
                    ):

                        response_lines.append(
                            f"- {warning}"
                        )

                else:

                    response_lines.append(
                        "- No major portfolio "
                        "warnings detected."
                    )

                # --------------------------------------------------
                # INSIGHTS
                # --------------------------------------------------

                response_lines.extend(
                    [
                        "",
                        "Portfolio insights:",
                    ]
                )

                if insight_data["insights"]:

                    for insight in (
                        insight_data["insights"]
                    ):

                        response_lines.append(
                            f"- {insight}"
                        )

                else:

                    response_lines.append(
                        "- No additional insights "
                        "available."
                    )

                # --------------------------------------------------
                # DISCLAIMER
                # --------------------------------------------------

                response_lines.extend(
                    [
                        "",
                        "These insights are based only "
                        "on your portfolio data and "
                        "FinPilot's current analytics "
                        "model.",
                    ]
                )

                return "\n".join(
                    response_lines
                )

            # ==================================================
            # RETURN
            # ==================================================

            elif (
                portfolio_query_type
                == PortfolioQueryType.RETURN
            ):

                return (
                    "Your portfolio return is "
                    f"{analytics['profit_loss_percentage']:.2f}%."
                )

            # ==================================================
            # CURRENT VALUE
            # ==================================================

            elif (
                portfolio_query_type
                == PortfolioQueryType.VALUE
            ):

                return (
                    "Your current portfolio value is "
                    f"₹{analytics['total_current_value']:.2f}."
                )

            # ==================================================
            # PROFIT / LOSS
            # ==================================================

            elif (
                portfolio_query_type
                == PortfolioQueryType.PROFIT_LOSS
            ):

                profit_loss = (
                    analytics[
                        "total_profit_loss"
                    ]
                )

                if profit_loss > 0:

                    return (
                        f"Your portfolio is currently "
                        f"in profit of ₹{profit_loss:.2f}."
                    )

                elif profit_loss < 0:

                    return (
                        f"Your portfolio is currently "
                        f"in a loss of "
                        f"₹{abs(profit_loss):.2f}."
                    )

                else:

                    return (
                        "Your portfolio is currently "
                        "at break-even."
                    )

            # ==================================================
            # BEST PERFORMER
            # ==================================================

            elif (
                portfolio_query_type
                == PortfolioQueryType.BEST_PERFORMER
            ):

                symbol = (
                    analytics[
                        "best_performer"
                    ]
                )

                return (
                    f"{symbol} is your best-performing "
                    f"holding with a return of "
                    f"{analytics['best_performer_return']:.2f}%."
                )

            # ==================================================
            # WORST PERFORMER
            # ==================================================

            elif (
                portfolio_query_type
                == PortfolioQueryType.WORST_PERFORMER
            ):

                symbol = (
                    analytics[
                        "worst_performer"
                    ]
                )

                return (
                    f"{symbol} is your worst-performing "
                    f"holding with a return of "
                    f"{analytics['worst_performer_return']:.2f}%."
                )

            # ==================================================
            # HIGHEST RISK
            # ==================================================

            elif (
                portfolio_query_type
                == PortfolioQueryType.HIGHEST_RISK
            ):

                symbol = (
                    analytics[
                        "highest_risk_holding"
                    ]
                )

                risk_score = (
                    analytics[
                        "highest_risk_score"
                    ]
                )

                risk_level = (
                    analytics[
                        "highest_risk_level"
                    ]
                )

                return (
                    f"{symbol} is your highest-risk "
                    f"holding with a risk score of "
                    f"{risk_score:.1f} "
                    f"({risk_level})."
                )

            # ==================================================
            # LARGEST HOLDING
            # ==================================================

            elif (
                portfolio_query_type
                == PortfolioQueryType.LARGEST_HOLDING
            ):

                symbol = (
                    analytics[
                        "largest_holding"
                    ]
                )

                allocation = (
                    analytics[
                        "largest_allocation"
                    ]
                )

                return (
                    f"{symbol} is your largest holding, "
                    f"representing "
                    f"{allocation:.2f}% of your "
                    f"portfolio."
                )

            # ==================================================
            # DIVERSIFICATION
            # ==================================================

            elif (
                portfolio_query_type
                == PortfolioQueryType.DIVERSIFICATION
            ):

                return (
                    "Your portfolio is "
                    f"{analytics['diversification_level'].lower()}."
                )

            # ==================================================
            # GENERAL PORTFOLIO ANALYSIS
            # ==================================================

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

8. When explaining portfolio performance, use the
   provided observations when they are relevant.

9. Clearly distinguish between portfolio-level
   information and individual holding-level
   information.

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
{analytics["portfolio_risk_score"]}

Portfolio risk level:
{analytics["portfolio_risk_level"]}

Best performer:
{analytics["best_performer"]}

Best performer return:
{analytics["best_performer_return"]}

Worst performer:
{analytics["worst_performer"]}

Worst performer return:
{analytics["worst_performer_return"]}

Highest risk holding:
{analytics["highest_risk_holding"]}

Highest risk score:
{analytics["highest_risk_score"]}

Highest risk level:
{analytics["highest_risk_level"]}

Largest holding:
{analytics["largest_holding"]}

Largest allocation:
{analytics["largest_allocation"]}%

Diversification:
{analytics["diversification_level"]}

Portfolio observations:
{analytics["observations"]}

Holdings:
{analytics["holdings"]}

Query type:
{query_type}

Portfolio query type:
{portfolio_query_type}

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
- Use observations, risk, performance,
  allocation, and diversification data
  when relevant.
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

                    "Score: "
                    f"{recommendation['score']}/100",

                    "Signal strength: "
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

                        "- Performance: "
                        f"{breakdown['performance']}/20",

                        "- Trend: "
                        f"{breakdown['trend']}/25",

                        "- Momentum: "
                        f"{breakdown['momentum']}/25",

                        "- Risk: "
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

                        "- Return: "
                        f"{metrics['return_percentage']}%",

                        "- RSI: "
                        f"{metrics['rsi_14']}",

                        "- SMA 20: "
                        f"₹{metrics['sma_20']}",

                        "- EMA 20: "
                        f"₹{metrics['ema_20']}",

                        "- MACD: "
                        f"{metrics['macd']}",

                        "- MACD Signal: "
                        f"{metrics['macd_signal']}",

                        "- Risk Score: "
                        f"{metrics['risk_score']}",

                        "- Risk Level: "
                        f"{metrics['risk_level']}",

                        "- Volatility: "
                        f"{metrics['volatility']}",

                        "- Maximum Drawdown: "
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

                # --------------------------------------------------
                # HEADER
                # --------------------------------------------------

                if comparison["winner"] is None:

                    response_lines = [

                        "FinPilot Stock Comparison",

                        "",

                        "Comparison result: "
                        f"{comparison.get('comparison_result', 'SCORE TIE')}",

                        "",

                        "Both stocks have the same "
                        "overall score.",
                    ]

                    if comparison.get(
                        "tie_breaker"
                    ):

                        response_lines.extend(
                            [

                                "",

                                "Metric-based advantage: "
                                f"{comparison['tie_breaker']}",
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

                        "Comparison strength: "
                        f"{comparison['comparison_strength']}",
                    ]

                # --------------------------------------------------
                # METRIC LEADERS
                # --------------------------------------------------

                metric_leaders = (
                    comparison.get(
                        "metric_leaders",
                        {},
                    )
                )

                response_lines.extend(
                    [

                        "",

                        "Metric leaders:",

                        "- Best performance: "
                        f"{metric_leaders.get('best_performance') or 'TIE'}",

                        "- Lowest risk: "
                        f"{metric_leaders.get('lowest_risk') or 'TIE'}",

                        "- Lowest volatility: "
                        f"{metric_leaders.get('lowest_volatility') or 'TIE'}",

                        "- Smallest drawdown: "
                        f"{metric_leaders.get('smallest_drawdown') or 'TIE'}",

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

                            "",

                            f"{stock['symbol']}: "
                            f"{stock['score']}/100",

                            "",

                            "Score breakdown:",

                            "- Performance: "
                            f"{breakdown['performance']}/25",

                            "- Trend: "
                            f"{breakdown['trend']}/25",

                            "- Momentum: "
                            f"{breakdown['momentum']}/25",

                            "- Risk: "
                            f"{breakdown['risk']}/25",

                            "",

                            "Key metrics:",

                            "- Return: "
                            f"{metrics['return_percentage']}%",

                            "- RSI: "
                            f"{metrics['rsi_14']}",

                            "- Risk score: "
                            f"{metrics['risk_score']}",

                            "- Risk level: "
                            f"{metrics['risk_level']}",

                            "- Volatility: "
                            f"{metrics['volatility']}",

                            "- Maximum drawdown: "
                            f"{metrics['maximum_drawdown']}%",

                        ]
                    )

                # --------------------------------------------------
                # OBSERVATIONS
                # --------------------------------------------------

                response_lines.extend(
                    [

                        "",

                        "Key observations:",
                    ]
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