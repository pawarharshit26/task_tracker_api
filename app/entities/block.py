from typing import Literal

from app.core.hash_ids import HashId
from app.entities.base import BaseEntity

BlockOwnerType = Literal["goal", "phase", "execution_log", "daily_reflection"]
BlockType = Literal["paragraph", "heading", "bullet", "checkbox", "quote"]


class BlockEntity(BaseEntity):
    id: HashId
    owner_type: BlockOwnerType
    owner_id: HashId
    block_type: BlockType
    content: dict
    position: int


class CreateBlockEntity(BaseEntity):
    owner_type: BlockOwnerType
    owner_id: HashId
    block_type: BlockType
    content: dict


class UpdateBlockEntity(BaseEntity):
    block_type: BlockType | None = None
    content: dict | None = None


class ReorderBlocksEntity(BaseEntity):
    owner_type: BlockOwnerType
    owner_id: HashId
    ids: list[HashId]
