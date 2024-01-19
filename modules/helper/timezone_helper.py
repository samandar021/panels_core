from sqlalchemy import Integer, cast, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from migration_system.models.panel_models import PanelAdmin, Panels


async def adjust_timestamp_with_timezone(session: AsyncSession, timestamp: int,
                                         panel_admin_id: int, panel_id: int, request_cache: dict) -> int:
    """Функция для корректировки timestamp с учетом часового пояса."""

    # Создаем ключ для кеша
    cache_key = f"{panel_admin_id}_{panel_id}"

    if cache_key not in request_cache:
        # Делаем запрос в бд, присваивая лейблы для одинаковых полей, фильтруем по id панели или id админа панели
        query = select(PanelAdmin.timezone.label("admin_timezone"), Panels.timezone.label("panel_timezone")) \
            .outerjoin(Panels, cast(PanelAdmin.panel_id, Integer) == cast(Panels.id, Integer)) \
            .filter(or_(cast(PanelAdmin.id, Integer) == panel_admin_id, cast(Panels.id, Integer) == panel_id))

        # Выполняем запрос и получаем первую строку
        result = await session.execute(query)
        row = result.fetchone()
        request_cache[cache_key] = row
    else:
        row = request_cache[cache_key]

    # Если значение admin_timezone не None, используем его как смещение, иначе используем значение panel_timezone
    if row is None:
        raise ValueError('row is None')
    timezone_offset = row.admin_timezone if row.admin_timezone is not None else row.panel_timezone

    if timezone_offset is None:
        return timestamp

    return timestamp + timezone_offset
