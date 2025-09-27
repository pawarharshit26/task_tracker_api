import uuid
from app.core.db import BaseModel, BaseRepo


class UserModel(BaseModel):
    id: str
    name: str
    email: str
    password: str

    def __init__(self, id: str, name: str, email: str, password: str) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password


FAKE_USER_DB = {}


class UserRepo(BaseRepo):
    class UserRepoException(BaseRepo.BaseRepoException):
        pass

    class UserNotFoundException(UserRepoException):
        pass

    class UserAlreadyExistsException(UserRepoException):
        pass

    def __init__(self):
        self.db = FAKE_USER_DB

    def create(self, user: UserModel) -> str:
        if user.email in self.db:
            raise self.UserAlreadyExistsException("User already exists")
        id = str(uuid.uuid4())
        user = UserModel(
            id=id, name=user.name, email=user.email, password=user.password
        )
        self.db[user.email] = user
        return id

    def get(self, id: str) -> UserModel:
        for user in self.db.values():
            if user.id == id:
                return user
        raise self.UserNotFoundException("User not found")

    def get_by_email(self, email: str) -> UserModel:
        if email not in self.db:
            raise self.UserNotFoundException("User not found")
        return self.db.get(email)


def get_user_repo() -> UserRepo:
    return UserRepo()
