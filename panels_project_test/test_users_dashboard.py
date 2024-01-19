from httpx import AsyncClient

from panels_project.app import app


async def test_user_ping():
    async with AsyncClient(app=app, base_url='http://test') as asyncclient:
        response = await asyncclient.get('/ping')
    assert response.status_code == 200, \
        f'panels_project.users_dasboard:ping return {response.status_code = }'
    assert response.text == '"Users dashboard"', \
        f'panels_project.users_dasboard:ping return {response.text = }'


async def test_user_ping_with_no_domain():
    async with AsyncClient(app=app, base_url='http://no_domain') as asyncclient:
        response = await asyncclient.get('/ping_domain')
    assert response.status_code == 200, \
        f'panels_project.users_dasboard:ping_with_domain return {response.status_code = }'

    normal_response = 'db is panels'
    assert normal_response in response.text, \
        f'panels_project.users_dasboard:ping_with_domain return {response.text = }'


async def test_user_ping_with_domain():
    async with AsyncClient(app=app, base_url='http://first_domain') as asyncclient:
        response = await asyncclient.get('/ping_domain')
    assert response.status_code == 200, \
        f'panels_project.users_dasboard:ping_with_domain return {response.status_code = }'

    assert response.text == '"AdminAuthHelper"', \
        f'panels_project.users_dasboard:ping_with_domain return {response.text = }'
