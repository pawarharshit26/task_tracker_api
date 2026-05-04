from app.entities.base import BaseEntity
from app.interactors.base import BaseInteractor
from app.services.theme import ThemeService


class DeleteThemeInput(BaseEntity):
    user_id: int
    theme_id: int


class DeleteThemeInteractor(BaseInteractor[DeleteThemeInput, None]):
    class ThemeNotFoundException(BaseInteractor.InteractorException):
        message = "Theme not found"

    def __init__(self, theme_service: ThemeService) -> None:
        self.theme_service = theme_service

    async def execute(self, input: DeleteThemeInput) -> None:
        try:
            await self.theme_service.delete(
                user_id=input.user_id,
                theme_id=input.theme_id,
            )
        except ThemeService.ThemeNotFoundException as e:
            raise self.ThemeNotFoundException() from e
