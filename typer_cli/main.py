import asyncio

import typer
from pydantic import ValidationError

from modules.cli.create_panel.create_panel import create_panel_main
from modules.cli.create_panel.schemas import CreatePanel
from modules.cli.create_panel_admin.create_panel_admin import create_panel_admin_main
from modules.cli.create_panel_admin.schemas import AdminCreate
from modules.utils.languages_loader import populate_languages

app = typer.Typer()


@app.command()
def run():
    typer.echo("Initializing...")


@app.command()
def create_panel_admin(panel_id: int, email: str, password: str):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_panel_admin_main(
            AdminCreate(panel_id=panel_id, email=email, password=password))
        )
    except ValidationError as e:
        typer.echo(f"Validation error: {e}")


@app.command()
def create_panel(panel_domain: str, is_subdomain: bool, email: str, password: str, currency: str):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_panel_main(CreatePanel(panel_domain=panel_domain,
                                                              is_subdomain=is_subdomain,
                                                              email=email,
                                                              password=password,
                                                              currency=currency))
                                )
    except ValidationError as e:
        typer.echo(f"Validation error: {e}")
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {e}")


@app.command()
def populate_langs():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(populate_languages())
        typer.echo("Successfully populated languages.")
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app()
