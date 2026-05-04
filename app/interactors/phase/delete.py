from app.entities.base import BaseEntity
from app.interactors.base import BaseInteractor
from app.services.phase import PhaseService


class DeletePhaseInput(BaseEntity):
    user_id: int
    phase_id: int


class DeletePhaseInteractor(BaseInteractor[DeletePhaseInput, None]):
    class PhaseNotFoundException(BaseInteractor.InteractorException):
        message = "Phase not found"

    def __init__(self, phase_service: PhaseService) -> None:
        self.phase_service = phase_service

    async def execute(self, input: DeletePhaseInput) -> None:
        try:
            await self.phase_service.delete(
                user_id=input.user_id,
                phase_id=input.phase_id,
            )
        except PhaseService.PhaseNotFoundException as e:
            raise self.PhaseNotFoundException() from e
