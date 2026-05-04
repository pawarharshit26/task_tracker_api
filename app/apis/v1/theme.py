from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.apis.exceptions import BaseAPIException
from app.apis.response import ResponseEntity
from app.core.hash_ids import decode
from app.dependencies import (
    get_create_theme_interactor,
    get_current_user_id,
    get_delete_theme_interactor,
    get_update_theme_interactor,
)
from app.entities.theme import CreateThemeEntity, ThemeEntity, UpdateThemeEntity
from app.interactors.theme.create import CreateThemeInput, CreateThemeInteractor
from app.interactors.theme.delete import DeleteThemeInput, DeleteThemeInteractor
from app.interactors.theme.update import UpdateThemeInput, UpdateThemeInteractor

theme_router = APIRouter()


@theme_router.post(
    path="/",
    response_model=ResponseEntity[ThemeEntity],
    status_code=status.HTTP_201_CREATED,
)
async def create_theme(
    body: CreateThemeEntity,
    interactor: Annotated[CreateThemeInteractor, Depends(get_create_theme_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=CreateThemeInput(
                user_id=user_id,
                vision_id=int(body.vision_id),
                name=body.name,
                description=body.description,
                preset_key=body.preset_key,
            )
        )
        return ResponseEntity[ThemeEntity](data=result)
    except CreateThemeInteractor.VisionNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e


@theme_router.patch(path="/{theme_id}", response_model=ResponseEntity[ThemeEntity])
async def update_theme(
    theme_id: str,
    body: UpdateThemeEntity,
    interactor: Annotated[UpdateThemeInteractor, Depends(get_update_theme_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=UpdateThemeInput(
                user_id=user_id,
                theme_id=decode(theme_id),
                name=body.name,
                description=body.description,
                preset_key=body.preset_key,
                is_active=body.is_active,
            )
        )
        return ResponseEntity[ThemeEntity](data=result)
    except UpdateThemeInteractor.ThemeNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e


@theme_router.delete(path="/{theme_id}", response_model=ResponseEntity[None])
async def delete_theme(
    theme_id: str,
    interactor: Annotated[DeleteThemeInteractor, Depends(get_delete_theme_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        await interactor.execute(
            input=DeleteThemeInput(user_id=user_id, theme_id=decode(theme_id))
        )
        return ResponseEntity[None](data=None)
    except DeleteThemeInteractor.ThemeNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e
