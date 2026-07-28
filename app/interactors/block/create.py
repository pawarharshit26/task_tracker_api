from app.entities.base import BaseEntity
from app.entities.block import BlockEntity, BlockOwnerType, BlockType
from app.interactors.base import BaseInteractor
from app.services.block import BlockService


class CreateBlockInput(BaseEntity):
    user_id: int
    owner_type: BlockOwnerType
    owner_id: int
    block_type: BlockType
    content: dict


class CreateBlockInteractor(BaseInteractor[CreateBlockInput, BlockEntity]):
    class OwnerNotFoundException(BaseInteractor.InteractorException):
        message = "Owner not found"

    def __init__(self, block_service: BlockService) -> None:
        self.block_service = block_service

    async def execute(self, input: CreateBlockInput) -> BlockEntity:
        try:
            return await self.block_service.create(
                user_id=input.user_id,
                owner_type=input.owner_type,
                owner_id=input.owner_id,
                block_type=input.block_type,
                content=input.content,
            )
        except BlockService.OwnerNotFoundException as e:
            raise self.OwnerNotFoundException() from e
