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

# --- Start of Custom Changes ---

# Add your project root directory to the Python path
# This allows Alembic to import modules from your project, like infrastructure.db.models
# Assuming alembic.ini and the 'alembic' directory are in the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Add print statements to debug the path and import
print(f"Project root added to sys.path: {project_root}")
print(f"Current sys.path: {sys.path}")

target_metadata = None # Initialize target_metadata to None

# Import your Base object from your models file
# This Base object should be the declarative base used by all your SQLAlchemy models
try:
    print("Attempting to import Base from infrastructure.db.models...")
    from infrastructure.db.models import Base
    target_metadata = Base.metadata
    print("Successfully imported Base and set target_metadata.")
except ImportError as e:
    print(f"ImportError: Could not import Base from infrastructure.db.models. Make sure the path is correct. Error: {e}")
    import traceback
    traceback.print_exc() # Print full traceback for import error
except Exception as e:
    print(f"An unexpected error occurred during import of Base: {e}")
    import traceback
    traceback.print_exc() # Print full traceback for other errors during import


# Import your Config object
try:
    from infrastructure.config import Config
    # Set the SQLAlchemy URL in the Alembic config using your application's Config
    config.set_main_option("sqlalchemy.url", Config.SQLALCHEMY_DATABASE_URL)
    print(f"Alembic using database URL from Config: {Config.SQLALCHEMY_DATABASE_URL}")
except ImportError:
    print("Could not import Config from infrastructure.config. Make sure the path is correct.")
    # Fallback to the URL in alembic.ini if Config cannot be imported
    pass


# --- End of Custom Changes ---


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata # This needs to be the actual metadata object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
