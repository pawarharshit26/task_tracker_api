from datetime import date

from app.entities.base import BaseEntity
from app.entities.history import HistoryTimelineEntity
from app.interactors.base import BaseInteractor
from app.services.history import HistoryService


class GetHistoryTimelineInput(BaseEntity):
    user_id: int
    before: date
    limit_days: int = 14


class GetHistoryTimelineInteractor(
    BaseInteractor[GetHistoryTimelineInput, HistoryTimelineEntity]
):
    def __init__(self, history_service: HistoryService) -> None:
        self.history_service = history_service

    async def execute(self, input: GetHistoryTimelineInput) -> HistoryTimelineEntity:
        return await self.history_service.get_timeline(
            user_id=input.user_id,
            before=input.before,
            limit_days=input.limit_days,
        )
