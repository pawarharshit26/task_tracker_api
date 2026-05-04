from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.apis.exceptions import BaseAPIException
from app.apis.response import ResponseEntity
from app.dependencies import (
    get_create_commitment_interactor,
    get_current_user_id,
)
from app.entities.commitment import CommitmentEntity, CreateCommitmentEntity
from app.interactors.commitment.create import (
    CreateCommitmentInput,
    CreateCommitmentInteractor,
)

commitment_router = APIRouter()


@commitment_router.post(
    path="/",
    response_model=ResponseEntity[CommitmentEntity],
    status_code=status.HTTP_201_CREATED,
)
async def create_commitment(
    body: CreateCommitmentEntity,
    interactor: Annotated[
        CreateCommitmentInteractor, Depends(get_create_commitment_interactor)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=CreateCommitmentInput(
                user_id=user_id,
                phase_id=int(body.phase_id),
                commitment_date=body.commitment_date,
                intent=body.intent,
                expected_minutes=body.expected_minutes,
            )
        )
        return ResponseEntity[CommitmentEntity](data=result)
    except CreateCommitmentInteractor.PhaseNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e
