from app.entities.base import BaseEntity
from app.interactors.base import BaseInteractor
from app.services.block import BlockService


class DeleteBlockInput(BaseEntity):
    user_id: int
    block_id: int


class DeleteBlockInteractor(BaseInteractor[DeleteBlockInput, None]):
    class BlockNotFoundException(BaseInteractor.InteractorException):
        message = "Block not found"

    class OwnerNotFoundException(BaseInteractor.InteractorException):
        message = "Owner not found"

    def __init__(self, block_service: BlockService) -> None:
        self.block_service = block_service

    async def execute(self, input: DeleteBlockInput) -> None:
        try:
            await self.block_service.delete(
                user_id=input.user_id,
                block_id=input.block_id,
            )
        except BlockService.BlockNotFoundException as e:
            raise self.BlockNotFoundException() from e
        except BlockService.OwnerNotFoundException as e:
            raise self.OwnerNotFoundException() from e
