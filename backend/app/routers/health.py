from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
def health() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "FinPilot AI Backend",
        "version": "1.0.0",
    }