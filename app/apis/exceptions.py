from fastapi import status
from fastapi.responses import JSONResponse

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

    
