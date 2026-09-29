from fastapi import APIRouter, Depends, HTTPException

from app import services

from app.api.dependencies import (
    get_current_user
)

from app.api.schemas import UserResponse

router = APIRouter(
    tags=["User"]
)

# ==========================================
# GET MY PROFILE
# ==========================================

@router.get(
    "/users/me",
    response_model=UserResponse,
    summary="Get my profile"
)
def get_my_profile(
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user[0]

    profile = services.get_user_profile(
        user_id
    )

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return profile
