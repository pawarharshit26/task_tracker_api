from datetime import datetime

from sqlalchemy import func, select

from app.db.models.block import Block
from app.entities.block import BlockEntity, BlockOwnerType, BlockType
from app.repositories.base import BaseRepository


def _to_entity(b: Block) -> BlockEntity:
    return BlockEntity(
        id=b.id,
        owner_type=b.owner_type,
        owner_id=b.owner_id,
        block_type=b.block_type,
        content=b.content,
        position=b.position,
    )


class BlockRepository(BaseRepository):
    async def list(
        self,
        owner_type: BlockOwnerType,
        owner_id: int,
    ) -> list[BlockEntity]:
        result = await self.db.execute(
            select(Block)
            .where(
                Block.owner_type == owner_type,
                Block.owner_id == owner_id,
                Block.deleted_at.is_(None),
            )
            .order_by(Block.position.asc())
        )
        return [_to_entity(b) for b in result.scalars().all()]

    async def get(self, block_id: int) -> BlockEntity | None:
        result = await self.db.execute(
            select(Block).where(
                Block.id == block_id,
                Block.deleted_at.is_(None),
            )
        )
        b = result.scalar_one_or_none()
        return _to_entity(b) if b else None

    async def count_for_owner(
        self,
        owner_type: BlockOwnerType,
        owner_id: int,
    ) -> int:
        result = await self.db.execute(
            select(func.count()).where(
                Block.owner_type == owner_type,
                Block.owner_id == owner_id,
                Block.deleted_at.is_(None),
            )
        )
        return result.scalar_one()

    async def create(
        self,
        owner_type: BlockOwnerType,
        owner_id: int,
        block_type: BlockType,
        content: dict,
        position: int,
        user_id: int,
    ) -> BlockEntity:
        now = datetime.utcnow()
        b = Block(
            owner_type=owner_type,
            owner_id=owner_id,
            block_type=block_type,
            content=content,
            position=position,
            created_at=now,
            updated_at=now,
            creator_id=user_id,
            updater_id=user_id,
        )
        self.db.add(b)
        await self.db.commit()
        await self.db.refresh(b)
        return _to_entity(b)

    async def update(
        self,
        block_id: int,
        user_id: int,
        block_type: BlockType | None,
        content: dict | None,
    ) -> BlockEntity:
        result = await self.db.execute(
            select(Block).where(
                Block.id == block_id,
                Block.deleted_at.is_(None),
            )
        )
        b = result.scalar_one()
        if block_type is not None:
            b.block_type = block_type
        if content is not None:
            b.content = content
        b.updated_at = datetime.utcnow()
        b.updater_id = user_id
        await self.db.commit()
        await self.db.refresh(b)
        return _to_entity(b)

    async def delete(self, block_id: int, user_id: int) -> None:
        result = await self.db.execute(
            select(Block).where(
                Block.id == block_id,
                Block.deleted_at.is_(None),
            )
        )
        b = result.scalar_one()
        b.deleted_at = datetime.utcnow()
        b.deleter_id = user_id
        await self.db.commit()

    async def reorder(self, ids: list[int], user_id: int) -> None:
        now = datetime.utcnow()
        for position, block_id in enumerate(ids):
            result = await self.db.execute(
                select(Block).where(
                    Block.id == block_id,
                    Block.deleted_at.is_(None),
                )
            )
            b = result.scalar_one()
            b.position = position
            b.updated_at = now
            b.updater_id = user_id
        await self.db.commit()
