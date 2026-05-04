from datetime import date

from app.entities.base import BaseEntity
from app.entities.commitment import CommitmentEntity
from app.interactors.base import BaseInteractor
from app.services.commitment import CommitmentService


class CreateCommitmentInput(BaseEntity):
    user_id: int
    phase_id: int
    commitment_date: date
    intent: str
    expected_minutes: int | None = None


class CreateCommitmentInteractor(
    BaseInteractor[CreateCommitmentInput, CommitmentEntity]
):
    class PhaseNotFoundException(BaseInteractor.InteractorException):
        message = "Phase not found"

    def __init__(self, commitment_service: CommitmentService) -> None:
        self.commitment_service = commitment_service

    async def execute(self, input: CreateCommitmentInput) -> CommitmentEntity:
        try:
            return await self.commitment_service.create(
                user_id=input.user_id,
                phase_id=input.phase_id,
                commitment_date=input.commitment_date,
                intent=input.intent,
                expected_minutes=input.expected_minutes,
            )
        except CommitmentService.PhaseNotFoundException as e:
            raise self.PhaseNotFoundException() from e
