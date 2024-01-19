from fastapi import APIRouter, Depends

from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

from .request_shemas import CreatedExportRequest

router = APIRouter()


@router.post("/", dependencies=[Depends(get_panel_admin_hash)])
async def created_export(request_data: CreatedExportRequest):
    fixed_response = {
        "status": "ok",
        "message": "Export created"
    }
    return fixed_response
