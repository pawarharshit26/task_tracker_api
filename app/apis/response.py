from typing import Generic, Optional, TypeVar

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")


class ResponseEntity(BaseModel, Generic[T]):
    code: int = status.HTTP_200_OK
    message: str = ""
    data: Optional[T] = None
    error: Optional[str] = None

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            content=self.model_dump(),
            status_code=self.code,
        )
