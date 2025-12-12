
from pydantic import  EmailStr
from datetime import datetime


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.services.base import BaseEntity
from app.core.exceptions import BaseException
from app.services.base import BaseService
from app.db.models.user import User
from app.db.base import get_db
from app.core.security import get_hash


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
        query = select(User).where(User.email == user.email, User.is_active == True, User.deleted_at.is_(None))
        result = await self.db.execute(query)
        existing_user = result.scalar_one_or_none()
        if existing_user:
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
        await self.db.commit()
        await self.db.refresh(user)
        return UserEntity.model_validate(user, from_attributes=True)


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)