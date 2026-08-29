from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.schemas.ai import AIChatRequest, AIChatResponse
from app.agents.agent_controller import AgentController


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


agent_controller = AgentController()


@router.post(
    "/chat",
    response_model=AIChatResponse,
)
def chat_with_ai(
    request: AIChatRequest,
    current_user: dict = Depends(get_current_user),
):

    user_id = current_user["id"]

    response = agent_controller.handle(
        user_id=user_id,
        message=request.message,
    )

    return {
        "response": response,
    }