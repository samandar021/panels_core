from fastapi import APIRouter, Depends

from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

from .request_shemas import UpdateColumnsRequest

router = APIRouter()


@router.post("/", dependencies=[Depends(get_panel_admin_hash)])
async def update_columns(request_data: UpdateColumnsRequest):
    fixed_response = {
        "status": "ok",
        "message": "Columns updated"
    }
    return fixed_response
