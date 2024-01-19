from datetime import datetime
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Integer, String, cast, delete, func, select, update
from sqlalchemy.orm import sessionmaker

from migration_system.models.panel_models import PanelAdmin
from migration_system.models.panel_template_models import LanguageMessages, Languages
from modules.config_manager.config_manager import get_configs
from modules.connect_to_database.get_session_panel_db import get_session_panel_db
from modules.helper.abstract_helper import AbstractHelper
from panels_project.admin_dashboard.api.v1.settings.languages.langs_request_schemas import (LangChangeStatus,
                                                                                            LanguageCodeSchema,
                                                                                            LanguageEdit,
                                                                                            SortLanguageSchema)
from panels_project.admin_dashboard.api.v1.settings.languages.langs_response_schemas import (AvailableLanguagesSchema,
                                                                                             ColumnSchema,
                                                                                             LanguageDataSchema,
                                                                                             LanguageResponseSchema,
                                                                                             ListingResponseSchema,
                                                                                             PayloadsSchema)
from panels_project.languages.translator import Translator, get_translate

NO_DEFAULT = 0
IS_DEFAULT = 1
IS_VISIBLE = 1
DEFAULT_POSITION = 1


class LanguagesHelper(AbstractHelper):
    """Класс helper для работы с языками"""

    async def create_language_helper(self,
                                     language: LanguageCodeSchema,
                                     translater: Annotated[Translator, Depends(get_translate)],
                                     ) -> LanguageResponseSchema:
        """Метод для создания нового языка"""

        lang_code = language.lang_code
        lang_exist = await self.session.execute(
            select(Languages).where(Languages.lang_code == cast(lang_code, String))
        )
        result = lang_exist.scalars().first()
        if result:
            return LanguageResponseSchema(status="error",
                                          message=translater.chapter_languages('Language already exists'))

        # Получаем данные из конфига
        config = get_configs()
        if lang_code not in config['languages']['languages']:
            return LanguageResponseSchema(
                status="error",
                message=translater.chapter_languages('Incorrect language code')
            )

        lang_name = config['languages']['languages'][lang_code]['name']
        lang_direction = config['languages']['languages'][lang_code]['direction']

        # Найти наибольшее текущее значение position
        max_position_result = await self.session.execute(
            select(func.max(Languages.position).label("max_position"))
        )
        max_position = max_position_result.scalar_one_or_none()
        new_position = max_position + DEFAULT_POSITION if max_position is not None else DEFAULT_POSITION
        new_lang = Languages(
            lang_code=lang_code,
            name=lang_name,
            position=new_position,
            default=NO_DEFAULT,
            is_visible=IS_VISIBLE,
            direction=lang_direction,
            created_at=int(datetime.now().timestamp()),
        )

        self.session.add(new_lang)
        await self.session.commit()

        return LanguageResponseSchema(status="ok", message=translater.chapter_languages('Language added'))

    async def edit_language(self,
                            lang_edit: LanguageEdit,
                            translator: Annotated[Translator, Depends(get_translate)],
                            ) -> LanguageResponseSchema:
        """Метод для редактирования языка"""
        lang_code = lang_edit.lang_code
        lang_name = lang_edit.lang_name
        variables = lang_edit.variables

        # Обновление данных в таблице Languages
        if lang_name is not None:
            lang_result = await self.session.execute(
                select(Languages).where(Languages.lang_code == cast(lang_code, String)))
            lang = lang_result.scalars().first()
            if lang is None:
                return LanguageResponseSchema(status="error",
                                              message=translator.chapter_languages('Language not found'))

            lang.name = lang_name
            lang.updated_at = int(datetime.now().timestamp())

        # Обновление или удаление переменных в таблице LanguageMessages
        if variables is not None:
            for code, value in variables.items():
                var_result = await self.session.execute(
                    select(LanguageMessages)
                    .where(LanguageMessages.lang_code == cast(lang_code, String))
                    .where(LanguageMessages.code == cast(code, String))
                )
                var = var_result.scalars().first()

                if value == "":
                    if var:
                        await self.session.delete(var)
                else:
                    if var:
                        var.value = value
                    else:
                        new_var = LanguageMessages(
                            lang_code=lang_code,
                            code=code,
                            value=value
                        )
                        self.session.add(new_var)

        await self.session.commit()

        return LanguageResponseSchema(status="ok", message=translator.chapter_languages('Language updated'))

    async def change_status_helper(self,
                                   lang_status: LangChangeStatus,
                                   translator: Annotated[Translator, Depends(get_translate)],
                                   ) -> LanguageResponseSchema:
        """Метод для изменения статуса языка"""

        # Проверяем существует ли язык с таким кодом
        lang_result = await self.session.execute(
            select(Languages)
            .where(Languages.lang_code == cast(lang_status.lang_code, String))
        )
        lang = lang_result.scalars().first()

        # Если язык не найден, возвращаем ошибку
        if lang is None:
            return LanguageResponseSchema(status="error", message=translator.chapter_languages('Language not found'))

        # Изменяем статус языка
        lang.is_visible = lang_status.status
        lang.updated_at = int(datetime.now().timestamp())

        await self.session.commit()

        return LanguageResponseSchema(status="ok", message=translator.chapter_languages('Language status changed'))

    async def change_default_language(self,
                                      language: LanguageCodeSchema,
                                      translater: Annotated[Translator, Depends(get_translate)],
                                      ) -> LanguageResponseSchema:
        """Метод для изменения дефолтного языка"""

        new_default_lang_code = language.lang_code

        # Найти текущий дефолтный язык
        current_default_result = await self.session.execute(
            select(Languages)
            .where(Languages.default == cast(IS_DEFAULT, Integer))
        )
        current_default = current_default_result.scalars().first()

        if current_default is None:
            await self.session.execute(
                update(Languages)
                .where(Languages.lang_code == cast(new_default_lang_code, String))
                .values(default=IS_DEFAULT, is_visible=IS_VISIBLE)
            )
            await self.session.commit()
            return LanguageResponseSchema(status="ok",
                                          message=translater.chapter_languages('Default language changed'))

        else:
            # Перенести переводы с текущего дефолтного языка на новый
            current_default_messages_result = await self.session.execute(
                select(LanguageMessages)
                .where(LanguageMessages.lang_code == cast(current_default.lang_code, String))
            )
            current_default_messages = current_default_messages_result.scalars().all()

            new_default_messages_result = await self.session.execute(
                select(LanguageMessages)
                .where(LanguageMessages.lang_code == cast(new_default_lang_code, String))
            )
            new_default_messages = new_default_messages_result.scalars().all()

            new_default_message_codes = [msg.code for msg in new_default_messages]

            for msg in current_default_messages:
                if msg.code not in new_default_message_codes:
                    new_message = LanguageMessages(
                        lang_code=new_default_lang_code,
                        code=msg.code,
                        value=msg.value
                    )
                    self.session.add(new_message)

            # Изменить текущий дефолтный язык
            await self.session.execute(
                update(Languages)
                .where(Languages.default == cast(IS_DEFAULT, Integer))
                .values(default=NO_DEFAULT)
            )

            # Изменить новый дефолтный язык
            await self.session.execute(
                update(Languages)
                .where(Languages.lang_code == cast(new_default_lang_code, String))
                .values(default=IS_DEFAULT, is_visible=IS_VISIBLE)
            )

            # Изменить дефолтный язык в таблице PanelAdmin
            await self.session.execute(
                update(PanelAdmin)
                .values(lang_code=new_default_lang_code)
            )

            await self.session.commit()

            return LanguageResponseSchema(status="ok",
                                          message=translater.chapter_languages('Default language changed'))

    async def sort_languages_helper(self,
                                    sort_data: SortLanguageSchema,
                                    translater: Annotated[Translator, Depends(get_translate)],
                                    ) -> LanguageResponseSchema:
        """Метод для сортировки языков"""

        # Получаем все языки из БД и сортируем их по позиции
        result = await self.session.execute(select(Languages).order_by(Languages.position))
        all_languages = list(result.scalars().all())

        # Находим необходимый язык
        target_language = next((lang for lang in all_languages if lang.lang_code == sort_data.lang_code), None)
        if target_language is None:
            return LanguageResponseSchema(status="error",
                                          message=translater.chapter_languages('Language not found'))

        # Если новая позиция отличается от старой, удаляем язык из списка
        if sort_data.old_position != sort_data.new_position:
            del all_languages[sort_data.old_position - 1]

        # Вставляем целевой язык на новую позицию
        # Если new_position больше длины списка или равно 0, добавляем в конец.
        insert_position = min(sort_data.new_position - 1, len(all_languages))
        all_languages.insert(insert_position, target_language)

        # Пересчитываем позиции
        for index, lang in enumerate(all_languages):
            new_pos = index + 1
            lang.position = new_pos

        await self.session.commit()

        return LanguageResponseSchema(status="ok", message=translater.chapter_languages('Position changed'))

    async def reset_language_changes(self,
                                     lang_reset: LanguageCodeSchema,
                                     translator: Annotated[Translator, Depends(get_translate)],
                                     ) -> LanguageResponseSchema:
        """Метод для сброса изменений(переводов) языка"""

        # Удаление всех переводов для заданного языка
        await self.session.execute(
            delete(LanguageMessages)
            .where(LanguageMessages.lang_code == cast(lang_reset.lang_code, String))
        )

        # Возможно здесь надо восстановить дефолтные переводы
        # …

        await self.session.commit()

        return LanguageResponseSchema(status="ok",
                                      message=translator.chapter_languages('Default translations applied'))

    async def get_languages(self):
        """Метод для получения listing языков"""
        result = await self.session.execute(
            select(Languages).order_by(Languages.position)
        )
        all_languages = result.scalars().all()

        # Формируем данные активных языков для ответа
        data = [
            LanguageDataSchema(
                code=lang.lang_code,
                is_visible=lang.is_visible,
                updated=datetime.fromtimestamp(lang.updated_at).strftime(
                    "%d.%m.%Y %H:%M:%S") if lang.updated_at is not None else None,
                position=lang.position,
                name=lang.name
            ) for lang in all_languages if lang.is_visible == IS_VISIBLE
        ]

        # Формируем данные неактивных доступных языков для ответа
        available_languages = [
            AvailableLanguagesSchema(
                lang_code=lang.lang_code,
                name=lang.name
            ) for lang in all_languages if lang.is_visible != IS_VISIBLE
        ]

        columns = {
            "name": ColumnSchema(name="Name", sort=None),
            "is_visible": ColumnSchema(name="Visibility", sort=None),
            "updated": ColumnSchema(name="Last modified", sort={"is_active": None})
        }

        payloads = PayloadsSchema(
            data=data,
            columns=columns,
            list=["name", "is_visible", "updated"],
            available_languages=available_languages
        )

        response = ListingResponseSchema(
            status="ok",
            payloads=payloads
        )

        return response


async def get_languages_helper(async_session: sessionmaker = Depends(get_session_panel_db)):
    async with async_session() as session:
        yield LanguagesHelper(session)
