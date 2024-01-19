from fastapi import Depends

from modules.helper.admin_auth_helper import AdminAuthHelper, get_admin_auth_helper
from panels_project.utils import CustomFastAPI

app_users_dashboard = CustomFastAPI(title='UsersDashboard')


@app_users_dashboard.get('/ping', tags=['Ping'], include_in_schema=False)
async def ping() -> str:
    return 'Users dashboard'


@app_users_dashboard.get('/ping_domain', tags=['Ping'])
async def ping_with_domain(
    panel_template_helper: AdminAuthHelper = Depends(get_admin_auth_helper)
) -> str:
    """Получение сессии по домену для сессии"""
    if panel_template_helper is None:
        return 'db is panels'

    result = panel_template_helper.__class__.__name__
    return result
