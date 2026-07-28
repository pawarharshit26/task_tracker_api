from fastapi import APIRouter

from app.apis.v1.block import block_router
from app.apis.v1.commitment import commitment_router
from app.apis.v1.execution_log import log_router
from app.apis.v1.goal import goal_router
from app.apis.v1.history import history_router
from app.apis.v1.phase import phase_router
from app.apis.v1.structure import structure_router
from app.apis.v1.theme import theme_router
from app.apis.v1.today import today_router
from app.apis.v1.track import track_router
from app.apis.v1.user import user_router
from app.apis.v1.vision import vision_router

router = APIRouter(prefix="/v1")

router.include_router(router=user_router, prefix="/user", tags=["User"])
router.include_router(router=vision_router, prefix="/vision", tags=["Vision"])
router.include_router(router=structure_router, prefix="/structure", tags=["Structure"])
router.include_router(router=theme_router, prefix="/theme", tags=["Theme"])
router.include_router(router=track_router, prefix="/track", tags=["Track"])
router.include_router(router=goal_router, prefix="/goal", tags=["Goal"])
router.include_router(router=phase_router, prefix="/phase", tags=["Phase"])
router.include_router(
    router=commitment_router, prefix="/commitment", tags=["Commitment"]
)
router.include_router(router=log_router, prefix="/log", tags=["ExecutionLog"])
router.include_router(router=today_router, prefix="/today", tags=["Today"])
router.include_router(router=history_router, prefix="/history", tags=["History"])
router.include_router(router=block_router, prefix="/block", tags=["Block"])
