from fastapi import Depends, HTTPException
from typing import Annotated
from app.core.jwt import JWT, get_jwt
from app.core.services import BaseService
from app.user.repo import UserModel, UserRepo, get_user_repo
from app.user.schemas import SignupInputSchema, LoginInputSchema, LoginOutputSchema


class UserService(BaseService):
    class UserServiceException(BaseService.BaseServiceException):
        pass

    class UserNotFoundException(UserServiceException):
        pass

    class UserAlreadyExistsException(UserServiceException):
        pass

    def __init__(self, repo: Annotated[UserRepo, Depends(get_user_repo)]):
        self.user_repo = repo

    def get(self, id: str) -> UserModel:
        try:
            return self.user_repo.get(id)
        except UserRepo.UserNotFoundException:
            raise self.UserNotFoundException("User not found")

    def get_by_email(self, email: str) -> UserModel:
        try:
            return self.user_repo.get_by_email(email)
        except UserRepo.UserNotFoundException:
            raise self.UserNotFoundException("User not found")

    def create(self, user: SignupInputSchema) -> str:
        try:
            return self.user_repo.create(user)
        except UserRepo.UserAlreadyExistsException:
            raise self.UserAlreadyExistsException("User already exists")


def get_user_service(repo: Annotated[UserRepo, Depends(get_user_repo)]) -> UserService:
    return UserService(repo=repo)


class AuthService(BaseService):
    class AuthServiceException(BaseService.BaseServiceException):
        pass

    class UserNotFoundException(AuthServiceException):
        pass

    class UserAlreadyExistsException(AuthServiceException):
        pass

    def __init__(
        self,
        user_service: Annotated[UserService, Depends(get_user_service)],
        jwt: Annotated[JWT, Depends(get_jwt)],
    ):
        self.jwt = jwt
        self.user_service = user_service

    def generate_token(self, user: LoginOutputSchema) -> str:
        return self.jwt.encode({"email": user.email})

    def decode_token(self, token: str) -> dict:
        return self.jwt.decode(token)

    def signup(self, user: SignupInputSchema) -> LoginOutputSchema:
        try:
            id = self.user_service.create(user)
            token = self._generate_token(user.email)
            return LoginOutputSchema(
                id=id, name=user.name, email=user.email, token=token
            )
        except UserService.UserAlreadyExistsException:
            raise self.UserAlreadyExistsException("User already exists")

    def login(self, user: LoginInputSchema) -> str:
        try:
            user = self.user_service.get_by_email(user.email)
            if not user:
                raise self.UserNotFoundException("User not found")
            if user.password != user.password:
                raise HTTPException(
                    status_code=401, detail="Incorrect email or password"
                )
            token = self._generate_token(user.email)
            return LoginOutputSchema(
                id=user.id, name=user.name, email=user.email, token=token
            )
        except UserService.UserNotFoundException:
            raise self.UserNotFoundException("User not found")

    def _generate_token(self, email: str) -> str:
        return self.jwt.encode({"email": email})


def get_auth_service(
    jwt: Annotated[JWT, Depends(get_jwt)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> AuthService:
    return AuthService(jwt=jwt, user_service=user_service)
