from app.core.exceptions import BaseException


class BaseService:
    class BaseServiceException(BaseException):
        pass
