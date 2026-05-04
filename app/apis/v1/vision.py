from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.apis.exceptions import BaseAPIException
from app.apis.response import ResponseEntity
from app.dependencies import (
    get_current_user_id,
    get_get_active_vision_interactor,
    get_upsert_vision_interactor,
)
from app.entities.vision import CreateVisionEntity, VisionEntity
from app.interactors.vision.get_active import GetActiveVisionInteractor
from app.interactors.vision.upsert import UpsertVisionInput, UpsertVisionInteractor

vision_router = APIRouter()


@vision_router.get(path="/me", response_model=ResponseEntity[VisionEntity])
async def get_active_vision(
    interactor: Annotated[
        GetActiveVisionInteractor, Depends(get_get_active_vision_interactor)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(input=user_id)
        return ResponseEntity[VisionEntity](data=result)
    except GetActiveVisionInteractor.VisionNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e


@vision_router.put(path="/me", response_model=ResponseEntity[VisionEntity])
async def upsert_vision(
    body: CreateVisionEntity,
    interactor: Annotated[
        UpsertVisionInteractor, Depends(get_upsert_vision_interactor)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    result = await interactor.execute(
        input=UpsertVisionInput(
            user_id=user_id,
            title=body.title,
            description=body.description,
        )
    )
    return ResponseEntity[VisionEntity](data=result)
