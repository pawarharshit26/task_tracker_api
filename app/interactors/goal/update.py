from app.entities.base import BaseEntity
from app.entities.goal import GoalEntity
from app.interactors.base import BaseInteractor
from app.services.goal import GoalService


class UpdateGoalInput(BaseEntity):
    user_id: int
    goal_id: int
    title: str | None = None
    horizon: str | None = None


class UpdateGoalInteractor(BaseInteractor[UpdateGoalInput, GoalEntity]):
    class GoalNotFoundException(BaseInteractor.InteractorException):
        message = "Goal not found"

    def __init__(self, goal_service: GoalService) -> None:
        self.goal_service = goal_service

    async def execute(self, input: UpdateGoalInput) -> GoalEntity:
        try:
            return await self.goal_service.update(
                user_id=input.user_id,
                goal_id=input.goal_id,
                title=input.title,
                horizon=input.horizon,
            )
        except GoalService.GoalNotFoundException as e:
            raise self.GoalNotFoundException() from e
