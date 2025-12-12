from pydantic import BaseModel

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db


class BaseEntity(BaseModel):
    pass


class BaseService:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db
