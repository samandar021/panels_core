from typing import List

from fastapi import APIRouter, Depends

from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

from .request_shemas import UpdateChangeStatusRequest

router = APIRouter()


@router.post("/", dependencies=[Depends(get_panel_admin_hash)])
async def change_status(request_data: List[UpdateChangeStatusRequest]):
    fixed_response = {
        "status": "ok",
        "message": "Status changed"
    }
    return fixed_response
