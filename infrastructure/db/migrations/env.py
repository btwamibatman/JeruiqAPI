import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# --- Start of Custom Changes ---

# Add your project root directory to the Python path
# This allows Alembic to import modules from your project, like infrastructure.db.models
# Assuming alembic.ini and the 'alembic' directory are in the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import your Base object from your models file
# This Base object should be the declarative base used by all your SQLAlchemy models
try:
    from infrastructure.db.models import Base
    target_metadata = Base.metadata
except ImportError:
    print("Could not import Base from infrastructure.db.models. Make sure the path is correct.")
    target_metadata = None # Set to None if models can't be found

# Import your Config object
try:
    from infrastructure.config import Config
    # Set the SQLAlchemy URL in the Alembic config using your application's Config
    config.set_main_option("sqlalchemy.url", Config.SQLALCHEMY_DATABASE_URL)
except ImportError:
    print("Could not import Config from infrastructure.config. Make sure the path is correct.")
    # Fallback to the URL in alembic.ini if Config cannot be imported
    pass # The url will remain whatever is in alembic.ini or None if not set


# --- End of Custom Changes ---


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a database to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()