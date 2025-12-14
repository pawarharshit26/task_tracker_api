import structlog
from fastapi import APIRouter, status, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.apis.response import ResponseEntity
from app.apis.v1.base import router as router_v1

router = APIRouter(prefix="/api")

logger = structlog.get_logger(__name__)


@router.get("/health")
def health(db: Annotated[Session, Depends(get_db)]):
    logger.info("Health check started")
    result = db.execute("SELECT 1")
    logger.info("Health check completed", result=result)
    return ResponseEntity(
        code=status.HTTP_200_OK, message="I am healthy", data={}
    ).to_response()


router.include_router(router_v1)
