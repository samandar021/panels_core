from unittest.mock import AsyncMock, Mock

import pytest

from modules.crud.panels_crud import generate_unique_db_name  # Замените на реальный путь к вашей функции


@pytest.mark.asyncio  # для асинхронных тестов
async def test_generate_unique_db_name():
    # 1. Создаем mock-объект для session
    mock_session = AsyncMock()

    # 2. Настроим, чтобы mock возвращал нужные нам данные
    mock_scalars = AsyncMock()
    mock_scalars.all = AsyncMock(return_value=[
        Mock(db_name="panel_1"),
        Mock(db_name="panel_1_1"),
        Mock(db_name="panel_1_2")
    ])

    mock_result = Mock()
    mock_result.scalars.return_value = mock_scalars

    mock_session.execute.return_value = mock_result

    result = await generate_unique_db_name(mock_session, 1)

    # 4. Проверяем, что она возвращает ожидаемое имя БД
    assert result != "panel_1"
    assert result != "panel_1_1"
    assert result != "panel_1_2"
    assert result == "panel_1_3"
