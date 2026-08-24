import re

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.schemas.ai import AIChatRequest, AIChatResponse
from app.services.ai_service import AIService
from app.agents.portfolio_tool import PortfolioTool
from app.agents.intent_agent import IntentAgent
from app.agents.stock_tool import StockTool


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

ai_service = AIService()
portfolio_tool = PortfolioTool()
intent_agent = IntentAgent()
stock_tool = StockTool()


def extract_stock_symbol(
    message: str,
) -> str | None:

    words = re.findall(
        r"\b[A-Za-z]{2,20}\b",
        message,
    )

    ignored_words = {
        "what",
        "whats",
        "the",
        "current",
        "price",
        "stock",
        "share",
        "of",
        "is",
        "for",
        "tell",
        "me",
        "about",
        "risk",
        "information",
        "details",
        "how",
        "performing",
        "perform",
        "today",
        "give",
        "please",
        "can",
        "you",
        "could",
        "provide",
        "show",
    }

    for word in words:

        if word.lower() not in ignored_words:
            return word.upper()

    return None


@router.post(
    "/chat",
    response_model=AIChatResponse,
)
def chat_with_ai(
    request: AIChatRequest,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["id"]

    intent = intent_agent.detect_intent(
        request.message
    )

    # -------------------------------------------------
    # PORTFOLIO
    # -------------------------------------------------

    if intent == IntentAgent.PORTFOLIO:

        try:
            analytics = (
                portfolio_tool
                .get_portfolio_analytics(
                    user_id
                )
            )

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=(
                    status.HTTP_503_SERVICE_UNAVAILABLE
                ),
                detail=(
                    f"Unable to retrieve portfolio data: {e}"
                ),
            )

        portfolio_context = f"""
Portfolio data for the authenticated user:

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
"""

        prompt = f"""
You are FinPilot AI, a financial portfolio assistant.

Use ONLY the portfolio data provided below when answering
questions about the user's portfolio.

Do not invent financial numbers, facts, or causes.

If a reason or cause is not present in the data,
do not speculate about it.

If the user asks why something happened and the
provided data does not contain the reason, clearly
say that the available portfolio data does not
provide the reason.

Provide clear, concise explanations.

{portfolio_context}

User question:
{request.message}
"""

    # -------------------------------------------------
    # STOCK
    # -------------------------------------------------

    elif intent == IntentAgent.STOCK:

        symbol = extract_stock_symbol(
            request.message
        )

        if not symbol:
            return {
                "response": (
                    "Please provide the stock symbol "
                    "you want me to analyze."
                )
            }

        try:
            stock_data = stock_tool.get_stock_analysis(
                symbol
            )

        except RuntimeError as e:
            raise HTTPException(
                status_code=(
                    status.HTTP_503_SERVICE_UNAVAILABLE
                ),
                detail=str(e),
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
{request.message}

Answer the user's question clearly and concisely.

If the available data does not contain the reason
for a price movement or performance, do not speculate.
Clearly state that the available data does not provide
the reason.
"""

    # -------------------------------------------------
    # GENERAL
    # -------------------------------------------------

    else:

        prompt = f"""
You are FinPilot AI, a helpful financial assistant.

Answer the user's question clearly and concisely.

Do not invent financial data.

If the question requires the user's personal
portfolio data, explain that portfolio information
requires the appropriate portfolio tool.

User question:
{request.message}
"""        


    response = ai_service.generate_response(
        prompt
    )

    return {
        "response": response,
    }