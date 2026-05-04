from app.entities.base import BaseEntity
from app.entities.vision import VisionEntity
from app.interactors.base import BaseInteractor
from app.services.vision import VisionService


class UpsertVisionInput(BaseEntity):
    user_id: int
    title: str
    description: str


class UpsertVisionInteractor(BaseInteractor[UpsertVisionInput, VisionEntity]):
    def __init__(self, vision_service: VisionService) -> None:
        self.vision_service = vision_service

    async def execute(self, input: UpsertVisionInput) -> VisionEntity:
        return await self.vision_service.upsert(
            user_id=input.user_id,
            title=input.title,
            description=input.description,
        )
