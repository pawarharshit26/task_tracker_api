from app.entities.base import BaseEntity
from app.entities.execution_log import ExecutionLogEntity
from app.interactors.base import BaseInteractor
from app.services.execution_log import ExecutionLogService


class UpsertLogInput(BaseEntity):
    user_id: int
    commitment_id: int
    actual_minutes: int | None = None
    energy_level: int | None = None
    note: str | None = None


class UpsertLogInteractor(BaseInteractor[UpsertLogInput, ExecutionLogEntity]):
    class CommitmentNotFoundException(BaseInteractor.InteractorException):
        message = "Commitment not found"

    class LogNotEditableException(BaseInteractor.InteractorException):
        message = "Execution logs can only be edited for today's commitments"

    def __init__(self, log_service: ExecutionLogService) -> None:
        self.log_service = log_service

    async def execute(self, input: UpsertLogInput) -> ExecutionLogEntity:
        try:
            return await self.log_service.upsert(
                user_id=input.user_id,
                commitment_id=input.commitment_id,
                actual_minutes=input.actual_minutes,
                energy_level=input.energy_level,
                note=input.note,
            )
        except ExecutionLogService.CommitmentNotFoundException as e:
            raise self.CommitmentNotFoundException() from e
        except ExecutionLogService.LogNotEditableException as e:
            raise self.LogNotEditableException() from e
