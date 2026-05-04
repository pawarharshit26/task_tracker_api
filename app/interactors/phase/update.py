from datetime import date

from app.db.models.phase import PhaseLifecycle
from app.entities.base import BaseEntity
from app.entities.phase import PhaseEntity
from app.interactors.base import BaseInteractor
from app.services.phase import PhaseService


class UpdatePhaseInput(BaseEntity):
    user_id: int
    phase_id: int
    title: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    lifecycle: PhaseLifecycle | None = None
    outcome: str | None = None


class UpdatePhaseInteractor(BaseInteractor[UpdatePhaseInput, PhaseEntity]):
    class PhaseNotFoundException(BaseInteractor.InteractorException):
        message = "Phase not found"

    def __init__(self, phase_service: PhaseService) -> None:
        self.phase_service = phase_service

    async def execute(self, input: UpdatePhaseInput) -> PhaseEntity:
        try:
            return await self.phase_service.update(
                user_id=input.user_id,
                phase_id=input.phase_id,
                title=input.title,
                start_date=input.start_date,
                end_date=input.end_date,
                lifecycle=input.lifecycle,
                outcome=input.outcome,
            )
        except PhaseService.PhaseNotFoundException as e:
            raise self.PhaseNotFoundException() from e
