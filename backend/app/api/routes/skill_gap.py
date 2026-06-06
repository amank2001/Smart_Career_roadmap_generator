"""Skill gap analysis routes."""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id
from app.schemas import SkillGapAnalysis

router = APIRouter()


@router.post(
    "/analyze",
    response_model=SkillGapAnalysis,
    summary="Run skill gap analysis",
)
async def analyze_skill_gap(
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Run AI-powered skill gap analysis comparing profile skills to target role requirements."""
    return {"message": "not implemented"}


@router.get(
    "/results",
    response_model=SkillGapAnalysis,
    summary="Get latest skill gap analysis results",
)
async def get_results(
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Retrieve the most recent skill gap analysis results for the authenticated user."""
    return {"message": "not implemented"}
