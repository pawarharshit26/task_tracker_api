from app.core.exceptions import BaseException
from app.entities.vision import VisionEntity
from app.repositories.vision import VisionRepository
from app.services.base import BaseService


class VisionService(BaseService):
    class VisionNotFoundException(BaseException):
        message = "Vision not found"

    def __init__(self, repo: VisionRepository) -> None:
        self.repo = repo

    async def get_active(self, user_id: int) -> VisionEntity:
        vision = await self.repo.get_active(user_id=user_id)
        if not vision:
            raise self.VisionNotFoundException()
        return vision

    async def upsert(self, user_id: int, title: str, description: str) -> VisionEntity:
        existing = await self.repo.get_active(user_id=user_id)
        if existing:
            return await self.repo.update(
                vision_id=int(existing.id),
                user_id=user_id,
                title=title,
                description=description,
            )
        return await self.repo.create(
            user_id=user_id, title=title, description=description
        )
