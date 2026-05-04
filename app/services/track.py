from app.core.exceptions import BaseException
from app.entities.track import TrackEntity
from app.repositories.theme import ThemeRepository
from app.repositories.track import TrackRepository
from app.services.base import BaseService


class TrackService(BaseService):
    class TrackNotFoundException(BaseException):
        message = "Track not found"

    class ThemeNotFoundException(BaseException):
        message = "Theme not found"

    def __init__(
        self, track_repo: TrackRepository, theme_repo: ThemeRepository
    ) -> None:
        self.track_repo = track_repo
        self.theme_repo = theme_repo

    async def create(
        self,
        user_id: int,
        theme_id: int,
        name: str,
        description: str | None,
        cadence_per_week: int | None,
    ) -> TrackEntity:
        theme = await self.theme_repo.get_owned(theme_id=theme_id, user_id=user_id)
        if not theme:
            raise self.ThemeNotFoundException()
        return await self.track_repo.create(
            theme_id=theme_id,
            user_id=user_id,
            name=name,
            description=description,
            cadence_per_week=cadence_per_week,
        )

    async def update(
        self,
        user_id: int,
        track_id: int,
        name: str | None,
        description: str | None,
        cadence_per_week: int | None,
        is_active: bool | None,
    ) -> TrackEntity:
        track = await self.track_repo.get_owned(track_id=track_id, user_id=user_id)
        if not track:
            raise self.TrackNotFoundException()
        return await self.track_repo.update(
            track_id=track_id,
            user_id=user_id,
            name=name,
            description=description,
            cadence_per_week=cadence_per_week,
            is_active=is_active,
        )

    async def delete(self, user_id: int, track_id: int) -> None:
        track = await self.track_repo.get_owned(track_id=track_id, user_id=user_id)
        if not track:
            raise self.TrackNotFoundException()
        await self.track_repo.delete(track_id=track_id, user_id=user_id)
