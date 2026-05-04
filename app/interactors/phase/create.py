from datetime import date

from app.db.models.phase import PhaseLifecycle
from app.entities.base import BaseEntity
from app.entities.phase import PhaseEntity
from app.interactors.base import BaseInteractor
from app.services.phase import PhaseService


class CreatePhaseInput(BaseEntity):
    user_id: int
    goal_id: int
    title: str
    start_date: date
    end_date: date
    lifecycle: PhaseLifecycle = PhaseLifecycle.DRAFT
    outcome: str | None = None


class CreatePhaseInteractor(BaseInteractor[CreatePhaseInput, PhaseEntity]):
    class GoalNotFoundException(BaseInteractor.InteractorException):
        message = "Goal not found"

    def __init__(self, phase_service: PhaseService) -> None:
        self.phase_service = phase_service

    async def execute(self, input: CreatePhaseInput) -> PhaseEntity:
        try:
            return await self.phase_service.create(
                user_id=input.user_id,
                goal_id=input.goal_id,
                title=input.title,
                start_date=input.start_date,
                end_date=input.end_date,
                lifecycle=input.lifecycle,
                outcome=input.outcome,
            )
        except PhaseService.GoalNotFoundException as e:
            raise self.GoalNotFoundException() from e
