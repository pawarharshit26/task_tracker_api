from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.response import ResponseEntity
from app.apis.v1.base import router as router_v1
from app.db.base import get_db

router = APIRouter(prefix="/api")

logger = structlog.get_logger(__name__)


@router.get("/health")
async def health(db: Annotated[AsyncSession, Depends(get_db)]):
    logger.info("Health check started")
    await db.execute(text("SELECT 1"))
    logger.info("Health check completed, database connected successfully")
    return ResponseEntity(code=status.HTTP_200_OK, message="I am healthy", data={})


router.include_router(router_v1)
