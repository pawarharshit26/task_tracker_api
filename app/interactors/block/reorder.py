from app.entities.base import BaseEntity
from app.entities.block import BlockOwnerType
from app.interactors.base import BaseInteractor
from app.services.block import BlockService


class ReorderBlocksInput(BaseEntity):
    user_id: int
    owner_type: BlockOwnerType
    owner_id: int
    ids: list[int]


class ReorderBlocksInteractor(BaseInteractor[ReorderBlocksInput, None]):
    class OwnerNotFoundException(BaseInteractor.InteractorException):
        message = "Owner not found"

    class ReorderMismatchException(BaseInteractor.InteractorException):
        message = "Reorder list does not match existing blocks"

    def __init__(self, block_service: BlockService) -> None:
        self.block_service = block_service

    async def execute(self, input: ReorderBlocksInput) -> None:
        try:
            await self.block_service.reorder(
                user_id=input.user_id,
                owner_type=input.owner_type,
                owner_id=input.owner_id,
                ids=input.ids,
            )
        except BlockService.OwnerNotFoundException as e:
            raise self.OwnerNotFoundException() from e
        except BlockService.ReorderMismatchException as e:
            raise self.ReorderMismatchException() from e
