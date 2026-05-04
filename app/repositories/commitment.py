from datetime import date, datetime
from typing import NamedTuple

from sqlalchemy import select

from app.db.models.daily_commitment import DailyCommitment
from app.db.models.goal import Goal
from app.db.models.phase import Phase
from app.db.models.theme import Theme
from app.db.models.track import Track
from app.db.models.vision import Vision
from app.entities.breadcrumb import BreadcrumbEntity
from app.entities.commitment import CommitmentEntity
from app.repositories.base import BaseRepository


def _to_entity(c: DailyCommitment) -> CommitmentEntity:
    return CommitmentEntity(
        id=c.id,
        phase_id=c.phase_id,
        date=c.commitment_date,
        intent=c.intent,
        expected_minutes=c.expected_minutes,
        mve_minutes=c.mve_minutes,
    )


class _CommitmentRow(NamedTuple):
    commitment: CommitmentEntity
    breadcrumb: BreadcrumbEntity


class CommitmentRepository(BaseRepository):
    async def list_by_date(self, user_id: int, for_date: date) -> list[_CommitmentRow]:
        result = await self.db.execute(
            select(DailyCommitment, Track, Theme)
            .join(Phase, DailyCommitment.phase_id == Phase.id)
            .join(Goal, Phase.goal_id == Goal.id)
            .join(Track, Goal.track_id == Track.id)
            .join(Theme, Track.theme_id == Theme.id)
            .join(Vision, Theme.vision_id == Vision.id)
            .where(
                Vision.user_id == user_id,
                DailyCommitment.commitment_date == for_date,
                Vision.deleted_at.is_(None),
                Theme.deleted_at.is_(None),
                Track.deleted_at.is_(None),
                Goal.deleted_at.is_(None),
                Phase.deleted_at.is_(None),
                DailyCommitment.deleted_at.is_(None),
            )
        )
        rows = result.all()
        return [
            _CommitmentRow(
                commitment=_to_entity(commitment),
                breadcrumb=BreadcrumbEntity(
                    theme_preset_key=theme.preset_key,
                    theme_name=theme.name,
                    track_name=track.name,
                ),
            )
            for commitment, track, theme in rows
        ]

    async def get_owned(
        self, commitment_id: int, user_id: int
    ) -> CommitmentEntity | None:
        result = await self.db.execute(
            select(DailyCommitment)
            .join(Phase, DailyCommitment.phase_id == Phase.id)
            .join(Goal, Phase.goal_id == Goal.id)
            .join(Track, Goal.track_id == Track.id)
            .join(Theme, Track.theme_id == Theme.id)
            .join(Vision, Theme.vision_id == Vision.id)
            .where(
                Vision.user_id == user_id,
                DailyCommitment.id == commitment_id,
                Vision.deleted_at.is_(None),
                Theme.deleted_at.is_(None),
                Track.deleted_at.is_(None),
                Goal.deleted_at.is_(None),
                Phase.deleted_at.is_(None),
                DailyCommitment.deleted_at.is_(None),
            )
        )
        c = result.scalar_one_or_none()
        return _to_entity(c) if c else None

    async def list_by_date_range(
        self, user_id: int, from_date: date, to_date: date
    ) -> list[_CommitmentRow]:
        result = await self.db.execute(
            select(DailyCommitment, Track, Theme, Goal)
            .join(Phase, DailyCommitment.phase_id == Phase.id)
            .join(Goal, Phase.goal_id == Goal.id)
            .join(Track, Goal.track_id == Track.id)
            .join(Theme, Track.theme_id == Theme.id)
            .join(Vision, Theme.vision_id == Vision.id)
            .where(
                Vision.user_id == user_id,
                DailyCommitment.commitment_date >= from_date,
                DailyCommitment.commitment_date <= to_date,
                Vision.deleted_at.is_(None),
                Theme.deleted_at.is_(None),
                Track.deleted_at.is_(None),
                Goal.deleted_at.is_(None),
                Phase.deleted_at.is_(None),
                DailyCommitment.deleted_at.is_(None),
            )
        )
        rows = result.all()
        return [
            _CommitmentRow(
                commitment=_to_entity(commitment),
                breadcrumb=BreadcrumbEntity(
                    theme_preset_key=theme.preset_key,
                    theme_name=theme.name,
                    track_name=track.name,
                    goal_title=goal.title,
                ),
            )
            for commitment, track, theme, goal in rows
        ]

    async def create(
        self,
        phase_id: int,
        user_id: int,
        commitment_date: date,
        intent: str,
        expected_minutes: int | None,
    ) -> CommitmentEntity:
        mve_minutes = (
            max(5, round(expected_minutes / 3))
            if expected_minutes is not None
            else None
        )
        now = datetime.utcnow()
        c = DailyCommitment(
            phase_id=phase_id,
            commitment_date=commitment_date,
            intent=intent,
            expected_minutes=expected_minutes,
            mve_minutes=mve_minutes,
            created_at=now,
            updated_at=now,
            creator_id=user_id,
            updater_id=user_id,
        )
        self.db.add(c)
        await self.db.commit()
        await self.db.refresh(c)
        return _to_entity(c)
