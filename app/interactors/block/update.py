from app.entities.base import BaseEntity
from app.entities.block import BlockEntity, BlockType
from app.interactors.base import BaseInteractor
from app.services.block import BlockService


class UpdateBlockInput(BaseEntity):
    user_id: int
    block_id: int
    block_type: BlockType | None = None
    content: dict | None = None


class UpdateBlockInteractor(BaseInteractor[UpdateBlockInput, BlockEntity]):
    class BlockNotFoundException(BaseInteractor.InteractorException):
        message = "Block not found"

    class OwnerNotFoundException(BaseInteractor.InteractorException):
        message = "Owner not found"

    def __init__(self, block_service: BlockService) -> None:
        self.block_service = block_service

    async def execute(self, input: UpdateBlockInput) -> BlockEntity:
        try:
            return await self.block_service.update(
                user_id=input.user_id,
                block_id=input.block_id,
                block_type=input.block_type,
                content=input.content,
            )
        except BlockService.BlockNotFoundException as e:
            raise self.BlockNotFoundException() from e
        except BlockService.OwnerNotFoundException as e:
            raise self.OwnerNotFoundException() from e
