from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from app.user.schemas import LoginOutputSchema, SignupInputSchema, LoginInputSchema
from app.user.services import AuthService, get_auth_service

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post("/signup", response_model=LoginOutputSchema)
async def signup(
    user: SignupInputSchema, service: Annotated[AuthService, Depends(get_auth_service)]
):
    return service.signup(user)


@user_router.post("/login", response_model=LoginOutputSchema)
async def login(
    input: LoginInputSchema, service: Annotated[AuthService, Depends(get_auth_service)]
):
    return service.login(input)
