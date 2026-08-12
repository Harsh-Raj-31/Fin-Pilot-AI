from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.repositories.user_repository import user_repository
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.core.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
)


class UserService:     

    def login_user(self, user: UserLogin) -> dict:
       """
       Authenticates a user using email and password.
       """

       existing_user = user_repository.get_user_by_email(
           user.email
       )

       if not existing_user:
           raise InvalidCredentialsException()
       password_valid = verify_password(
           user.password,
           existing_user["password_hash"],
       )

       if not password_valid:
           raise InvalidCredentialsException()

       access_token = create_access_token(
         {
          "sub": existing_user["id"],
         }
         )

       return {
            "access_token": access_token,
            "token_type": "bearer",
        }




    def create_user(self, user: UserCreate) -> UserResponse:
        """
        Creates a new user after checking for duplicate email.
        """

        existing_user = user_repository.get_user_by_email(
            user.email
        )

        if existing_user:
            raise UserAlreadyExistsException(user.email)
                            
        password_hash = hash_password(user.password)

        user_data = {
            "full_name": user.full_name,
            "email": user.email.lower(),
            "password_hash": password_hash,
        }

        created_user = user_repository.create_user(user_data)

        return UserResponse(
            id=created_user["id"],
            full_name=created_user["full_name"],
            email=created_user["email"],
        )


user_service = UserService()