from app.entities.base import BaseEntity
from app.entities.history import HistoryEntity
from app.interactors.base import BaseInteractor
from app.services.history import HistoryService


class GetHistoryCalendarInput(BaseEntity):
    user_id: int
    year: int
    month: int


class GetHistoryCalendarInteractor(
    BaseInteractor[GetHistoryCalendarInput, HistoryEntity]
):
    def __init__(self, history_service: HistoryService) -> None:
        self.history_service = history_service

    async def execute(self, input: GetHistoryCalendarInput) -> HistoryEntity:
        return await self.history_service.get_calendar(
            user_id=input.user_id,
            year=input.year,
            month=input.month,
        )
