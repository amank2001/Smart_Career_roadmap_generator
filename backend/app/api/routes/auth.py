"""Authentication routes — register and login."""

from fastapi import APIRouter

from app.schemas import Token, UserCreate, UserLogin

router = APIRouter()


@router.post("/register", response_model=Token, summary="Register a new user")
async def register(body: UserCreate) -> dict:
    """Create a new user account and return a JWT token."""
    return {"message": "not implemented"}


@router.post("/token", response_model=Token, summary="Login and obtain JWT token")
async def login(body: UserLogin) -> dict:
    """Authenticate an existing user and return a JWT token."""
    return {"message": "not implemented"}
