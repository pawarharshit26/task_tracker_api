from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.exceptions import BaseException


class JWT:
    class JWTException(BaseException):
        pass

    class JWTDecodeException(JWTException):
        pass

    JWT_EXPIRE_MINUTES: int = 10
    ALGORITHM: str = "HS256"

    def encode(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=self.JWT_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=self.ALGORITHM)

    def decode(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            return payload
        except JWTError:
            raise self.JWTDecodeException("Invalid token")


def get_jwt() -> JWT:
    return JWT()
