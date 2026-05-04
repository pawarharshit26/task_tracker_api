from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.apis.exceptions import BaseAPIException
from app.apis.response import ResponseEntity
from app.core.hash_ids import decode
from app.dependencies import (
    get_create_track_interactor,
    get_current_user_id,
    get_delete_track_interactor,
    get_update_track_interactor,
)
from app.entities.track import CreateTrackEntity, TrackEntity, UpdateTrackEntity
from app.interactors.track.create import CreateTrackInput, CreateTrackInteractor
from app.interactors.track.delete import DeleteTrackInput, DeleteTrackInteractor
from app.interactors.track.update import UpdateTrackInput, UpdateTrackInteractor

track_router = APIRouter()


@track_router.post(
    path="/",
    response_model=ResponseEntity[TrackEntity],
    status_code=status.HTTP_201_CREATED,
)
async def create_track(
    body: CreateTrackEntity,
    interactor: Annotated[CreateTrackInteractor, Depends(get_create_track_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=CreateTrackInput(
                user_id=user_id,
                theme_id=int(body.theme_id),
                name=body.name,
                description=body.description,
                cadence_per_week=body.cadence_per_week,
            )
        )
        return ResponseEntity[TrackEntity](data=result)
    except CreateTrackInteractor.ThemeNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e


@track_router.patch(path="/{track_id}", response_model=ResponseEntity[TrackEntity])
async def update_track(
    track_id: str,
    body: UpdateTrackEntity,
    interactor: Annotated[UpdateTrackInteractor, Depends(get_update_track_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=UpdateTrackInput(
                user_id=user_id,
                track_id=decode(track_id),
                name=body.name,
                description=body.description,
                cadence_per_week=body.cadence_per_week,
                is_active=body.is_active,
            )
        )
        return ResponseEntity[TrackEntity](data=result)
    except UpdateTrackInteractor.TrackNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e


@track_router.delete(path="/{track_id}", response_model=ResponseEntity[None])
async def delete_track(
    track_id: str,
    interactor: Annotated[DeleteTrackInteractor, Depends(get_delete_track_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        await interactor.execute(
            input=DeleteTrackInput(user_id=user_id, track_id=decode(track_id))
        )
        return ResponseEntity[None](data=None)
    except DeleteTrackInteractor.TrackNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e
