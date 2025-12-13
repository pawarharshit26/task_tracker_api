from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.apis.exceptions import BaseAPIException
from app.apis.response import ResponseEntity
from app.services.user import (
    UserService,
    UserSignInEntity,
    UserSignUpEntity,
    UserTokenEntity,
    get_user_service,
)

user_router = APIRouter()


@user_router.post(path="/signup", response_model=UserTokenEntity)
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


@user_router.post(path="/signin", response_model=UserTokenEntity)
async def signin(
    data: UserSignInEntity, service: Annotated[UserService, Depends(get_user_service)]
):
    try:
        user = await service.sign_in(data)
        return ResponseEntity(data=user).to_response()
    except UserService.UserInvalidPasswordException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_401_UNAUTHORIZED
        ) from None
    except UserService.UserNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from None
    except UserService.UserException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_400_BAD_REQUEST
        ) from None
