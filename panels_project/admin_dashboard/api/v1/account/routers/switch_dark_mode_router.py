from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import sessionmaker

from migration_system.models.panel_models import PanelAdminHash
from modules.connect_to_database.get_session_panel_db import get_session_panel_db
from panels_project.admin_dashboard.api.v1.account.handlers.switch_dark_mode_handler import switch_dark_mode_status
from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash

app_dark_mode = APIRouter()


@app_dark_mode.post("/darkmode")
async def switch_dark_mode(
        panel_id: int,
        status: int,
        session_maker: sessionmaker = Depends(get_session_panel_db),
        panel_admin_hash: PanelAdminHash = Depends(get_panel_admin_hash)
) -> dict:
    if session_maker is None:
        raise HTTPException(status_code=400, detail="Database not found: Failed to get session.")

    result = await switch_dark_mode_status(panel_id, status, session_maker, panel_admin_hash)
    return result
