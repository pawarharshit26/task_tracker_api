from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.apis.exceptions import BaseAPIException
from app.apis.response import ResponseEntity
from app.core.hash_ids import decode
from app.dependencies import (
    get_current_user_id,
    get_upsert_log_interactor,
)
from app.entities.execution_log import CreateExecutionLogEntity, ExecutionLogEntity
from app.interactors.execution_log.upsert import UpsertLogInput, UpsertLogInteractor

log_router = APIRouter()


@log_router.post(
    path="/{commitment_id}",
    response_model=ResponseEntity[ExecutionLogEntity],
    status_code=status.HTTP_201_CREATED,
)
async def upsert_log(
    commitment_id: str,
    body: CreateExecutionLogEntity,
    interactor: Annotated[UpsertLogInteractor, Depends(get_upsert_log_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=UpsertLogInput(
                user_id=user_id,
                commitment_id=decode(commitment_id),
                actual_minutes=body.actual_minutes,
                energy_level=body.energy_level,
                note=body.note,
            )
        )
        return ResponseEntity[ExecutionLogEntity](data=result)
    except UpsertLogInteractor.CommitmentNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e
