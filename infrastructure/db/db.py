from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from infrastructure.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=Config.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()