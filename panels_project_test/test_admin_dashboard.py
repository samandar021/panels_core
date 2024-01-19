from httpx import AsyncClient

from panels_project.app import app


async def test_admin_ping():
    async with AsyncClient(app=app, base_url='http://test') as asyncclient:
        response = await asyncclient.get('/admin/ping')
    assert response.status_code == 200, \
        f'panels_project.admin_dashboard:ping return {response.status_code = }'
    assert response.text == '"Admin dashboard"', \
        f'panels_project.admin_dashboard:ping return {response.text = }'
