"""Learning roadmap generation and management routes."""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id
from app.schemas import LearningRoadmap

router = APIRouter()


@router.post("", response_model=LearningRoadmap, summary="Generate a personalised learning roadmap")
async def generate_roadmap(
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Generate an AI-powered learning roadmap based on the skill gap analysis."""
    return {"message": "not implemented"}


@router.get("", response_model=LearningRoadmap, summary="Get the current learning roadmap")
async def get_roadmap(
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Retrieve the authenticated user's current learning roadmap."""
    return {"message": "not implemented"}


@router.put("/hours", response_model=LearningRoadmap, summary="Update weekly study hours")
async def update_weekly_hours(
    body: dict,
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Update the number of weekly study hours and recalculate the roadmap timeline."""
    return {"message": "not implemented"}
