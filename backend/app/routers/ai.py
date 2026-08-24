from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.schemas.ai import AIChatRequest, AIChatResponse
from app.services.ai_service import AIService
from app.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

ai_service = AIService()
portfolio_analytics_service = PortfolioAnalyticsService()


@router.post(
    "/chat",
    response_model=AIChatResponse,
)
def chat_with_ai(
    request: AIChatRequest,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["id"]

    try:
        analytics = (
            portfolio_analytics_service
            .calculate_portfolio_analytics(
                user_id
            )
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to retrieve portfolio data: {e}",
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

Use only information explicitly provided in the
portfolio data.

If a reason or cause is not present in the data,
do not speculate about it.

If the user asks why something happened and the
provided data does not contain the reason, clearly
say that the available portfolio data does not
provide the reason.

If the user asks something unrelated to the portfolio,
answer normally.

Provide clear, concise explanations.

{portfolio_context}

User question:
{request.message}
"""

    response = ai_service.generate_response(
        prompt
    )

    return {
        "response": response,
    }