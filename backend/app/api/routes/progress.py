"""Progress tracking routes."""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id
from app.schemas import ProgressSummary, TimelineEntry

router = APIRouter()


@router.get("", response_model=ProgressSummary, summary="Get overall progress summary")
async def get_progress(
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Retrieve a summary of the authenticated user's overall learning progress."""
    return {"message": "not implemented"}


@router.get(
    "/timeline",
    response_model=list[TimelineEntry],
    summary="Get progress timeline",
)
async def get_timeline(
    user_id: UUID = Depends(get_current_user_id),
) -> list:
    """Retrieve the full timeline of weekly plan completions and statuses."""
    return []
