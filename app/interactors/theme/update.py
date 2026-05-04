from app.entities.base import BaseEntity
from app.entities.theme import ThemeEntity
from app.interactors.base import BaseInteractor
from app.services.theme import ThemeService


class UpdateThemeInput(BaseEntity):
    user_id: int
    theme_id: int
    name: str | None = None
    description: str | None = None
    preset_key: str | None = None
    is_active: bool | None = None


class UpdateThemeInteractor(BaseInteractor[UpdateThemeInput, ThemeEntity]):
    class ThemeNotFoundException(BaseInteractor.InteractorException):
        message = "Theme not found"

    def __init__(self, theme_service: ThemeService) -> None:
        self.theme_service = theme_service

    async def execute(self, input: UpdateThemeInput) -> ThemeEntity:
        try:
            return await self.theme_service.update(
                user_id=input.user_id,
                theme_id=input.theme_id,
                name=input.name,
                description=input.description,
                preset_key=input.preset_key,
                is_active=input.is_active,
            )
        except ThemeService.ThemeNotFoundException as e:
            raise self.ThemeNotFoundException() from e
