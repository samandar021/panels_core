import unittest
from datetime import datetime
from unittest.mock import AsyncMock, Mock

from sqlalchemy.ext.asyncio import AsyncSession

from modules.helper.timezone_helper import adjust_timestamp_with_timezone


class TestAdjustTimestampWithTimezone(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.timestamp = int(datetime(2023, 8, 23).timestamp())
        self.panel_admin_id = 1
        self.panel_id = 1
        self.local_cache = {}  # Инициализация локального кеша

    async def test_adjust_timestamp_with_timezone_no_timezone(self):
        """Тестирование функции если нет ни админской ни панельной таймзоны"""
        session = AsyncMock(spec=AsyncSession)
        session.execute.return_value.fetchone = AsyncMock(return_value=Mock(admin_timezone=None, panel_timezone=None))

        adjusted_timestamp = await adjust_timestamp_with_timezone(session, self.timestamp, self.panel_admin_id,
                                                                  self.panel_id, self.local_cache)
        self.assertEqual(adjusted_timestamp, self.timestamp)

    async def test_adjust_timestamp_with_timezone_with_admin_timezone(self):
        """Тестирование функции если есть только админская таймзона"""
        session = AsyncMock(spec=AsyncSession)
        session.execute.return_value.fetchone = AsyncMock(return_value=Mock(admin_timezone=3600, panel_timezone=None))

        adjusted_timestamp = await adjust_timestamp_with_timezone(session, self.timestamp, self.panel_admin_id,
                                                                  self.panel_id, self.local_cache)
        self.assertEqual(adjusted_timestamp, self.timestamp + 3600)

    async def test_adjust_timestamp_with_timezone_with_panel_timezone(self):
        """Тестирование функции если есть только панельная таймзона"""
        session = AsyncMock(spec=AsyncSession)
        session.execute.return_value.fetchone = AsyncMock(return_value=Mock(admin_timezone=None, panel_timezone=7200))

        adjusted_timestamp = await adjust_timestamp_with_timezone(session, self.timestamp, self.panel_admin_id,
                                                                  self.panel_id, self.local_cache)
        self.assertEqual(adjusted_timestamp, self.timestamp + 7200)

    async def test_adjust_timestamp_with_timezone_cache_same_params(self):
        """При двух вызовах с одинаковыми параметрами функция должна вызывать SQL-запрос только один раз."""

        session = AsyncMock(spec=AsyncSession)
        session.execute.return_value.fetchone = AsyncMock(return_value=Mock(admin_timezone=3600, panel_timezone=None))

        # Первый вызов (данные ещё не в кеше)
        adjusted_timestamp1 = await adjust_timestamp_with_timezone(session, self.timestamp, self.panel_admin_id,
                                                                   self.panel_id, self.local_cache)

        # Второй вызов с теми же параметрами (данные должны быть взяты из кеша)
        adjusted_timestamp2 = await adjust_timestamp_with_timezone(session, self.timestamp, self.panel_admin_id,
                                                                   self.panel_id, self.local_cache)

        self.assertEqual(adjusted_timestamp1, self.timestamp + 3600)
        self.assertEqual(adjusted_timestamp2, self.timestamp + 3600)

        # Проверяем, что функция для выполнения SQL-запроса была вызвана только один раз.
        session.execute.assert_called_once()

    async def test_adjust_timestamp_with_timezone_cache_diff_params(self):
        """При двух вызовах с разными параметрами функция должна вызывать SQL-запрос два раза."""
        session = AsyncMock(spec=AsyncSession)
        session.execute.return_value.fetchone = AsyncMock(return_value=Mock(admin_timezone=3600, panel_timezone=None))

        # Первый вызов (данные ещё не в кеше)
        await adjust_timestamp_with_timezone(session, self.timestamp, self.panel_admin_id,
                                             self.panel_id, self.local_cache)

        # Второй вызов с другими параметрами (данные не должны быть взяты из кеша)
        await adjust_timestamp_with_timezone(session, self.timestamp, self.panel_admin_id + 1,
                                             self.panel_id + 1, self.local_cache)

        # Проверяем, что функция для выполнения SQL-запроса была вызвана два раза
        self.assertEqual(session.execute.call_count, 2)
