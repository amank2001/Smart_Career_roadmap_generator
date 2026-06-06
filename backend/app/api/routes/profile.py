"""Profile management routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File

from app.api.deps import get_current_user_id
from app.schemas import CreateProfileInput, Profile, UpdateProfileInput

router = APIRouter()


@router.post("", response_model=Profile, summary="Create user profile")
async def create_profile(
    body: CreateProfileInput,
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Create a new profile for the authenticated user."""
    return {"message": "not implemented"}


@router.put("", response_model=Profile, summary="Update user profile")
async def update_profile(
    body: UpdateProfileInput,
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Update the profile for the authenticated user."""
    return {"message": "not implemented"}


@router.get("", response_model=Profile, summary="Get current user profile")
async def get_profile(
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Retrieve the current authenticated user's profile."""
    return {"message": "not implemented"}


@router.post("/resume", summary="Upload resume for profile extraction")
async def upload_resume(
    file: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user_id),
) -> dict:
    """Upload a resume (PDF/DOCX/text) and extract profile information."""
    return {"message": "not implemented"}
