from app.entities.base import BaseEntity
from app.interactors.base import BaseInteractor
from app.services.goal import GoalService


class DeleteGoalInput(BaseEntity):
    user_id: int
    goal_id: int


class DeleteGoalInteractor(BaseInteractor[DeleteGoalInput, None]):
    class GoalNotFoundException(BaseInteractor.InteractorException):
        message = "Goal not found"

    def __init__(self, goal_service: GoalService) -> None:
        self.goal_service = goal_service

    async def execute(self, input: DeleteGoalInput) -> None:
        try:
            await self.goal_service.delete(
                user_id=input.user_id,
                goal_id=input.goal_id,
            )
        except GoalService.GoalNotFoundException as e:
            raise self.GoalNotFoundException() from e
