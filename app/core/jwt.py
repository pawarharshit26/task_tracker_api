from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

import jwt

from app.core.config import settings
from app.core.exceptions import BaseException


class JWT:
    class JWTException(BaseException):
        pass

    class JWTTokenExpiredException(JWTException):
        pass

    class JWTInvalidTokenException(JWTException):
        pass

    def __init__(self):
        self.algorithm = settings.JWT_ALGORITHM
        self.secret_key = settings.JWT_SECRET
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(
        self,
        subject: Union[dict, Any],
        expires_delta: Optional[timedelta] = None,
        **kwargs,
    ) -> str:
        """
        Create a JWT access token

        Args:
            subject: The subject or data to encode
            expires_delta: Optional timedelta for token expiration
            **kwargs: Additional claims to include in the token

        Returns:
            str: Encoded JWT token
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )

        to_encode = {"exp": expire, "iat": datetime.utcnow(), "sub": subject, **kwargs}

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(
        self, token: str, options: Optional[Dict[str, bool]] = None
    ) -> Dict[str, Any]:
        """
        Decode and validate a JWT token

        Args:
            token: The JWT token to decode
            options: Optional dict of options to pass to PyJWT decode

        Returns:
            Dict containing the token payload

        Raises:
            PyJWTError: If the token is invalid or expired
        """
        if options is None:
            options = {"verify_signature": True, "verify_exp": True}

        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm], options=options
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise self.JWTTokenExpiredException("Token has expired") from None
        except jwt.InvalidTokenError as e:
            raise self.JWTInvalidTokenException(f"Invalid token: {e!s}") from e

    def get_payload(self, token: str) -> dict[str, Any]:
        """Get token payload without signature verification"""
        return self.decode_token(token, options={"verify_signature": False})

    def get_subject(self, token: str) -> str:
        """Get the subject (sub) from a token"""
        payload = self.get_payload(token)
        return payload.get("sub")

    def is_token_expired(self, token: str) -> bool:
        """Check if a token is expired"""
        try:
            self.decode_token(token)
            return False
        except Exception:
            return True
