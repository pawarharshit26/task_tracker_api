from datetime import datetime
from typing import Optional

from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.core.db import BaseEntity, BaseModel, BaseRepo, get_db
from sqlalchemy import Column, String, DateTime, Boolean, Integer, func


class UserModel(BaseModel):
    __tablename__ = "tt_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)


class UserRepoEntitiy(BaseEntity):
    id: Optional[int]
    name: str
    email: str
    password: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    is_active: bool


class UserRepo(BaseRepo):
    class UserRepoException(BaseRepo.BaseRepoException):
        pass

    class UserNotFoundException(UserRepoException):
        pass

    class UserAlreadyExistsException(UserRepoException):
        pass

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserRepoEntitiy) -> str:
        exists = self.db.query(UserModel).filter(UserModel.email == user.email).first()
        if exists is not None:
            raise self.UserAlreadyExistsException("User already exists")
        model = UserModel(name=user.name, email=user.email, password=user.password)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model.id

    def get(self, id: str) -> UserRepoEntitiy:
        user = self.db.get(UserModel, id)
        if user is None:
            raise self.UserNotFoundException("User not found")
        return user

    def get_by_email(self, email: EmailStr) -> UserRepoEntitiy:
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if user is None:
            raise self.UserNotFoundException("User not found")
        return user


def get_user_repo(db: Session = Depends(get_db)) -> UserRepo:
    return UserRepo(db=db)
