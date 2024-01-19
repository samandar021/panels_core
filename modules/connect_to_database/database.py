from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from modules.config_manager.config_manager import get_configs

configs_database = get_configs()['common']['db']
host = configs_database['host']
password = configs_database['password']
username = configs_database['username']
port = configs_database['port']
panels_db = configs_database['database']


async def get_session(url_database: str) -> async_sessionmaker:
    """Подключение к бд"""
    engine = create_async_engine(url_database, future=True)
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False)
    return async_session


async def get_session_panels_db() -> async_sessionmaker:
    url_database = f'mysql+aiomysql://{username}:{password}@{host}:{port}/{panels_db}'
    return await get_session(url_database)


async def get_session_panel_template_db(panel_template_db: str) -> async_sessionmaker:
    url_database = f'mysql+aiomysql://{username}:{password}@{host}:{port}/{panel_template_db}'
    return await get_session(url_database)
