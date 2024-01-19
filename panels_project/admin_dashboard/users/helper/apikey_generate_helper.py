import random
import string
import time
from typing import AsyncGenerator, Union

from fastapi import Depends
from sqlalchemy import Integer, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from migration_system.models.panel_template_models import Users, UsersApikeyHistory
from modules.config_manager.config_manager import get_configs
from modules.connect_to_database.get_session_panel_db import get_session_panel_db
from panels_project.admin_dashboard.users.utils.apikey_hash_generate import hash_apikey_generate


class UsersAPIKeyHelper:
    """Класс для генерации и сохранения API ключа пользователя."""

    def __init__(self, db_session: AsyncSession) -> None:
        configs = get_configs()
        self.salt = configs["common"]["user_apikey_generate"]["user_apikey_salt"]
        self.k = configs["common"]["user_apikey_generate"]["user_apikey_length"]
        self.db_session = db_session

    async def generate_and_save_apikey(self, user_id: int) -> Union[str, dict]:
        """Генерация и сохранение API ключа пользователя."""

        # Генерация ключа
        apikey = ''.join(random.choices(string.ascii_letters + string.digits, k=self.k))
        # Хеширование ключа
        hashed = hash_apikey_generate(self.salt, apikey)

        # Извлечение и обновление пользователя
        stmt = select(Users).where(Users.id == cast(user_id, Integer))
        result = await self.db_session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            return {"error": "User not found"}

        user.apikey = hashed
        user.apikey_updated_at = int(time.time())

        # Добавление в историю ключей
        new_history = UsersApikeyHistory(
            user_id=user_id,
            apikey=hashed,
            created_at=int(time.time())
        )

        self.db_session.add(new_history)
        await self.db_session.commit()

        return apikey


async def get_user_helper(async_session: sessionmaker = Depends(get_session_panel_db)) -> AsyncGenerator:
    """Получение экземпляра класса UsersAPIKeyHelper."""

    async with async_session() as session:
        yield UsersAPIKeyHelper(session)

# @router.post("/generate_api_key/{user_id}")
# async def generate_api_key(
#     user_id: int,
#     helper: UsersAPIKeyHelper = Depends(get_user_helper)
# ):
#     return await helper.generate_and_save_apikey(user_id)
