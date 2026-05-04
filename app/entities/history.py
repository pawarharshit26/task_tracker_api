from datetime import date

from app.entities.base import BaseEntity
from app.entities.breadcrumb import BreadcrumbEntity
from app.entities.commitment import CommitmentEntity
from app.entities.execution_log import ExecutionLogEntity


class HistoryItemEntity(BaseEntity):
    commitment: CommitmentEntity
    log: ExecutionLogEntity | None
    breadcrumb: BreadcrumbEntity


class HistoryDayEntity(BaseEntity):
    date: date
    items: list[HistoryItemEntity]


class HistoryEntity(BaseEntity):
    days: list[HistoryDayEntity]


class HistoryTimelineEntity(BaseEntity):
    days: list[HistoryDayEntity]
    next_cursor: date | None
