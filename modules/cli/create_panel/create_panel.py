import asyncio
import datetime
import os

from modules.cli.create_panel.schemas import CreatePanel
from modules.cli.create_panel_admin.create_panel_admin import create_panel_admin_main
from modules.cli.create_panel_admin.schemas import AdminCreate
from modules.config_manager.config_manager import get_configs
from modules.connect_to_database.database import get_session_panels_db as async_session
from modules.crud.panels_crud import (check_panel_by_domain, create_domain, create_panel, generate_unique_db_name,
                                      generate_unique_system_subdomain)
from modules.helper.expired_date_helper import calculate_expired_date
from modules.utils.create_panel_utils import run_command_with_io
from modules.utils.idn_convertation import DomainConverter

config = get_configs()
DB_HOST = config['common']['db']['host']
DB_PORT = config['common']['db']['port']
DB_USERNAME = config['common']['db']['username']
DB_PASSWORD = config['common']['db']['password']
DB_DB = config['common']['db']['db_panel_template']
SYSTEM_DOMAIN_TYPE = 2
MYSQL = config['common']['mysql_commands']['mysql']
MYSQLDUMP = config['common']['mysql_commands']['mysqldump']


async def create_panel_main(panel_data: CreatePanel) -> None:
    """Метод создания панели"""

    async_session_instance = await async_session()
    async with async_session_instance() as session:
        # Конвертируем домен в punycode
        punycode_domain = DomainConverter.to_punycode(panel_data.panel_domain)
        # Проверяем, существует ли уже панель с таким доменом
        panel = await check_panel_by_domain(punycode_domain, session)

        if panel:
            raise Exception("Panel already exists")

        # Вычисляем дату окончания действия панели и создаем панель
        expired_date = calculate_expired_date(datetime.datetime.now())
        new_panel = await create_panel(panel_data, expired_date, session)
        if not new_panel:
            raise Exception("Panel not created")

        # Генерируем уникальное имя базы данных
        panel_with_db_name = await generate_unique_db_name(session, new_panel.id)
        if panel_with_db_name:
            # Создаем базу данных для панели
            await run_command_with_io(
                None, None, MYSQL, '-h', DB_HOST, '-P', str(DB_PORT), '-u',
                DB_USERNAME, '-p' + DB_PASSWORD, '-e', f"CREATE DATABASE {panel_with_db_name}"
            )

            # Генерируем уникальное имя системного поддомена
            unique_subdomain = await generate_unique_system_subdomain(panel_data.panel_domain, session)

            if unique_subdomain:
                # Создаем системный домен
                new_system_domain = await create_domain(new_panel.id, unique_subdomain, SYSTEM_DOMAIN_TYPE, session)

                if new_system_domain:
                    admin_data = AdminCreate(
                        panel_id=new_panel.id,
                        email=panel_data.email,
                        password=panel_data.password
                    )
                    await create_panel_admin_main(admin_data)

                    # Делаем дамп структуры базы данных во временный файл
                    dump_file = '/tmp/temp_db_dump.sql'
                    await run_command_with_io(
                        None, dump_file, MYSQLDUMP, '-h', DB_HOST, '-P', str(DB_PORT), '-u',
                        DB_USERNAME, '-p' + DB_PASSWORD, '--no-data', DB_DB
                    )

                    # Импортируем структуру базы данных в созданную базу данных
                    await run_command_with_io(
                        dump_file, None, MYSQL, '-h', DB_HOST, '-P', str(DB_PORT), '-u', DB_USERNAME,
                        '-p' + DB_PASSWORD, panel_with_db_name
                    )

                    # Удаляем временный файл
                    if os.path.exists(dump_file):
                        await asyncio.to_thread(os.remove, dump_file)
                    else:
                        print(f'Файл {dump_file} не существует. Пропускаем удаление.')
                else:
                    raise Exception("Error creating system/subdomain domains")
            else:
                raise Exception("Error generating unique subdomain")
        else:
            raise Exception("Error generating unique DB name")
