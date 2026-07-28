from app.core.exceptions import BaseException
from app.entities.block import BlockEntity, BlockOwnerType, BlockType
from app.repositories.block import BlockRepository
from app.repositories.commitment import CommitmentRepository
from app.repositories.execution_log import ExecutionLogRepository
from app.repositories.goal import GoalRepository
from app.repositories.phase import PhaseRepository
from app.services.base import BaseService


class BlockService(BaseService):
    class BlockNotFoundException(BaseException):
        message = "Block not found"

    class OwnerNotFoundException(BaseException):
        message = "Owner not found"

    class ReorderMismatchException(BaseException):
        message = "Reorder list does not match existing blocks"

    def __init__(
        self,
        block_repo: BlockRepository,
        goal_repo: GoalRepository,
        phase_repo: PhaseRepository,
        log_repo: ExecutionLogRepository,
        commitment_repo: CommitmentRepository,
    ) -> None:
        self.block_repo = block_repo
        self.goal_repo = goal_repo
        self.phase_repo = phase_repo
        self.log_repo = log_repo
        self.commitment_repo = commitment_repo

    async def _verify_owner(
        self,
        owner_type: BlockOwnerType,
        owner_id: int,
        user_id: int,
    ) -> None:
        if owner_type == "goal":
            owner = await self.goal_repo.get_owned(
                goal_id=owner_id, user_id=user_id
            )
        elif owner_type == "phase":
            owner = await self.phase_repo.get_owned(
                phase_id=owner_id, user_id=user_id
            )
        elif owner_type == "execution_log":
            log = await self.log_repo.get(log_id=owner_id)
            if not log:
                raise self.OwnerNotFoundException()
            owner = await self.commitment_repo.get_owned(
                commitment_id=int(log.commitment_id), user_id=user_id
            )
        else:
            raise self.OwnerNotFoundException()
        if not owner:
            raise self.OwnerNotFoundException()

    async def list(
        self,
        user_id: int,
        owner_type: BlockOwnerType,
        owner_id: int,
    ) -> list[BlockEntity]:
        await self._verify_owner(
            owner_type=owner_type, owner_id=owner_id, user_id=user_id
        )
        return await self.block_repo.list(
            owner_type=owner_type, owner_id=owner_id
        )

    async def create(
        self,
        user_id: int,
        owner_type: BlockOwnerType,
        owner_id: int,
        block_type: BlockType,
        content: dict,
    ) -> BlockEntity:
        await self._verify_owner(
            owner_type=owner_type, owner_id=owner_id, user_id=user_id
        )
        position = await self.block_repo.count_for_owner(
            owner_type=owner_type, owner_id=owner_id
        )
        return await self.block_repo.create(
            owner_type=owner_type,
            owner_id=owner_id,
            block_type=block_type,
            content=content,
            position=position,
            user_id=user_id,
        )

    async def update(
        self,
        user_id: int,
        block_id: int,
        block_type: BlockType | None,
        content: dict | None,
    ) -> BlockEntity:
        block = await self.block_repo.get(block_id=block_id)
        if not block:
            raise self.BlockNotFoundException()
        await self._verify_owner(
            owner_type=block.owner_type,
            owner_id=int(block.owner_id),
            user_id=user_id,
        )
        return await self.block_repo.update(
            block_id=block_id,
            user_id=user_id,
            block_type=block_type,
            content=content,
        )

    async def delete(self, user_id: int, block_id: int) -> None:
        block = await self.block_repo.get(block_id=block_id)
        if not block:
            raise self.BlockNotFoundException()
        await self._verify_owner(
            owner_type=block.owner_type,
            owner_id=int(block.owner_id),
            user_id=user_id,
        )
        await self.block_repo.delete(block_id=block_id, user_id=user_id)

    async def reorder(
        self,
        user_id: int,
        owner_type: BlockOwnerType,
        owner_id: int,
        ids: list[int],
    ) -> None:
        await self._verify_owner(
            owner_type=owner_type, owner_id=owner_id, user_id=user_id
        )
        existing = await self.block_repo.list(
            owner_type=owner_type, owner_id=owner_id
        )
        existing_ids = {int(b.id) for b in existing}
        if set(ids) != existing_ids:
            raise self.ReorderMismatchException()
        await self.block_repo.reorder(ids=ids, user_id=user_id)
