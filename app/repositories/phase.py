from datetime import date, datetime

from sqlalchemy import select

from app.db.models.goal import Goal
from app.db.models.phase import Phase, PhaseLifecycle
from app.db.models.theme import Theme
from app.db.models.track import Track
from app.db.models.vision import Vision
from app.entities.phase import PhaseEntity
from app.repositories.base import BaseRepository


def _to_entity(p: Phase) -> PhaseEntity:
    return PhaseEntity(
        id=p.id,
        goal_id=p.goal_id,
        title=p.title,
        start_date=p.start_date,
        end_date=p.end_date,
        lifecycle=p.lifecycle,
        outcome=p.outcome,
    )


class PhaseRepository(BaseRepository):
    async def list(self, user_id: int, goal_id: int) -> list[PhaseEntity]:
        result = await self.db.execute(
            select(Phase)
            .join(Goal, Phase.goal_id == Goal.id)
            .join(Track, Goal.track_id == Track.id)
            .join(Theme, Track.theme_id == Theme.id)
            .join(Vision, Theme.vision_id == Vision.id)
            .where(
                Vision.user_id == user_id,
                Phase.goal_id == goal_id,
                Vision.deleted_at.is_(None),
                Theme.deleted_at.is_(None),
                Track.deleted_at.is_(None),
                Goal.deleted_at.is_(None),
                Phase.deleted_at.is_(None),
            )
        )
        return [_to_entity(p) for p in result.scalars().all()]

    async def get_owned(self, phase_id: int, user_id: int) -> PhaseEntity | None:
        result = await self.db.execute(
            select(Phase)
            .join(Goal, Phase.goal_id == Goal.id)
            .join(Track, Goal.track_id == Track.id)
            .join(Theme, Track.theme_id == Theme.id)
            .join(Vision, Theme.vision_id == Vision.id)
            .where(
                Vision.user_id == user_id,
                Phase.id == phase_id,
                Vision.deleted_at.is_(None),
                Theme.deleted_at.is_(None),
                Track.deleted_at.is_(None),
                Goal.deleted_at.is_(None),
                Phase.deleted_at.is_(None),
            )
        )
        p = result.scalar_one_or_none()
        return _to_entity(p) if p else None

    async def create(
        self,
        goal_id: int,
        user_id: int,
        title: str,
        start_date: date,
        end_date: date,
        lifecycle: PhaseLifecycle,
        outcome: str | None,
    ) -> PhaseEntity:
        now = datetime.utcnow()
        p = Phase(
            goal_id=goal_id,
            title=title,
            start_date=start_date,
            end_date=end_date,
            lifecycle=lifecycle,
            outcome=outcome,
            created_at=now,
            updated_at=now,
            creator_id=user_id,
            updater_id=user_id,
        )
        self.db.add(p)
        await self.db.commit()
        await self.db.refresh(p)
        return _to_entity(p)

    async def update(
        self,
        phase_id: int,
        user_id: int,
        title: str | None,
        start_date: date | None,
        end_date: date | None,
        lifecycle: PhaseLifecycle | None,
        outcome: str | None,
    ) -> PhaseEntity:
        result = await self.db.execute(
            select(Phase).where(Phase.id == phase_id, Phase.deleted_at.is_(None))
        )
        p = result.scalar_one()
        if title is not None:
            p.title = title
        if start_date is not None:
            p.start_date = start_date
        if end_date is not None:
            p.end_date = end_date
        if lifecycle is not None:
            p.lifecycle = lifecycle
        if outcome is not None:
            p.outcome = outcome
        p.updated_at = datetime.utcnow()
        p.updater_id = user_id
        await self.db.commit()
        await self.db.refresh(p)
        return _to_entity(p)

    async def delete(self, phase_id: int, user_id: int) -> None:
        result = await self.db.execute(
            select(Phase).where(Phase.id == phase_id, Phase.deleted_at.is_(None))
        )
        p = result.scalar_one()
        p.deleted_at = datetime.utcnow()
        p.deleter_id = user_id
        await self.db.commit()
