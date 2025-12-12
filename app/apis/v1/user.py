from fastapi import APIRouter, Depends

from app.services.user import get_user_service, UserService, UserSignUpEntity, UserEntity
from app.apis.response import ResponseEntity

user_router = APIRouter()


@user_router.post(path = "/signup", response_model = UserEntity)
async def signup(data: UserSignUpEntity, service: UserService = Depends(get_user_service)):
    user = await service.create_user(data)
    return ResponseEntity(data=user).to_response()
    
