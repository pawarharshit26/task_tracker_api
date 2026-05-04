import calendar as _calendar
from datetime import date, timedelta

from app.entities.history import (
    HistoryDayEntity,
    HistoryEntity,
    HistoryItemEntity,
    HistoryTimelineEntity,
)
from app.repositories.commitment import CommitmentRepository
from app.repositories.execution_log import ExecutionLogRepository
from app.services.base import BaseService


class HistoryService(BaseService):
    def __init__(
        self,
        commitment_repo: CommitmentRepository,
        log_repo: ExecutionLogRepository,
    ) -> None:
        self.commitment_repo = commitment_repo
        self.log_repo = log_repo

    def _build_days(
        self,
        rows: list,
        logs: dict,
    ) -> list[HistoryDayEntity]:
        days_map: dict[date, list[HistoryItemEntity]] = {}
        for row in rows:
            d = row.commitment.date
            if d not in days_map:
                days_map[d] = []
            days_map[d].append(
                HistoryItemEntity(
                    commitment=row.commitment,
                    log=logs.get(int(row.commitment.id)),
                    breadcrumb=row.breadcrumb,
                )
            )
        return [
            HistoryDayEntity(date=d, items=items)
            for d, items in sorted(days_map.items(), reverse=True)
        ]

    async def get_timeline(
        self, user_id: int, before: date, limit_days: int
    ) -> HistoryTimelineEntity:
        to_date = before - timedelta(days=1)
        from_date = to_date - timedelta(days=limit_days - 1)

        rows = await self.commitment_repo.list_by_date_range(
            user_id=user_id, from_date=from_date, to_date=to_date
        )
        commitment_ids = [int(row.commitment.id) for row in rows]
        logs = await self.log_repo.get_by_commitment_ids(commitment_ids=commitment_ids)
        history_days = self._build_days(rows=rows, logs=logs)

        return HistoryTimelineEntity(
            days=history_days,
            next_cursor=from_date if history_days else None,
        )

    async def get_calendar(
        self, user_id: int, year: int, month: int
    ) -> HistoryEntity:
        from_date = date(year, month, 1)
        last_day = _calendar.monthrange(year, month)[1]
        to_date = date(year, month, last_day)

        rows = await self.commitment_repo.list_by_date_range(
            user_id=user_id, from_date=from_date, to_date=to_date
        )
        commitment_ids = [int(row.commitment.id) for row in rows]
        logs = await self.log_repo.get_by_commitment_ids(commitment_ids=commitment_ids)
        history_days = self._build_days(rows=rows, logs=logs)

        return HistoryEntity(days=history_days)
