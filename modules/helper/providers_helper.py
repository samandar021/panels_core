import base64
import datetime
from typing import Annotated, AsyncGenerator, Optional

from fastapi import Depends
from sqlalchemy import Integer, String, and_, cast, delete, select
from sqlalchemy.orm import sessionmaker

from migration_system.models.panel_models import PanelProviderAPIKeyLog, PanelProviderHistory, PanelProviders, Providers
from modules.connect_to_database.get_session_panel_db import get_session_panel_db
from modules.helper.abstract_helper import AbstractHelper
from modules.utils.encryption import Encryption
from panels_project.admin_dashboard.api.v1.settings.providers.providers_request_schemas import (CreateProviderSchema,
                                                                                                DomainProviderSchema,
                                                                                                ProviderSchema,
                                                                                                ProviderUpdateSchema)
from panels_project.admin_dashboard.api.v1.settings.providers.providers_response_schemas import (
    PayloadProviderResponse, ProviderResponseSchema, SearchProviderSuccessResponse)
from panels_project.admin_dashboard.api.v1.settings.providers.utils import validate_domain
from panels_project.languages.translator import Translator, get_translate

HAS_FOUND = 1
NO_FOUND = 0


class ProviderServiceHelper(AbstractHelper):
    """Класс провайдера для работы с базой данных"""

    async def find_provider_by_domain(self, domain: str) -> Optional[Providers]:
        """Метод поиска провайдера по домену"""

        db_query = select(Providers).where(Providers.domain == cast(domain, String))
        result = await self.session.execute(db_query)
        provider = result.scalar_one_or_none()
        return provider

    async def find_panel_provider(self, panel_id, provider_id):
        """Метод поиска провайдера в таблице PanelProviders по panel_id и provider_id"""

        db_query = (
            select(PanelProviders)
            .where(
                and_(
                    PanelProviders.provider_id == cast(provider_id, Integer),
                    PanelProviders.panel_id == cast(panel_id, Integer),
                )
            )
        )
        result = await self.session.execute(db_query)
        provider = result.scalars().first()
        return provider

    async def add_to_db(self, entity):
        self.session.add(entity)

    async def commit_changes(self):
        await self.session.commit()

    async def delete_panel_provider(self, panel_id, provider_id):
        """Метод удаления провайдера из таблицы PanelProviders по panel_id и provider_id"""
        await self.session.execute(
            delete(PanelProviders).where(
                and_(
                    PanelProviders.provider_id == cast(provider_id, Integer),
                    PanelProviders.panel_id == cast(panel_id, Integer),
                )
            )
        )
        await self.session.commit()


class ProviderHelper:
    """Класс провайдера для работы с API (CRUD)"""

    def __init__(self, service: ProviderServiceHelper, translater: Annotated[Translator, Depends(get_translate)]):
        self.service = service
        self.translater = translater

    async def create_provider(
            self,
            data: CreateProviderSchema,
            panel_id: int,
    ) -> ProviderResponseSchema:
        """Метод создания провайдера"""

        # Проверяем, есть ли уже провайдер с таким доменом
        provider = await self.service.find_provider_by_domain(data.domain)

        if provider:
            # Проверяем, есть ли уже запись в PanelProviders с данным provider_id
            existing_panel_provider = await self.service.find_panel_provider(panel_id, provider.id)
            if existing_panel_provider:
                return self._response('fail', 'Provider already exists for this panel')
            # Создать новую запись в PanelProviders
            new_panel_provider = self._create_new_panel_provider(data, panel_id, provider.id)
            # Создать новую запись в PanelProviderAPIKeyLog
            new_panel_provider_apikey_log = self._create_new_apikey_log(data, panel_id, provider.id)

            await self.service.add_to_db(new_panel_provider)
            await self.service.add_to_db(new_panel_provider_apikey_log)
            await self.service.commit_changes()

            return self._response('ok', 'Provider created')

        return self._response('fail', 'Provider not found')

    async def edit_provider(
            self,
            data: ProviderUpdateSchema,
            panel_id: int,
    ) -> ProviderResponseSchema:
        """Метод редактирования провайдера"""

        # Поиск существующего провайдера с заданными panel_id и provider_id
        provider = await self.service.find_panel_provider(panel_id, data.provider_id)

        if not provider:
            return self._response('fail', 'Provider not found')

        # Обновляем данные провайдера
        provider = self._update_provider_data(provider, data)
        await self.service.add_to_db(provider)

        # Создаем запись в таблице логов
        new_panel_provider_apikey_log = self._create_new_apikey_log(data, panel_id, provider.id)
        await self.service.add_to_db(new_panel_provider_apikey_log)

        await self.service.commit_changes()

        return self._response('ok', 'Provider updated')

    async def delete_provider(
            self,
            data: ProviderSchema,
            panel_id: int,
    ) -> ProviderResponseSchema:
        """Метод удаления провайдера"""

        # Ищем провайдера в базе данных с заданными panel_id и provider_id
        provider = await self.service.find_panel_provider(panel_id, data.provider_id)

        # Если провайдер не найден, отправляем ошибку
        if not provider:
            return self._response('fail', 'Provider not found')

        # Удаляем провайдера
        await self.service.delete_panel_provider(panel_id, data.provider_id)

        return self._response('ok', 'Provider deleted')

    async def search_provider(
            self,
            data: DomainProviderSchema,
            panel_id: int,
    ):
        """Метод поиска провайдера по домену"""
        valid_domain = validate_domain(data.domain)

        provider = await self.service.find_provider_by_domain(valid_domain)

        # Log history
        log_entry = self._create_panel_provider_history(panel_id, valid_domain, provider is not None)
        await self.service.add_to_db(log_entry)
        await self.service.commit_changes()

        if provider:
            response = self._create_success_response(provider)
            return response.model_dump()
        else:
            return self._response('fail', 'Provider not found')

    def _response(self, status, message_key):
        """Метод для формирования ответа"""

        return ProviderResponseSchema(
            status=status,
            message=self.translater.settings_providers(message_key),
        )

    @staticmethod
    def _create_new_panel_provider(data, panel_id, provider_id):
        """Метод создания нового провайдера в таблице PanelProviders (create_provider)"""

        encryption_instance = Encryption()

        # Шифрование ключей провайдера
        encrypted_auth_field_1 = encryption_instance.execute(data.auth_field_1)
        encrypted_auth_field_2 = encryption_instance.execute(data.auth_field_2)
        encrypted_auth_field_3 = encryption_instance.execute(data.auth_field_3)

        # Создание объекта PanelProvider
        new_panel_provider = PanelProviders(
            panel_id=panel_id,
            provider_id=provider_id,
            auth_field_1=base64.b64encode(encrypted_auth_field_1).decode('utf-8'),
            auth_field_2=base64.b64encode(encrypted_auth_field_2).decode('utf-8'),
            auth_field_3=base64.b64encode(encrypted_auth_field_3).decode('utf-8'),
            created_at=int(datetime.datetime.now().timestamp())
        )
        return new_panel_provider

    @staticmethod
    def _create_new_apikey_log(data, panel_id, provider_id):
        """Метод создания логов провайдера в таблице PanelProviderAPIKeyLog"""

        # Создание объекта PanelProviderAPIKeyLog
        new_panel_provider_apikey_log = PanelProviderAPIKeyLog(
            panel_id=panel_id,
            provider_id=provider_id,
            auth_field_1=data.auth_field_1,
            auth_field_2=data.auth_field_2,
            auth_field_3=data.auth_field_3
        )
        return new_panel_provider_apikey_log

    @staticmethod
    def _update_provider_data(provider, data):
        """Метод обновления данных провайдера (edit_provider)"""

        # Обновление данных провайдера
        provider.auth_field_1 = data.auth_field_1
        provider.auth_field_2 = data.auth_field_2
        provider.auth_field_3 = data.auth_field_3
        provider.updated_at = int(datetime.datetime.now().timestamp())
        return provider

    @staticmethod
    def _create_panel_provider_history(panel_id, domain, has_found):
        """Метод создания записи истории поиска провайдера в таблице PanelProviderHistory (search_provider)"""

        log_entry = PanelProviderHistory(
            panel_id=panel_id,
            string=domain,
            has_found=HAS_FOUND if has_found else NO_FOUND,
            created_at=int(datetime.datetime.now().timestamp())
        )
        return log_entry

    @staticmethod
    def _create_success_response(provider):
        """Метод создания ответа при успешном поиске провайдера (search_provider)"""

        settings_form = provider.settings_form
        form_data = {
            key: value
            for key, value in settings_form.items()
        }
        payload_data = PayloadProviderResponse(id=provider.id, form=form_data)
        response = SearchProviderSuccessResponse(status='ok', payload=payload_data)
        return response


async def get_provider_helper(
        async_session: sessionmaker = Depends(get_session_panel_db),
        translater: Translator = Depends(get_translate),
) -> AsyncGenerator:
    async with async_session() as session:
        service_helper = ProviderServiceHelper(session)
        provider_helper = ProviderHelper(service_helper, translater)
        yield provider_helper
