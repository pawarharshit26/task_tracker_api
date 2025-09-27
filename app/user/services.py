from fastapi import Depends, HTTPException
from typing import Annotated
from app.core.jwt import JWT, get_jwt
from app.core.services import BaseService
from app.user.repo import UserRepo, UserRepoEntitiy, get_user_repo
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

    def get(self, id: str) -> UserRepoEntitiy:
        try:
            return self.user_repo.get(id)
        except UserRepo.UserNotFoundException:
            raise self.UserNotFoundException("User not found")

    def get_by_email(self, email: str) -> UserRepoEntitiy:
        try:
            dbUser = self.user_repo.get_by_email(email)

            return UserRepoEntitiy(
                id=dbUser.id,
                name=dbUser.name,
                email=dbUser.email,
                password=dbUser.password,
                created_at=dbUser.created_at,
                updated_at=dbUser.updated_at,
                deleted_at=dbUser.deleted_at,
                is_active=dbUser.is_active,
            )
        except UserRepo.UserNotFoundException:
            raise self.UserNotFoundException("User not found")

    def create(self, user: SignupInputSchema) -> int:
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

    def login(self, data: LoginInputSchema) -> str:
        try:
            dbUser = self.user_service.get_by_email(data.email)
            if not dbUser:
                raise self.UserNotFoundException("User not found")
            if dbUser.password != data.password:
                raise HTTPException(
                    status_code=401, detail="Incorrect email or password"
                )
            token = self._generate_token(data.email)
            return LoginOutputSchema(
                id=dbUser.id, name=dbUser.name, email=dbUser.email, token=token
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
