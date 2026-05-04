from app.entities.base import BaseEntity
from app.interactors.base import BaseInteractor
from app.services.track import TrackService


class DeleteTrackInput(BaseEntity):
    user_id: int
    track_id: int


class DeleteTrackInteractor(BaseInteractor[DeleteTrackInput, None]):
    class TrackNotFoundException(BaseInteractor.InteractorException):
        message = "Track not found"

    def __init__(self, track_service: TrackService) -> None:
        self.track_service = track_service

    async def execute(self, input: DeleteTrackInput) -> None:
        try:
            await self.track_service.delete(
                user_id=input.user_id,
                track_id=input.track_id,
            )
        except TrackService.TrackNotFoundException as e:
            raise self.TrackNotFoundException() from e
