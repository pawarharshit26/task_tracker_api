from datetime import date

from app.core.exceptions import BaseException
from app.db.models.phase import PhaseLifecycle
from app.entities.phase import PhaseEntity
from app.repositories.goal import GoalRepository
from app.repositories.phase import PhaseRepository
from app.services.base import BaseService


class PhaseService(BaseService):
    class PhaseNotFoundException(BaseException):
        message = "Phase not found"

    class GoalNotFoundException(BaseException):
        message = "Goal not found"

    def __init__(self, phase_repo: PhaseRepository, goal_repo: GoalRepository) -> None:
        self.phase_repo = phase_repo
        self.goal_repo = goal_repo

    async def create(
        self,
        user_id: int,
        goal_id: int,
        title: str,
        start_date: date,
        end_date: date,
        lifecycle: PhaseLifecycle,
        outcome: str | None,
    ) -> PhaseEntity:
        goal = await self.goal_repo.get_owned(goal_id=goal_id, user_id=user_id)
        if not goal:
            raise self.GoalNotFoundException()
        return await self.phase_repo.create(
            goal_id=goal_id,
            user_id=user_id,
            title=title,
            start_date=start_date,
            end_date=end_date,
            lifecycle=lifecycle,
            outcome=outcome,
        )

    async def update(
        self,
        user_id: int,
        phase_id: int,
        title: str | None,
        start_date: date | None,
        end_date: date | None,
        lifecycle: PhaseLifecycle | None,
        outcome: str | None,
    ) -> PhaseEntity:
        phase = await self.phase_repo.get_owned(phase_id=phase_id, user_id=user_id)
        if not phase:
            raise self.PhaseNotFoundException()
        return await self.phase_repo.update(
            phase_id=phase_id,
            user_id=user_id,
            title=title,
            start_date=start_date,
            end_date=end_date,
            lifecycle=lifecycle,
            outcome=outcome,
        )

    async def delete(self, user_id: int, phase_id: int) -> None:
        phase = await self.phase_repo.get_owned(phase_id=phase_id, user_id=user_id)
        if not phase:
            raise self.PhaseNotFoundException()
        await self.phase_repo.delete(phase_id=phase_id, user_id=user_id)
