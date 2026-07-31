from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Home"])
def home() -> dict:
    """Root endpoint."""
    return {
        "success": True,
        "message": "Welcome to FinPilot AI 🚀",
        "version": "1.0.0",
    }
