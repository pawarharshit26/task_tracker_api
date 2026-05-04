from datetime import datetime

from sqlalchemy import select

from app.db.models.execution_log import ExecutionLog
from app.entities.execution_log import ExecutionLogEntity
from app.repositories.base import BaseRepository


def _to_entity(e: ExecutionLog) -> ExecutionLogEntity:
    return ExecutionLogEntity(
        id=e.id,
        commitment_id=e.commitment_id,
        actual_minutes=e.actual_minutes,
        energy_level=e.energy_level,
        note=e.note,
    )


class ExecutionLogRepository(BaseRepository):
    async def get_by_commitment_ids(
        self, commitment_ids: list[int]
    ) -> dict[int, ExecutionLogEntity]:
        if not commitment_ids:
            return {}
        result = await self.db.execute(
            select(ExecutionLog).where(
                ExecutionLog.commitment_id.in_(commitment_ids),
                ExecutionLog.deleted_at.is_(None),
            )
        )
        return {e.commitment_id: _to_entity(e) for e in result.scalars().all()}

    async def create(
        self,
        commitment_id: int,
        user_id: int,
        actual_minutes: int | None,
        energy_level: int | None,
        note: str | None,
    ) -> ExecutionLogEntity:
        now = datetime.utcnow()
        e = ExecutionLog(
            commitment_id=commitment_id,
            actual_minutes=actual_minutes,
            energy_level=energy_level,
            note=note,
            created_at=now,
            updated_at=now,
            creator_id=user_id,
            updater_id=user_id,
        )
        self.db.add(e)
        await self.db.commit()
        await self.db.refresh(e)
        return _to_entity(e)

    async def get_by_commitment_id(
        self, commitment_id: int
    ) -> ExecutionLogEntity | None:
        result = await self.db.execute(
            select(ExecutionLog).where(
                ExecutionLog.commitment_id == commitment_id,
                ExecutionLog.deleted_at.is_(None),
            )
        )
        e = result.scalar_one_or_none()
        return _to_entity(e) if e else None

    async def update(
        self,
        log_id: int,
        user_id: int,
        actual_minutes: int | None,
        energy_level: int | None,
        note: str | None,
    ) -> ExecutionLogEntity:
        result = await self.db.execute(
            select(ExecutionLog).where(
                ExecutionLog.id == log_id,
                ExecutionLog.deleted_at.is_(None),
            )
        )
        e = result.scalar_one()
        if actual_minutes is not None:
            e.actual_minutes = actual_minutes
        if energy_level is not None:
            e.energy_level = energy_level
        if note is not None:
            e.note = note
        e.updated_at = datetime.utcnow()
        e.updater_id = user_id
        await self.db.commit()
        await self.db.refresh(e)
        return _to_entity(e)
