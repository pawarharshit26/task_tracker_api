from datetime import date

from app.core.exceptions import BaseException
from app.entities.commitment import CommitmentEntity
from app.repositories.commitment import CommitmentRepository
from app.repositories.phase import PhaseRepository
from app.services.base import BaseService


class CommitmentService(BaseService):
    class PhaseNotFoundException(BaseException):
        message = "Phase not found"

    def __init__(
        self,
        commitment_repo: CommitmentRepository,
        phase_repo: PhaseRepository,
    ) -> None:
        self.commitment_repo = commitment_repo
        self.phase_repo = phase_repo

    async def create(
        self,
        user_id: int,
        phase_id: int,
        commitment_date: date,
        intent: str,
        expected_minutes: int | None,
    ) -> CommitmentEntity:
        phase = await self.phase_repo.get_owned(phase_id=phase_id, user_id=user_id)
        if not phase:
            raise self.PhaseNotFoundException()
        return await self.commitment_repo.create(
            phase_id=phase_id,
            user_id=user_id,
            commitment_date=commitment_date,
            intent=intent,
            expected_minutes=expected_minutes,
        )
