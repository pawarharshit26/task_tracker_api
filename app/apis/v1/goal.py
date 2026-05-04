from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.apis.exceptions import BaseAPIException
from app.apis.response import ResponseEntity
from app.core.hash_ids import decode
from app.dependencies import (
    get_create_goal_interactor,
    get_current_user_id,
    get_delete_goal_interactor,
    get_get_goal_detail_interactor,
    get_list_goals_interactor,
    get_update_goal_interactor,
)
from app.entities.goal import (
    CreateGoalEntity,
    GoalDetailEntity,
    GoalEntity,
    UpdateGoalEntity,
)
from app.interactors.goal.create import CreateGoalInput, CreateGoalInteractor
from app.interactors.goal.delete import DeleteGoalInput, DeleteGoalInteractor
from app.interactors.goal.get_detail import GetGoalDetailInput, GetGoalDetailInteractor
from app.interactors.goal.list import ListGoalsInteractor
from app.interactors.goal.update import UpdateGoalInput, UpdateGoalInteractor

goal_router = APIRouter()


@goal_router.get(path="/", response_model=ResponseEntity[list[GoalEntity]])
async def list_goals(
    interactor: Annotated[ListGoalsInteractor, Depends(get_list_goals_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    result = await interactor.execute(input=user_id)
    return ResponseEntity[list[GoalEntity]](data=result)


@goal_router.get(path="/{goal_id}", response_model=ResponseEntity[GoalDetailEntity])
async def get_goal_detail(
    goal_id: str,
    interactor: Annotated[
        GetGoalDetailInteractor, Depends(get_get_goal_detail_interactor)
    ],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=GetGoalDetailInput(user_id=user_id, goal_id=decode(goal_id))
        )
        return ResponseEntity[GoalDetailEntity](data=result)
    except GetGoalDetailInteractor.GoalNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e


@goal_router.post(
    path="/",
    response_model=ResponseEntity[GoalEntity],
    status_code=status.HTTP_201_CREATED,
)
async def create_goal(
    body: CreateGoalEntity,
    interactor: Annotated[CreateGoalInteractor, Depends(get_create_goal_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    result = await interactor.execute(
        input=CreateGoalInput(
            user_id=user_id,
            track_id=int(body.track_id),
            title=body.title,
            horizon=body.horizon,
        )
    )
    return ResponseEntity[GoalEntity](data=result)


@goal_router.patch(path="/{goal_id}", response_model=ResponseEntity[GoalEntity])
async def update_goal(
    goal_id: str,
    body: UpdateGoalEntity,
    interactor: Annotated[UpdateGoalInteractor, Depends(get_update_goal_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        result = await interactor.execute(
            input=UpdateGoalInput(
                user_id=user_id,
                goal_id=decode(goal_id),
                title=body.title,
                horizon=body.horizon,
            )
        )
        return ResponseEntity[GoalEntity](data=result)
    except UpdateGoalInteractor.GoalNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e


@goal_router.delete(path="/{goal_id}", response_model=ResponseEntity[None])
async def delete_goal(
    goal_id: str,
    interactor: Annotated[DeleteGoalInteractor, Depends(get_delete_goal_interactor)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    try:
        await interactor.execute(
            input=DeleteGoalInput(user_id=user_id, goal_id=decode(goal_id))
        )
        return ResponseEntity[None](data=None)
    except DeleteGoalInteractor.GoalNotFoundException as e:
        raise BaseAPIException(
            message=str(e.message), status_code=status.HTTP_404_NOT_FOUND
        ) from e
