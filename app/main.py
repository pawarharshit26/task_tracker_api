from fastapi import APIRouter, FastAPI
from contextlib import asynccontextmanager

from app.core.db import engine, Base
from app.core.logger import setup_logging, get_logger
from app.user.apis import user_router


setup_logging()
logger = get_logger(__file__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("✅ Database connection successful")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")

    Base.metadata.create_all(engine)  # Create tables (only for SQLite dev mode)
    logger.info("✅ Tables created successfully")

    yield  # 👈 Application runs here

    logger.info("👋 Shutting down... closing resources")


app = FastAPI(lifespan=lifespan)


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user_router)


@api_router.get("/health", tags=["Health"])
def health_check():
    return {"message": "Hello, Welcome to Task Tracker"}


app.include_router(api_router)
