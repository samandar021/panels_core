import datetime
from typing import Optional

from sqlalchemy import Integer, String, Update, and_, cast, or_, select

from migration_system.models.panel_models import PanelDomains, PanelOptions, Panels
from modules.cli.create_panel.schemas import CreatePanel
from modules.config_manager.config_manager import get_configs
from modules.utils.idn_convertation import DomainConverter

DEFAULT_PLAN_ID = 1
DEFAULT_STATUS = 1


async def check_panel_by_domain(panel_domain: str, session) -> Optional[Panels]:
    stmt = select(Panels). \
        outerjoin(PanelDomains, PanelDomains.panel_id == Panels.id). \
        where(
        and_(
            or_(Panels.domain == cast(panel_domain, String), PanelDomains.domain == cast(panel_domain, String)),
            or_(Panels.status == 1, Panels.status == 2)
        )
    )
    result = await session.execute(stmt)
    panel = result.scalars().one_or_none()
    return panel


async def create_panel(panel_data: CreatePanel, expired_date, session) -> Optional[Panels]:
    """Метод создания панели"""

    punycode_domain: str = DomainConverter.to_punycode(panel_data.panel_domain)

    new_panel = Panels(
        domain=punycode_domain,
        created_at=int(datetime.datetime.now().timestamp()),
        expired_at=expired_date,
        currency=panel_data.currency,
        plan_id=DEFAULT_PLAN_ID,
        db_name='',
        status=DEFAULT_STATUS,
    )
    session.add(new_panel)
    await session.commit()
    return new_panel


async def generate_unique_db_name(session, panel_id: int) -> str:
    """Метод генерации уникального имени базы данных"""

    # Создаем базовое имя с префиксом
    base_db_name = f"panel_{panel_id}"
    result = await session.execute(select(Panels).where(
        Panels.db_name.like(f"{base_db_name}%")))
    rows = result.scalars().all()

    # Создаем множество существующих имён
    existing_dbs = {row.db_name for row in rows}
    index = 1
    db_name = base_db_name

    # Проверяем, существует ли уже такое имя в базе. Если да, добавляем индекс.
    while db_name in existing_dbs:
        db_name = f"{base_db_name}_{index}"
        index += 1

    return db_name


async def update_panel_with_bd_name(panel_id, db_name: str, session) -> Optional[Panels]:
    """Метод обновления панели с уникальным именем базы данных"""
    panel = await session.execute(Update(Panels).where(Panels.id == cast(panel_id, Integer)).values(db_name=db_name))
    await session.commit()
    return panel.scalars().one_or_none()


async def generate_unique_system_subdomain(client_domain: str, session) -> str:
    system_domain = get_configs()['common']['system_domain']
    base_subdomain = client_domain.replace(".", "-")

    subdomain = base_subdomain
    index = 1
    while True:
        # Проверяем, свободен ли домен
        full_subdomain = f"{subdomain}{system_domain}"
        result = await session.execute(
            select(PanelDomains).where(PanelDomains.domain == cast(full_subdomain, String))
        )
        existing_domain = result.scalar_one_or_none()

        if existing_domain is None:
            return full_subdomain

        # Если домен занят, добавляем индекс
        index_part = f"_{index}"
        if subdomain.endswith(index_part):
            subdomain = subdomain.rstrip(index_part)

        index += 1
        subdomain = f"{subdomain}{index_part}"


async def create_domain(panel_id: int, domain: str, domain_type: int, session) -> int:
    """Метод создания домена"""

    punycode_domain: str = DomainConverter.to_punycode(domain)

    new_domain = PanelDomains(
        panel_id=panel_id,
        domain=punycode_domain,
        domain_type=domain_type,
    )
    session.add(new_domain)
    await session.commit()
    return new_domain.id


async def create_panel_options(panel_id: int, session) -> int:
    """Метод создания опций панели"""
    new_panel_options = PanelOptions(panel_id=panel_id, signup_page=1)
    session.add(new_panel_options)
    await session.commit()
    return new_panel_options.id
