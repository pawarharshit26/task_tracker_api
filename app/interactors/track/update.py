from app.entities.base import BaseEntity
from app.entities.track import TrackEntity
from app.interactors.base import BaseInteractor
from app.services.track import TrackService


class UpdateTrackInput(BaseEntity):
    user_id: int
    track_id: int
    name: str | None = None
    description: str | None = None
    cadence_per_week: int | None = None
    is_active: bool | None = None


class UpdateTrackInteractor(BaseInteractor[UpdateTrackInput, TrackEntity]):
    class TrackNotFoundException(BaseInteractor.InteractorException):
        message = "Track not found"

    def __init__(self, track_service: TrackService) -> None:
        self.track_service = track_service

    async def execute(self, input: UpdateTrackInput) -> TrackEntity:
        try:
            return await self.track_service.update(
                user_id=input.user_id,
                track_id=input.track_id,
                name=input.name,
                description=input.description,
                cadence_per_week=input.cadence_per_week,
                is_active=input.is_active,
            )
        except TrackService.TrackNotFoundException as e:
            raise self.TrackNotFoundException() from e
