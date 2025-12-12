from fastapi import APIRouter, status

from app.apis.response import ResponseEntity
from app.apis.v1.base import router as router_v1

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    return ResponseEntity(
        code=status.HTTP_200_OK, message="I am healthy", data={}
    ).to_response()


router.include_router(router_v1)
