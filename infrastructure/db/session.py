from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from infrastructure.config import ActiveConfig

# Use the DATABASE_URL from config
engine = create_engine(ActiveConfig.DATABASE_URL)

# Create a session factory
SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create a scoped session for thread-safe operations
Session = scoped_session(SessionFactory)

def dispose_engine():
    """Dispose the engine to release resources."""
    engine.dispose()