from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


class BaseEntity(BaseModel):
    pass


class BaseService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
