from sqlalchemy import text

from migration_system.models.panel_models import PanelLanguages
from modules.config_manager.config_manager import get_configs
from modules.connect_to_database.database import get_session_panels_db as async_session

IS_DEFAULT = 1
NOT_DEFAULT = 0


async def populate_languages():
    """Метод заполнения таблицы языков после успешных миграций"""

    async_session_instance = await async_session()
    async with async_session_instance() as session:

        # Проверка существующих записей
        result = await session.execute(text('SELECT * FROM panels.panel_languages LIMIT 1'))
        existing_record = result.scalar_one_or_none()

        if existing_record is not None:
            return

        # Получение данных о языках
        config = get_configs()
        languages = config['languages']['languages']

        # Заполнение таблицы
        for code, details in languages.items():
            is_default = IS_DEFAULT if code == 'en' else NOT_DEFAULT
            language = PanelLanguages(
                code=code,
                name=details['name'],
                direction=details['direction'],
                default=is_default
            )

            session.add(language)
        await session.commit()
