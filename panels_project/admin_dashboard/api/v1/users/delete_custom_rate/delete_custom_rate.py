from typing import List

from fastapi import APIRouter, Depends

from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

from .request_shemas import DeleteCustomRateRequest

router = APIRouter()


@router.post("/", dependencies=[Depends(get_panel_admin_hash)])
async def delete_custom_rate(request_data: List[DeleteCustomRateRequest]):
    fixed_response = {
        "status": "ok",
        "message": "Password setted"
    }
    return fixed_response
