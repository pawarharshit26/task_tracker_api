from app.entities.base import BaseEntity
from app.entities.track import TrackEntity
from app.interactors.base import BaseInteractor
from app.services.track import TrackService


class CreateTrackInput(BaseEntity):
    user_id: int
    theme_id: int
    name: str
    description: str | None = None
    cadence_per_week: int | None = None


class CreateTrackInteractor(BaseInteractor[CreateTrackInput, TrackEntity]):
    class ThemeNotFoundException(BaseInteractor.InteractorException):
        message = "Theme not found"

    def __init__(self, track_service: TrackService) -> None:
        self.track_service = track_service

    async def execute(self, input: CreateTrackInput) -> TrackEntity:
        try:
            return await self.track_service.create(
                user_id=input.user_id,
                theme_id=input.theme_id,
                name=input.name,
                description=input.description,
                cadence_per_week=input.cadence_per_week,
            )
        except TrackService.ThemeNotFoundException as e:
            raise self.ThemeNotFoundException() from e
