from app.entities.base import BaseEntity
from app.entities.goal import GoalEntity
from app.interactors.base import BaseInteractor
from app.services.goal import GoalService


class CreateGoalInput(BaseEntity):
    user_id: int
    track_id: int
    title: str
    horizon: str | None = None


class CreateGoalInteractor(BaseInteractor[CreateGoalInput, GoalEntity]):
    def __init__(self, goal_service: GoalService) -> None:
        self.goal_service = goal_service

    async def execute(self, input: CreateGoalInput) -> GoalEntity:
        return await self.goal_service.create(
            user_id=input.user_id,
            track_id=input.track_id,
            title=input.title,
            horizon=input.horizon,
        )
