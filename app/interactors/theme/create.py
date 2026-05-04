from app.entities.base import BaseEntity
from app.entities.theme import ThemeEntity
from app.interactors.base import BaseInteractor
from app.services.theme import ThemeService


class CreateThemeInput(BaseEntity):
    user_id: int
    vision_id: int
    name: str
    description: str
    preset_key: str


class CreateThemeInteractor(BaseInteractor[CreateThemeInput, ThemeEntity]):
    class VisionNotFoundException(BaseInteractor.InteractorException):
        message = "Vision not found"

    def __init__(self, theme_service: ThemeService) -> None:
        self.theme_service = theme_service

    async def execute(self, input: CreateThemeInput) -> ThemeEntity:
        try:
            return await self.theme_service.create(
                user_id=input.user_id,
                vision_id=input.vision_id,
                name=input.name,
                description=input.description,
                preset_key=input.preset_key,
            )
        except ThemeService.VisionNotFoundException as e:
            raise self.VisionNotFoundException() from e
