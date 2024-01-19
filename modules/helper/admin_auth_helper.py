from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from modules.connect_to_database.get_session_panel_db import get_session_panel_db
from modules.helper.abstract_helper import AbstractHelper


class AdminAuthHelper(AbstractHelper):
    pass


async def get_admin_auth_helper(
    async_session: sessionmaker = Depends(get_session_panel_db)
) -> AsyncGenerator:
    async with async_session() as session:
        yield AdminAuthHelper(session)
