from fastapi import APIRouter, Depends

from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

router = APIRouter()


@router.get("/", dependencies=[Depends(get_panel_admin_hash)])
async def export_download(export_id: int):
    fixed_response = {
        "file": "...."
    }
    return fixed_response
