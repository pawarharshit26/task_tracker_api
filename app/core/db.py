from app.core.exceptions import BaseException


class BaseModel:
    pass


class BaseRepo:
    class BaseRepoException(BaseException):
        pass
