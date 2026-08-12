from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import JWTError, jwt

from app.config import settings
from app.core.exceptions import InvalidCredentialsException
from app.repositories.user_repository import user_repository


http_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise InvalidCredentialsException()

    except JWTError:
        raise InvalidCredentialsException()

    user = user_repository.get_user_by_id(user_id)

    if user is None:
        raise InvalidCredentialsException()

    return user