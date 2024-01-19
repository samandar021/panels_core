from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from panels_project.admin_dashboard.users.helper.apikey_generate_helper import UsersAPIKeyHelper


@pytest.mark.asyncio
async def test_generate_and_save_apikey():
    # Асинхронный мок сессии БД
    db_session = AsyncMock(spec=AsyncSession)
    # Синхронный мок результата запроса
    result = MagicMock()
    # Объединяем моки
    db_session.execute.return_value = result
    # Синхронный мок результата запроса
    result.scalar_one_or_none.return_value = MagicMock()

    # Инициализация объекта UsersAPIKeyHelper с замоканным db_session
    user_api_key_helper = UsersAPIKeyHelper(db_session=db_session)

    user_id = 1

    apikey_result = await user_api_key_helper.generate_and_save_apikey(user_id)

    assert isinstance(apikey_result, str)
    assert len(apikey_result) == user_api_key_helper.k

    db_session.execute.assert_awaited()
    db_session.commit.assert_awaited()
