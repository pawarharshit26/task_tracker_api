from app.entities.base import BaseEntity
from app.entities.block import BlockEntity, BlockOwnerType
from app.interactors.base import BaseInteractor
from app.services.block import BlockService


class ListBlocksInput(BaseEntity):
    user_id: int
    owner_type: BlockOwnerType
    owner_id: int


class ListBlocksInteractor(BaseInteractor[ListBlocksInput, list[BlockEntity]]):
    class OwnerNotFoundException(BaseInteractor.InteractorException):
        message = "Owner not found"

    def __init__(self, block_service: BlockService) -> None:
        self.block_service = block_service

    async def execute(self, input: ListBlocksInput) -> list[BlockEntity]:
        try:
            return await self.block_service.list(
                user_id=input.user_id,
                owner_type=input.owner_type,
                owner_id=input.owner_id,
            )
        except BlockService.OwnerNotFoundException as e:
            raise self.OwnerNotFoundException() from e
