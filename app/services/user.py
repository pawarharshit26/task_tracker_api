from datetime import datetime
from typing import Annotated

import structlog
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BaseException
from app.core.security import get_hash
from app.db.base import get_db
from app.db.models.user import User
from app.services.base import BaseEntity, BaseService

logger = structlog.get_logger(__name__)


class UserSignUpEntity(BaseEntity):
    email: EmailStr
    password: str
    name: str


class UserEntity(BaseEntity):
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserService(BaseService):
    class UserException(BaseException):
        message = "User Exception"

    class UserAlreadyExistsException(UserException):
        message = "User Already Exists"

    async def create_user(self, user: UserSignUpEntity) -> UserEntity:
        logger.info("Creating user", email=user.email)

        query = select(User).where(
            User.email == user.email,
            User.is_active.is_(True),
            User.deleted_at.is_(None),
        )
        result = await self.db.execute(query)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            logger.info("User already exists", email=user.email)
            raise self.UserAlreadyExistsException()

        user = User(
            email=user.email,
            name=user.name,
            password=get_hash(user.password),
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        self.db.add(user)
        await self.db.commit() # using autocommit currently
        await self.db.refresh(user)

        logger.info("User created", email=user.email)
        return UserEntity.model_validate(user, from_attributes=True)


def get_user_service(db: Annotated[AsyncSession, Depends(get_db)]) -> UserService:
    return UserService(db)
