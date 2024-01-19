import importlib
import warnings
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine, engine_from_config, pool, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from migration_system.models.panel_models import Base
from modules.config_manager.config_manager import get_configs

warnings.filterwarnings("ignore")
config = context.config
fileConfig(config.config_file_name)

configs_database = get_configs()['common']['db']
host = configs_database['host']
password = configs_database['password']
username = configs_database['username']
port = configs_database['port']
panels_db = configs_database['database']

DATABASE_PANELS_URL = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{panels_db}'
DATABASE_PANEL_TEMPLATE_URL = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/panel_template'

file_models_panels_template = Path(__file__).parent.joinpath('models').joinpath('panel_template_models.py')


def include_object(object, name, type_, reflected, compare_to):
    """Отсечение объектов у которых схема panels, при работе с panel_template"""
    if type_ == 'table' and object.schema is not None and 'panels' in object.schema:
        return False
    else:
        return True


def include_name(include_schemas):
    """Добавление нужных схем для оброботки alembic"""

    def inner(name, type_, parent_names):
        if type_ == "schema":
            return name in include_schemas
        else:
            return True

    return inner


def _run_migrations_online(connection, target_metadata, include_schemas=None) -> None:
    """Запуск миграций"""
    opthions = {}
    if include_schemas is not None:
        opthions.update(
            include_schemas=True,
            include_object=include_object,
            include_name=include_name(include_schemas),
        )
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        **opthions
    )

    with context.begin_transaction():
        try:
            context.run_migrations()
        except ProgrammingError as error:
            if 'already exists' not in str(error):
                connection.close()
                raise error


def run_migrations_online_panels_db() -> None:
    """Функция для работы с бд panels"""
    target_metadata = Base.metadata

    config.set_main_option('sqlalchemy.url', DATABASE_PANELS_URL)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        connection.execute(text('CREATE SCHEMA IF NOT EXISTS panel_template;'))
        connection.commit()
        _run_migrations_online(connection, target_metadata)


def _get_all_scheme_in_db() -> set[str] | list:
    """Получение всех db_name из panels.panels"""
    try:
        engine = create_engine(DATABASE_PANELS_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        scheme_in_db = session.execute(text('SELECT db_name FROM `panels`.`panels`;'))
    except ProgrammingError:
        return []
    else:
        scheme_in_db = scheme_in_db.all()
        if len(scheme_in_db) > 0:
            return {db_name[0] for db_name in scheme_in_db}
        return []


def _replace_scehema(origin_models: str, schema_name: str):
    """Добавление в Base.metadata модели panel_{db_name}"""
    input_text = "__table_args__ = {'mysql_engine': 'InnoDB'}"
    output_text = "__table_args__ = {'mysql_engine': 'InnoDB', 'schema': '" + schema_name + "'}"
    new_models = origin_models.replace(input_text, output_text)
    with open(file_models_panels_template, 'w') as file:
        file.write(new_models)

    import migration_system.models.panel_template_models as panel_template_models
    importlib.reload(panel_template_models)

    with open(file_models_panels_template, 'w') as file:
        file.write(origin_models)


def run_migrations_online_panel_template_db(origin_models) -> None:
    """Функция для работы с бд panel_template и panel_{db_name}"""
    from migration_system.models.panel_template_models import Base
    target_metadata = Base.metadata

    config.set_main_option('sqlalchemy.url', DATABASE_PANEL_TEMPLATE_URL)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    include_schemas = [None]
    with connectable.connect() as connection:

        all_scheme_in_db = _get_all_scheme_in_db()
        for schema_name in all_scheme_in_db:

            if schema_name:  # Проверяем, что schema_name не пустое и не None
                include_schemas.append(schema_name)
                connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schema_name};'))
                connection.commit()
            else:
                print("Warning: Empty schema name detected.")

            _replace_scehema(origin_models, schema_name)

        _run_migrations_online(connection, target_metadata, include_schemas)


def migrations_panel_template_db():
    """Обработка файла с моделями для запуска основной функции"""
    try:
        with open(file_models_panels_template, 'r') as file:
            origin_models = file.read()

        run_migrations_online_panel_template_db(origin_models)

    except Exception as error:
        with open(file_models_panels_template, 'w') as file:
            file.write(origin_models)
        raise error


if context.is_offline_mode():
    raise Exception('only online')
else:
    if config.cmd_opts.config == 'alembic_panels_db.ini':
        run_migrations_online_panels_db()
    elif config.cmd_opts.config == 'alembic_panel_template_db.ini':
        migrations_panel_template_db()
    else:
        raise Exception('Not found database, please look README')
