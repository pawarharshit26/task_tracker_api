from typing import Annotated

import structlog
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.exceptions import UnauthorizedException
from app.core.jwt import JWTService, get_jwt_service
from app.db.base import get_db
from app.interactors.commitment.create import CreateCommitmentInteractor
from app.interactors.execution_log.upsert import UpsertLogInteractor
from app.interactors.goal.create import CreateGoalInteractor
from app.interactors.goal.delete import DeleteGoalInteractor
from app.interactors.goal.get_detail import GetGoalDetailInteractor
from app.interactors.goal.list import ListGoalsInteractor
from app.interactors.goal.update import UpdateGoalInteractor
from app.interactors.history.get import GetHistoryTimelineInteractor
from app.interactors.history.get_calendar import GetHistoryCalendarInteractor
from app.interactors.phase.create import CreatePhaseInteractor
from app.interactors.phase.delete import DeletePhaseInteractor
from app.interactors.phase.update import UpdatePhaseInteractor
from app.interactors.structure.get import GetStructureInteractor
from app.interactors.theme.create import CreateThemeInteractor
from app.interactors.theme.delete import DeleteThemeInteractor
from app.interactors.theme.update import UpdateThemeInteractor
from app.interactors.today.get import GetTodayInteractor
from app.interactors.track.create import CreateTrackInteractor
from app.interactors.track.delete import DeleteTrackInteractor
from app.interactors.track.update import UpdateTrackInteractor
from app.interactors.user.get_me import GetMeInteractor
from app.interactors.user.signin import SigninInteractor
from app.interactors.user.signout import SignoutInteractor
from app.interactors.user.signup import SignupInteractor
from app.interactors.vision.get_active import GetActiveVisionInteractor
from app.interactors.vision.upsert import UpsertVisionInteractor
from app.repositories.commitment import CommitmentRepository
from app.repositories.execution_log import ExecutionLogRepository
from app.repositories.goal import GoalRepository
from app.repositories.phase import PhaseRepository
from app.repositories.reflection import ReflectionRepository
from app.repositories.theme import ThemeRepository
from app.repositories.track import TrackRepository
from app.repositories.user import UserRepository
from app.repositories.vision import VisionRepository
from app.services.commitment import CommitmentService
from app.services.execution_log import ExecutionLogService
from app.services.goal import GoalService
from app.services.history import HistoryService
from app.services.phase import PhaseService
from app.services.structure import StructureService
from app.services.theme import ThemeService
from app.services.today import TodayService
from app.services.track import TrackService
from app.services.user import UserService
from app.services.vision import VisionService

logger = structlog.get_logger(__name__)


# --- User ---


def get_user_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    return UserRepository(db=db)


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
) -> UserService:
    return UserService(repo=repo, jwt_service=jwt_service)


def get_signup_interactor(
    service: Annotated[UserService, Depends(get_user_service)],
) -> SignupInteractor:
    return SignupInteractor(user_service=service)


def get_signin_interactor(
    service: Annotated[UserService, Depends(get_user_service)],
) -> SigninInteractor:
    return SigninInteractor(user_service=service)


def get_signout_interactor(
    service: Annotated[UserService, Depends(get_user_service)],
) -> SignoutInteractor:
    return SignoutInteractor(user_service=service)


def get_me_interactor(
    service: Annotated[UserService, Depends(get_user_service)],
) -> GetMeInteractor:
    return GetMeInteractor(user_service=service)


# --- Vision ---


def get_vision_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> VisionRepository:
    return VisionRepository(db=db)


def get_vision_service(
    repo: Annotated[VisionRepository, Depends(get_vision_repository)],
) -> VisionService:
    return VisionService(repo=repo)


def get_get_active_vision_interactor(
    service: Annotated[VisionService, Depends(get_vision_service)],
) -> GetActiveVisionInteractor:
    return GetActiveVisionInteractor(vision_service=service)


def get_upsert_vision_interactor(
    service: Annotated[VisionService, Depends(get_vision_service)],
) -> UpsertVisionInteractor:
    return UpsertVisionInteractor(vision_service=service)


# --- Structure (read) ---


def get_theme_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ThemeRepository:
    return ThemeRepository(db=db)


def get_track_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TrackRepository:
    return TrackRepository(db=db)


def get_structure_service(
    theme_repo: Annotated[ThemeRepository, Depends(get_theme_repository)],
    track_repo: Annotated[TrackRepository, Depends(get_track_repository)],
) -> StructureService:
    return StructureService(theme_repo=theme_repo, track_repo=track_repo)


def get_get_structure_interactor(
    service: Annotated[StructureService, Depends(get_structure_service)],
) -> GetStructureInteractor:
    return GetStructureInteractor(structure_service=service)


# --- Theme (write) ---


def get_theme_service(
    theme_repo: Annotated[ThemeRepository, Depends(get_theme_repository)],
    vision_repo: Annotated[VisionRepository, Depends(get_vision_repository)],
) -> ThemeService:
    return ThemeService(theme_repo=theme_repo, vision_repo=vision_repo)


def get_create_theme_interactor(
    service: Annotated[ThemeService, Depends(get_theme_service)],
) -> CreateThemeInteractor:
    return CreateThemeInteractor(theme_service=service)


def get_update_theme_interactor(
    service: Annotated[ThemeService, Depends(get_theme_service)],
) -> UpdateThemeInteractor:
    return UpdateThemeInteractor(theme_service=service)


def get_delete_theme_interactor(
    service: Annotated[ThemeService, Depends(get_theme_service)],
) -> DeleteThemeInteractor:
    return DeleteThemeInteractor(theme_service=service)


# --- Track (write) ---


def get_track_service(
    track_repo: Annotated[TrackRepository, Depends(get_track_repository)],
    theme_repo: Annotated[ThemeRepository, Depends(get_theme_repository)],
) -> TrackService:
    return TrackService(track_repo=track_repo, theme_repo=theme_repo)


def get_create_track_interactor(
    service: Annotated[TrackService, Depends(get_track_service)],
) -> CreateTrackInteractor:
    return CreateTrackInteractor(track_service=service)


def get_update_track_interactor(
    service: Annotated[TrackService, Depends(get_track_service)],
) -> UpdateTrackInteractor:
    return UpdateTrackInteractor(track_service=service)


def get_delete_track_interactor(
    service: Annotated[TrackService, Depends(get_track_service)],
) -> DeleteTrackInteractor:
    return DeleteTrackInteractor(track_service=service)


# --- Goal ---


def get_goal_repository(db: Annotated[AsyncSession, Depends(get_db)]) -> GoalRepository:
    return GoalRepository(db=db)


def get_phase_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PhaseRepository:
    return PhaseRepository(db=db)


def get_goal_service(
    goal_repo: Annotated[GoalRepository, Depends(get_goal_repository)],
    phase_repo: Annotated[PhaseRepository, Depends(get_phase_repository)],
) -> GoalService:
    return GoalService(goal_repo=goal_repo, phase_repo=phase_repo)


def get_list_goals_interactor(
    service: Annotated[GoalService, Depends(get_goal_service)],
) -> ListGoalsInteractor:
    return ListGoalsInteractor(goal_service=service)


def get_get_goal_detail_interactor(
    service: Annotated[GoalService, Depends(get_goal_service)],
) -> GetGoalDetailInteractor:
    return GetGoalDetailInteractor(goal_service=service)


def get_create_goal_interactor(
    service: Annotated[GoalService, Depends(get_goal_service)],
) -> CreateGoalInteractor:
    return CreateGoalInteractor(goal_service=service)


def get_update_goal_interactor(
    service: Annotated[GoalService, Depends(get_goal_service)],
) -> UpdateGoalInteractor:
    return UpdateGoalInteractor(goal_service=service)


def get_delete_goal_interactor(
    service: Annotated[GoalService, Depends(get_goal_service)],
) -> DeleteGoalInteractor:
    return DeleteGoalInteractor(goal_service=service)


# --- Phase ---


def get_phase_service(
    phase_repo: Annotated[PhaseRepository, Depends(get_phase_repository)],
    goal_repo: Annotated[GoalRepository, Depends(get_goal_repository)],
) -> PhaseService:
    return PhaseService(phase_repo=phase_repo, goal_repo=goal_repo)


def get_create_phase_interactor(
    service: Annotated[PhaseService, Depends(get_phase_service)],
) -> CreatePhaseInteractor:
    return CreatePhaseInteractor(phase_service=service)


def get_update_phase_interactor(
    service: Annotated[PhaseService, Depends(get_phase_service)],
) -> UpdatePhaseInteractor:
    return UpdatePhaseInteractor(phase_service=service)


def get_delete_phase_interactor(
    service: Annotated[PhaseService, Depends(get_phase_service)],
) -> DeletePhaseInteractor:
    return DeletePhaseInteractor(phase_service=service)


# --- Commitment ---


def get_commitment_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CommitmentRepository:
    return CommitmentRepository(db=db)


def get_commitment_service(
    commitment_repo: Annotated[
        CommitmentRepository, Depends(get_commitment_repository)
    ],
    phase_repo: Annotated[PhaseRepository, Depends(get_phase_repository)],
) -> CommitmentService:
    return CommitmentService(commitment_repo=commitment_repo, phase_repo=phase_repo)


def get_create_commitment_interactor(
    service: Annotated[CommitmentService, Depends(get_commitment_service)],
) -> CreateCommitmentInteractor:
    return CreateCommitmentInteractor(commitment_service=service)


# --- Execution Log ---


def get_execution_log_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ExecutionLogRepository:
    return ExecutionLogRepository(db=db)


def get_execution_log_service(
    log_repo: Annotated[ExecutionLogRepository, Depends(get_execution_log_repository)],
    commitment_repo: Annotated[
        CommitmentRepository, Depends(get_commitment_repository)
    ],
) -> ExecutionLogService:
    return ExecutionLogService(log_repo=log_repo, commitment_repo=commitment_repo)


def get_upsert_log_interactor(
    service: Annotated[ExecutionLogService, Depends(get_execution_log_service)],
) -> UpsertLogInteractor:
    return UpsertLogInteractor(log_service=service)


# --- Today ---


def get_reflection_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ReflectionRepository:
    return ReflectionRepository(db=db)


def get_today_service(
    commitment_repo: Annotated[
        CommitmentRepository, Depends(get_commitment_repository)
    ],
    log_repo: Annotated[ExecutionLogRepository, Depends(get_execution_log_repository)],
    reflection_repo: Annotated[
        ReflectionRepository, Depends(get_reflection_repository)
    ],
) -> TodayService:
    return TodayService(
        commitment_repo=commitment_repo,
        log_repo=log_repo,
        reflection_repo=reflection_repo,
    )


def get_get_today_interactor(
    service: Annotated[TodayService, Depends(get_today_service)],
) -> GetTodayInteractor:
    return GetTodayInteractor(today_service=service)


# --- History ---


def get_history_service(
    commitment_repo: Annotated[
        CommitmentRepository, Depends(get_commitment_repository)
    ],
    log_repo: Annotated[ExecutionLogRepository, Depends(get_execution_log_repository)],
) -> HistoryService:
    return HistoryService(
        commitment_repo=commitment_repo,
        log_repo=log_repo,
    )


def get_get_history_timeline_interactor(
    service: Annotated[HistoryService, Depends(get_history_service)],
) -> GetHistoryTimelineInteractor:
    return GetHistoryTimelineInteractor(history_service=service)


def get_get_history_calendar_interactor(
    service: Annotated[HistoryService, Depends(get_history_service)],
) -> GetHistoryCalendarInteractor:
    return GetHistoryCalendarInteractor(history_service=service)


# --- Auth guard ---


async def get_current_user_id(
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> int:
    logger.info("Getting current user id")
    if not credentials:
        raise UnauthorizedException()
    try:
        return await user_service.resolve_user_id_from_token(
            jwt_token=credentials.credentials
        )
    except UserService.UserAuthException as e:
        raise UnauthorizedException() from e
