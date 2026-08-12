from fastapi import APIRouter

from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.user_service import user_service
from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=UserResponse,
)

@router.post("/login")
def login_user(user: UserLogin) -> dict:
    return user_service.login_user(user)

def register_user(user: UserCreate) -> UserResponse:
    return user_service.create_user(user)

@router.get("/me")
def get_current_user_info(
    current_user: dict = Depends(get_current_user),
) -> dict:
    return {
        "id": current_user["id"],
        "full_name": current_user["full_name"],
        "email": current_user["email"],
    }