from fastapi import APIRouter, Depends, HTTPException

from app import services

from app.api.dependencies import (
    get_current_user
)

from app.api.schemas import DashboardResponse

router = APIRouter(
    tags=["Dashboard"]
)

# ==========================================
# FINANCIAL DASHBOARD
# ==========================================

@router.get(
    "/users/me/dashboard",
    response_model=DashboardResponse,
    summary="Get financial dashboard"
)
def get_dashboard(
    current_user=Depends(
        get_current_user
    )
):

    user_id = current_user[0]

    dashboard = services.get_user_dashboard(
        user_id
    )

    if not dashboard:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return dashboard
