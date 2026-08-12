from fastapi import status


class FinPilotException(Exception):
    """Base exception for the entire FinPilot AI application."""

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class StockNotFoundException(FinPilotException):
    """Raised when a stock symbol cannot be found."""

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, symbol: str):
        super().__init__(f"Stock '{symbol}' not found.")

class UserAlreadyExistsException(FinPilotException):
    """Raised when a user with the email already exists."""

    status_code = status.HTTP_409_CONFLICT

    def __init__(self, email: str):
        super().__init__(
            f"User with email '{email}' already exists."
        )

class StockAlreadyExistsException(FinPilotException):
    """Raised when a stock with the same symbol already exists."""

    status_code = status.HTTP_409_CONFLICT

    def __init__(self, symbol: str):
        super().__init__(f"Stock '{symbol}' already exists.")  

class InvalidCredentialsException(FinPilotException):
    """Raised when authentication credentials are invalid."""

    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self):
        super().__init__("Invalid authentication credentials.")

              