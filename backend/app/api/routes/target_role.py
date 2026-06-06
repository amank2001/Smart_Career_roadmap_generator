"""Target role selection and requirements routes."""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id
from app.schemas import CustomRoleInput, TargetRole, TargetRoleRequirements

router = APIRouter()


@router.post("", response_model=TargetRole, summary="Set a recognised target role")
async def set_target_role(
    body: dict,
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Set the user's target role by choosing from recognised roles."""
    return {"message": "not implemented"}


@router.get(
    "/requirements",
    response_model=TargetRoleRequirements,
    summary="Get skill requirements for target role",
)
async def get_requirements(
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Retrieve the skill requirements for the user's current target role."""
    return {"message": "not implemented"}


@router.put("/skills", response_model=TargetRole, summary="Update skills for target role")
async def update_skills(
    body: dict,
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Update the skill requirements associated with the target role."""
    return {"message": "not implemented"}


@router.post("/custom", response_model=TargetRole, summary="Set a custom target role")
async def set_custom_role(
    body: CustomRoleInput,
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Define a fully custom target role with user-specified skills."""
    return {"message": "not implemented"}
