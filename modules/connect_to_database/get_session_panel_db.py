from urllib.parse import urlparse

from fastapi import Depends, Request, status
from sqlalchemy.ext.asyncio import async_sessionmaker

from modules.connect_to_database.database import get_session_panel_template_db
from modules.helper.panels_helper import PanelsHelper, get_panels_helper
from panels_project.exception import NotFoundPanelByDomainException


async def get_domain(request: Request) -> str:
    """Получение домена по объекту запроса"""
    domain = urlparse(str(request.base_url)).netloc.lower().strip()
    if ':' in domain:
        domain = domain[:domain.index(':')]
    return domain


async def found_panels_db_by_domain(
        domain: str = Depends(get_domain),
        panels_helper: PanelsHelper = Depends(get_panels_helper)
) -> str:
    """Определение названия базы данных по домену, если не нету то вернется None"""

    panel_with_domain = await panels_helper.get_panel_by_domain(domain=domain)
    if panel_with_domain is None:
        raise NotFoundPanelByDomainException(status_code=status.HTTP_200_OK)
    return panel_with_domain.db_name


async def get_session_panel_db(
        db_name: str = Depends(found_panels_db_by_domain)
) -> async_sessionmaker:
    """Подключение к базе данных по названию или None"""
    async_session = await get_session_panel_template_db(db_name)
    return async_session
