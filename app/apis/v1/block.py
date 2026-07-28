from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.apis.exceptions import BaseAPIException
from app.apis.response import ResponseEntity
from app.core.hash_ids import decode
from app.dependencies import (
    get_create_block_interactor,
    get_current_user_id,
    get_delete_block_interactor,
    get_list_blocks_interactor,
    get_reorder_blocks_interactor,
    get_update_block_interactor,
)
from app.entities.block import (
    BlockEntity,
    BlockOwnerType,
    CreateBlockEntity,
    ReorderBlocksEntity,
    UpdateBlockEntity,
)
from app.interactors.block.create import CreateBlockInput, CreateBlockInteractor
from app.interactors.block.delete import DeleteBlockInput, DeleteBlockInteractor
from app.interactors.block.list import ListBlocksInput, ListBlocksInteractor
from app.interactors.block.reorder import ReorderBlocksInput, ReorderBlocksInteractor
from app.interactors.block.update import UpdateBlockInput, UpdateBlockInteractor

block_router = APIRouter()


@block_router.get(path="/", response_model=ResponseEntity[list[BlockEntity]])
async def list_blocks(
    owner_type: BlockOwnerType,
    owner_id: str,
    interactor: Annotated[ListBlocksInteractor, Depends(get_list_blocks_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=ListBlocksInput(
                user_id=user_id,
                owner_type=owner_type,
                owner_id=decode(owner_id),
            )
        )
        return ResponseEntity[list[BlockEntity]](data=result)
    except ListBlocksInteractor.OwnerNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e


@block_router.post(
    path="/",
    response_model=ResponseEntity[BlockEntity],
    status_code=status.HTTP_201_CREATED,
)
async def create_block(
    body: CreateBlockEntity,
    interactor: Annotated[CreateBlockInteractor, Depends(get_create_block_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=CreateBlockInput(
                user_id=user_id,
                owner_type=body.owner_type,
                owner_id=int(body.owner_id),
                block_type=body.block_type,
                content=body.content,
            )
        )
        return ResponseEntity[BlockEntity](data=result)
    except CreateBlockInteractor.OwnerNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e


@block_router.patch(path="/reorder", response_model=ResponseEntity[None])
async def reorder_blocks(
    body: ReorderBlocksEntity,
    interactor: Annotated[
        ReorderBlocksInteractor, Depends(get_reorder_blocks_interactor)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        await interactor.execute(
            input=ReorderBlocksInput(
                user_id=user_id,
                owner_type=body.owner_type,
                owner_id=int(body.owner_id),
                ids=[int(i) for i in body.ids],
            )
        )
        return ResponseEntity[None](data=None)
    except ReorderBlocksInteractor.OwnerNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e
    except ReorderBlocksInteractor.ReorderMismatchException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        ) from e


@block_router.patch(path="/{block_id}", response_model=ResponseEntity[BlockEntity])
async def update_block(
    block_id: str,
    body: UpdateBlockEntity,
    interactor: Annotated[UpdateBlockInteractor, Depends(get_update_block_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=UpdateBlockInput(
                user_id=user_id,
                block_id=decode(block_id),
                block_type=body.block_type,
                content=body.content,
            )
        )
        return ResponseEntity[BlockEntity](data=result)
    except UpdateBlockInteractor.BlockNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e
    except UpdateBlockInteractor.OwnerNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e


@block_router.delete(path="/{block_id}", response_model=ResponseEntity[None])
async def delete_block(
    block_id: str,
    interactor: Annotated[DeleteBlockInteractor, Depends(get_delete_block_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        await interactor.execute(
            input=DeleteBlockInput(
                user_id=user_id,
                block_id=decode(block_id),
            )
        )
        return ResponseEntity[None](data=None)
    except DeleteBlockInteractor.BlockNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e
    except DeleteBlockInteractor.OwnerNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e
