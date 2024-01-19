from typing import Annotated

from fastapi import Depends
from sqlalchemy import Integer, cast, select

from migration_system.models.panel_models import PanelAdmin, PanelAdminHash
from panels_project.admin_dashboard.api.v1.auth.auth import get_panel_admin_hash


async def switch_dark_mode_status(panel_id: int, status: int, session_maker,
                                  panel_admin_hash: Annotated[PanelAdminHash, Depends(get_panel_admin_hash)]) -> dict:
    """Переключение статуса dark_mode"""
    async with session_maker() as session:
        result = await session.execute(
            select(PanelAdmin).where(PanelAdmin.id == cast(panel_admin_hash.panel_admin_id, Integer))
        )
        admin = result.scalar_one_or_none()

        if admin is None:
            print(f"No admin found for panel_id: {panel_id}")
            return {"status": "fail"}

        admin.dark_mode = status
        session.add(admin)
        await session.commit()

    return {"status": "ok"}
