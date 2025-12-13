from typing import Optional, Union

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ResponseEntity(BaseModel):
    code: int = status.HTTP_200_OK
    message: str = ""
    data: Union[dict, BaseModel] = None
    error: Optional[str] = None

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            content=self.model_dump(),
            status_code=self.code,
        )
