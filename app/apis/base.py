from pydantic import BaseModel
from typing import Any, Optional, Union

from fastapi import status, APIRouter, Request
from fastapi.responses import JSONResponse


from app.core.exceptions import BaseException



class ResponseEntity(BaseModel):
    code: int
    message: str = ""
    data: Union[dict, BaseModel] = None
    error: Optional[str] = None

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            content=self.model_dump(),
            status_code=self.code,
        )



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



router = APIRouter()

@router.get("/health")
def health():
    return ResponseEntity(code=status.HTTP_200_OK, message="I am healthy", data={}).to_response()
