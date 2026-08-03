from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import FinPilotException
from app.schemas.response import ApiResponse


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(FinPilotException)
    async def finpilot_exception_handler(
        request: Request,
        exc: FinPilotException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiResponse(
                success=False,
                message=exc.message,
                data=None,
            ).model_dump(),
        )