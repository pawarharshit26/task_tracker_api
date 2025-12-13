from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

AsyncSessionMaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with AsyncSessionMaker() as session:
        yield session
