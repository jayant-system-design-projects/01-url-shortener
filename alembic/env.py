from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, text
import os
import sys
from alembic import context
from dotenv import load_dotenv
from app.models.urls import Base
from app.log_base import get_logger

# Add the alembic script directory to sys.path so migration files can import
# shared utilities (e.g. migration_utils) via `from migration_utils import ...`
sys.path.insert(0, os.path.dirname(__file__))

logger = get_logger("alembic_env_file")
load_dotenv()
config = context.config

db_url = f'postgresql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOSTNAME")}:{os.getenv("DB_PORT_NUMBER")}/{os.getenv("DB_DATABASE_NAME")}'
if db_url:
    logger.info(f"[Alembic] Using DATABASE_URL from environment: {db_url}")
    config.set_main_option("sqlalchemy.url", db_url)
else:
    logger.info("[Alembic] No DATABASE_URL found in environment; using alembic.ini URL")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
target_schema = "my_url_shortener"


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {target_schema}"))
        connection.execute(text("COMMIT"))

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=target_schema,
            include_schemas=True,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
