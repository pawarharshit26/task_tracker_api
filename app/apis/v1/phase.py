from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.apis.exceptions import BaseAPIException
from app.apis.response import ResponseEntity
from app.core.hash_ids import decode
from app.dependencies import (
    get_create_phase_interactor,
    get_current_user_id,
    get_delete_phase_interactor,
    get_update_phase_interactor,
)
from app.entities.phase import CreatePhaseEntity, PhaseEntity, UpdatePhaseEntity
from app.interactors.phase.create import CreatePhaseInput, CreatePhaseInteractor
from app.interactors.phase.delete import DeletePhaseInput, DeletePhaseInteractor
from app.interactors.phase.update import UpdatePhaseInput, UpdatePhaseInteractor

phase_router = APIRouter()


@phase_router.post(
    path="/",
    response_model=ResponseEntity[PhaseEntity],
    status_code=status.HTTP_201_CREATED,
)
async def create_phase(
    body: CreatePhaseEntity,
    interactor: Annotated[CreatePhaseInteractor, Depends(get_create_phase_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=CreatePhaseInput(
                user_id=user_id,
                goal_id=int(body.goal_id),
                title=body.title,
                start_date=body.start_date,
                end_date=body.end_date,
                lifecycle=body.lifecycle,
                outcome=body.outcome,
            )
        )
        return ResponseEntity[PhaseEntity](data=result)
    except CreatePhaseInteractor.GoalNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e


@phase_router.patch(path="/{phase_id}", response_model=ResponseEntity[PhaseEntity])
async def update_phase(
    phase_id: str,
    body: UpdatePhaseEntity,
    interactor: Annotated[UpdatePhaseInteractor, Depends(get_update_phase_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=UpdatePhaseInput(
                user_id=user_id,
                phase_id=decode(phase_id),
                title=body.title,
                start_date=body.start_date,
                end_date=body.end_date,
                lifecycle=body.lifecycle,
                outcome=body.outcome,
            )
        )
        return ResponseEntity[PhaseEntity](data=result)
    except UpdatePhaseInteractor.PhaseNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e
    except UpdatePhaseInteractor.ActivePhaseAlreadyExistsException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_409_CONFLICT
        ) from e


@phase_router.delete(path="/{phase_id}", response_model=ResponseEntity[None])
async def delete_phase(
    phase_id: str,
    interactor: Annotated[DeletePhaseInteractor, Depends(get_delete_phase_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        await interactor.execute(
            input=DeletePhaseInput(user_id=user_id, phase_id=decode(phase_id))
        )
        return ResponseEntity[None](data=None)
    except DeletePhaseInteractor.PhaseNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e
