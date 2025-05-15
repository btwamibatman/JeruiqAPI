# Infrastructure Folder

The `/infrastructure` folder manages external system interactions for the JeruyiqAPI project, such as database connectivity, migrations, and configuration, following clean architecture principles.

## Structure
- **`db/`**: Handles database-related functionality.
  - `base.py`: Defines the SQLAlchemy base class for ORM models.
  - `session.py`: Configures the database engine and session management.
  - `migrations/`:
    - `env.py`: Configures Alembic for database migrations.
- **`config.py`**: Manages project-wide configuration (e.g., environment variables, service URLs).

## Usage
- The `db/` module provides database connectivity and ORM setup, used by `adapters/` for persistence.
- The `config.py` module centralizes environment variable access, used across the application.
- The `migrations/` folder handles database schema migrations using Alembic.

## Development Guidelines
- Ensure all environment variables are loaded at the application’s entry point (e.g., in `app.py`).
- Use `ActiveConfig` from `config.py` to access environment-specific settings.
- Validate critical configuration variables in `config.py` to prevent runtime errors.
- Ensure proper session management in `session.py` using `SessionFactory` and `Session`.
- Dispose of the database engine during application shutdown to prevent resource leaks.
- Keep migrations in sync with ORM models defined in `db/base.py`.