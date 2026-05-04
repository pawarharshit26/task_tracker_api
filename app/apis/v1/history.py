from datetime import date, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.apis.response import ResponseEntity
from app.dependencies import (
    get_current_user_id,
    get_get_history_calendar_interactor,
    get_get_history_timeline_interactor,
)
from app.entities.history import HistoryEntity, HistoryTimelineEntity
from app.interactors.history.get import GetHistoryTimelineInput, GetHistoryTimelineInteractor
from app.interactors.history.get_calendar import (
    GetHistoryCalendarInput,
    GetHistoryCalendarInteractor,
)

history_router = APIRouter()


@history_router.get(path="/timeline", response_model=ResponseEntity[HistoryTimelineEntity])
async def get_history_timeline(
    interactor: Annotated[
        GetHistoryTimelineInteractor, Depends(get_get_history_timeline_interactor)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
    before: date | None = Query(default=None),
    limit: int = Query(default=14, ge=1, le=60),
):
    if before is None:
        before = date.today() + timedelta(days=1)
    result = await interactor.execute(
        input=GetHistoryTimelineInput(user_id=user_id, before=before, limit_days=limit)
    )
    return ResponseEntity[HistoryTimelineEntity](data=result)


@history_router.get(path="/calendar", response_model=ResponseEntity[HistoryEntity])
async def get_history_calendar(
    interactor: Annotated[
        GetHistoryCalendarInteractor, Depends(get_get_history_calendar_interactor)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
):
    result = await interactor.execute(
        input=GetHistoryCalendarInput(user_id=user_id, year=year, month=month)
    )
    return ResponseEntity[HistoryEntity](data=result)
