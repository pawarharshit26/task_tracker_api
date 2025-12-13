from fastapi import status

from app.apis.response import ResponseEntity
from app.core.exceptions import BaseException


class BaseAPIException(BaseException):
    code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Something went wrong"

    def __init__(
        self,
        message: str | None = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        self.code = status_code
        super().__init__(message=message)

    def to_response(self):
        return ResponseEntity(
            code=self.code,
            message=self.message,
            data=None,
            error=str(self),
        ).to_response()


class UnauthorizedException(BaseAPIException):
    message: str = "Unauthorized access"

    def __init__(self, message: str | None = None):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)
