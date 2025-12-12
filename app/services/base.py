from fastapi import Depends
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db


class BaseEntity(BaseModel):
    pass


class BaseService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
