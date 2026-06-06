"""Project suggestion routes."""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id
from app.schemas import ProjectSuggestion

router = APIRouter()


@router.get(
    "/suggestions/{plan_id}",
    response_model=list[ProjectSuggestion],
    summary="Get project suggestions for a weekly plan",
)
async def get_suggestions(
    plan_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> list:
    """Retrieve AI-generated project suggestions for a specific weekly plan milestone."""
    return []


@router.put(
    "/{project_id}/complete",
    response_model=ProjectSuggestion,
    summary="Mark a project as complete",
)
async def complete_project(
    project_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Mark a project suggestion as completed by the user."""
    return {"message": "not implemented"}


@router.put(
    "/{project_id}/dismiss",
    response_model=ProjectSuggestion,
    summary="Dismiss a project suggestion",
)
async def dismiss_project(
    project_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Dismiss a project suggestion so it no longer appears."""
    return {"message": "not implemented"}


@router.post(
    "/skip/{plan_id}",
    summary="Skip project for a weekly plan milestone",
)
async def skip_project(
    plan_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Skip the project suggestion for a given weekly plan milestone."""
    return {"message": "not implemented"}
