"""Weekly learning plan routes."""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id
from app.schemas import WeeklyPlan

router = APIRouter()


@router.get("", response_model=list[WeeklyPlan], summary="List all weekly plans")
async def list_weekly_plans(
    user_id: UUID = Depends(get_current_user_id),
) -> list:
    """Retrieve all weekly plans for the authenticated user's roadmap."""
    return []


@router.get("/current", response_model=WeeklyPlan, summary="Get the current active weekly plan")
async def get_current_plan(
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Retrieve the user's active (current) weekly plan."""
    return {"message": "not implemented"}


@router.put(
    "/{plan_id}/tasks/{task_id}/complete",
    response_model=WeeklyPlan,
    summary="Mark a task as complete",
)
async def complete_task(
    plan_id: UUID,
    task_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Mark a specific task within a weekly plan as completed."""
    return {"message": "not implemented"}


@router.post("/adjust", response_model=WeeklyPlan, summary="Request AI adjustment to current plan")
async def adjust_plan(
    body: dict,
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Request an AI-driven adjustment to the current weekly plan."""
    return {"message": "not implemented"}
