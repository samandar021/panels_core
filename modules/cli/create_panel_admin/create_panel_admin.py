import typer

from modules.cli.create_panel_admin.schemas import AdminCreate
from modules.connect_to_database.database import get_session_panels_db as async_session
from modules.helper.cli_helper import create_admin


async def create_panel_admin_main(admin_data: AdminCreate):
    async_session_instance = await async_session()
    async with async_session_instance() as session:
        await create_admin(session, admin_data)
        typer.echo(f"Admin {admin_data.email} created!")
