from app.core.exceptions import BaseException
from app.entities.theme import ThemeEntity
from app.repositories.theme import ThemeRepository
from app.repositories.vision import VisionRepository
from app.services.base import BaseService


class ThemeService(BaseService):
    class ThemeNotFoundException(BaseException):
        message = "Theme not found"

    class VisionNotFoundException(BaseException):
        message = "Vision not found"

    def __init__(
        self, theme_repo: ThemeRepository, vision_repo: VisionRepository
    ) -> None:
        self.theme_repo = theme_repo
        self.vision_repo = vision_repo

    async def create(
        self,
        user_id: int,
        vision_id: int,
        name: str,
        description: str,
        preset_key: str,
    ) -> ThemeEntity:
        vision = await self.vision_repo.get_owned(vision_id=vision_id, user_id=user_id)
        if not vision:
            raise self.VisionNotFoundException()
        return await self.theme_repo.create(
            vision_id=vision_id,
            user_id=user_id,
            name=name,
            description=description,
            preset_key=preset_key,
        )

    async def update(
        self,
        user_id: int,
        theme_id: int,
        name: str | None,
        description: str | None,
        preset_key: str | None,
        is_active: bool | None,
    ) -> ThemeEntity:
        theme = await self.theme_repo.get_owned(theme_id=theme_id, user_id=user_id)
        if not theme:
            raise self.ThemeNotFoundException()
        return await self.theme_repo.update(
            theme_id=theme_id,
            user_id=user_id,
            name=name,
            description=description,
            preset_key=preset_key,
            is_active=is_active,
        )

    async def delete(self, user_id: int, theme_id: int) -> None:
        theme = await self.theme_repo.get_owned(theme_id=theme_id, user_id=user_id)
        if not theme:
            raise self.ThemeNotFoundException()
        await self.theme_repo.delete(theme_id=theme_id, user_id=user_id)
