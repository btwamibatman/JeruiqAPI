from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from infrastructure.db import Base
from infrastructure.db.session import engine

# Читаем настройки Alembic
config = context.config

# Настройки логирования
fileConfig(config.config_file_name)

# Определяем модели, которые надо мигрировать
target_metadata = Base.metadata

def run_migrations_offline():
    """Генерация SQL-файлов без подключения к базе"""
    context.configure(url=engine.url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Обычные миграции в подключенной БД"""
    connectable = engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
