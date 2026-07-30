from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

API_VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 FinPilot AI starting...")
    yield
    print("🛑 FinPilot AI shutting down...")


app = FastAPI(
    title="FinPilot AI API",
    description="Multi-Agent Investment Intelligence Platform",
    version=API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Home"])
def home() -> dict:
    """Root endpoint."""
    return {
        "success": True,
        "message": "Welcome to FinPilot AI 🚀",
        "version": API_VERSION,
    }


@app.get("/health", tags=["Health"])
def health() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "FinPilot AI Backend",
        "version": API_VERSION,
    }
# cd Fin-Pilot-AI\backend
# .venv\Scripts\activate
# python -m uvicorn app.main:app --reload - for activate
