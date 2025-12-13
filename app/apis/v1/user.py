
from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.apis.exceptions import BaseAPIException
from app.apis.response import ResponseEntity
from app.services.user import (
    UserEntity,
    UserService,
    UserSignUpEntity,
    get_user_service,
)

user_router = APIRouter()


@user_router.post(path="/signup", response_model=UserEntity)
async def signup(
    data: UserSignUpEntity, service: Annotated[UserService, Depends(get_user_service)]
):
    try:
        user = await service.create_user(data)
        return ResponseEntity(data=user).to_response()
    except UserService.UserAlreadyExistsException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_400_BAD_REQUEST
        ) from None
