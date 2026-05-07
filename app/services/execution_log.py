from datetime import date

from app.core.exceptions import BaseException
from app.entities.execution_log import ExecutionLogEntity
from app.repositories.commitment import CommitmentRepository
from app.repositories.execution_log import ExecutionLogRepository
from app.services.base import BaseService


class ExecutionLogService(BaseService):
    class CommitmentNotFoundException(BaseException):
        message = "Commitment not found"

    class LogNotEditableException(BaseException):
        message = "Execution logs can only be edited for today's commitments"

    def __init__(
        self,
        log_repo: ExecutionLogRepository,
        commitment_repo: CommitmentRepository,
    ) -> None:
        self.log_repo = log_repo
        self.commitment_repo = commitment_repo

    async def upsert(
        self,
        user_id: int,
        commitment_id: int,
        actual_minutes: int | None,
        energy_level: int | None,
        note: str | None,
    ) -> ExecutionLogEntity:
        commitment = await self.commitment_repo.get_owned(
            commitment_id=commitment_id, user_id=user_id
        )
        if not commitment:
            raise self.CommitmentNotFoundException()
        if commitment.date != date.today():
            raise self.LogNotEditableException()
        existing = await self.log_repo.get_by_commitment_id(commitment_id=commitment_id)
        if existing:
            return await self.log_repo.update(
                log_id=int(existing.id),
                user_id=user_id,
                actual_minutes=actual_minutes,
                energy_level=energy_level,
                note=note,
            )
        return await self.log_repo.create(
            commitment_id=commitment_id,
            user_id=user_id,
            actual_minutes=actual_minutes,
            energy_level=energy_level,
            note=note,
        )
