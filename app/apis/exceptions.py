from app.core.exceptions import BaseException
from fastapi import status  
from app.apis.response import ResponseEntity
from fastapi.responses import JSONResponse


class BaseAPIException(BaseException):
    code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Something went wrong"

    def __init__(self, message: str = None, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.code = status_code
        super().__init__(message=message)

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.code,
            content=ResponseEntity(code=self.code, message=self.message, error=self.message).model_dump()
        )
